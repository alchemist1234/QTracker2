"""GUI 级冒烟测试(离屏): processEvents 驱动真实 MainWindow
覆盖: 分析全流程 + JPEG帧缓存 + 帧切换 + 加载中关窗不卡死 + 二次分析
运行: LD_LIBRARY_PATH=<libEGL目录> python <本文件>
"""
import os
import re
import shutil
import sys
import time

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import cv2
import numpy as np

# 生成 2000 帧测试视频: 半径5的移动圆点, 满足配置的面积过滤 [30, 99]
video_path = '/tmp/qt_gui_smoke.avi'
if not os.path.exists(video_path):
    vw = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (320, 240))
    assert vw.isOpened(), 'VideoWriter 打开失败'
    for i in range(2000):
        f = np.zeros((240, 320, 3), dtype=np.uint8)
        cv2.circle(f, (20 + (i % 280), 100 + (i % 40)), 5, (255, 255, 255), -1)
        vw.write(f)
    vw.release()

from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

from src.view.main import MainWindow, Settings

# 用仓库真实配置的副本(含旧版PySide序列化的值, 同时验证读取兜底), 不改写仓库文件
cfg_dir = '/tmp/qt_gui_cfg'
os.makedirs(cfg_dir, exist_ok=True)
cfg_path = os.path.join(cfg_dir, 'config.ini')
shutil.copy('/data/QTracker2/config.ini', cfg_path)
# 作者配置的面积过滤 [30, 99] 是为其实拍视频调的, 测试斑点检出面积~229,
# 放宽上限回默认3000以便验证分析管线(其余值保持原样, 含反序列化兜底场景)
with open(cfg_path, 'r', encoding='utf-8') as f:
    cfg_text = f.read()
cfg_text = re.sub(r'(maximum_area_for_detection\s*=\s*)99', r'\g<1>3000', cfg_text)
with open(cfg_path, 'w', encoding='utf-8') as f:
    f.write(cfg_text)
settings = Settings(cfg_path)


def total_particles(win):
    pp = win.scene.data_helper.particle_positions
    return sum(len(fp) for fp in pp.particles.values())


def pump(cond, timeout, tail=0.0):
    """驱动Qt事件循环直到cond为真或超时, 之后再泵tail秒"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        app.processEvents()
        if cond():
            end = time.time() + tail
            while time.time() < end:
                app.processEvents()
                time.sleep(0.01)
            return True
        time.sleep(0.005)
    return False


def wait_analysis(win):
    """等待一次 加载+分析 自然完成"""

    def done():
        if win.analyzer.running:
            done.seen = True
        return (getattr(done, 'seen', False) and not win.analyzer.running
                and not win.analyzer.receiving and win.analyzer.working)

    done.seen = False
    return pump(done, 90, tail=1.0)


# ---------------------------------------------------------------
# A. 分析全流程: 加载 + 分析 + 结果落地 (含背压与JPEG帧缓存)
# ---------------------------------------------------------------
win = MainWindow(settings)
win.show()

t_start = time.time()
win.pre_analyze(video_path)
assert wait_analysis(win), (f'分析未在90s内完成 (loader.running={win.video_loader.running}, '
                            f'analyzer.running={win.analyzer.running}, receiving={win.analyzer.receiving})')
elapsed_a = time.time() - t_start
particles = total_particles(win)
assert particles > 0, '分析完成但没有粒子'
cache_size = len(win.scene.frame_cache)
assert cache_size > 0, '帧缓存为空, JPEG缓存路径未工作'
print(f'A. 分析全流程 OK: {elapsed_a:.1f}s, 粒子数={particles}, 帧缓存={cache_size}')

# 帧切换不崩溃
win.scene.change_display(1)
win.scene.change_to_next_frame()
app.processEvents()
assert win.scene.current_frame_index == 2, win.scene.current_frame_index
print('A2. 帧切换 OK (1 -> 2)')

win.close()
app.processEvents()
assert win.video_loader_thread.isFinished() and win.analyzer_thread.isFinished(), '线程未退出'
print('A3. 分析完成后关闭 OK')

# ---------------------------------------------------------------
# B. 加载过程中关闭窗口: 必须立即返回 (旧实现会等到整段视频读完)
# ---------------------------------------------------------------
win2 = MainWindow(settings)
win2.show()
win2.pre_analyze(video_path)

started = pump(lambda: win2.video_loader.running, 10)
assert started, '加载未开始'
pump(lambda: False, 0.15)  # 让加载进行若干帧
assert win2.analyzer.receiving is True, '视频已加载完毕, 未能覆盖加载中场景'

t_close = time.time()
win2.close()
elapsed_b = time.time() - t_close
app.processEvents()
assert elapsed_b < 3.0, f'加载中关窗耗时 {elapsed_b:.2f}s, 疑似仍在等待加载'
assert win2.video_loader_thread.isFinished() and win2.analyzer_thread.isFinished(), '线程未退出'
print(f'B. 加载过程中关窗 OK: {elapsed_b:.2f}s (<3s)')

# ---------------------------------------------------------------
# C. 重新打开并分析, 验证二次使用(残留队列清理路径)
# ---------------------------------------------------------------
win3 = MainWindow(settings)
win3.show()
win3.pre_analyze(video_path)
assert wait_analysis(win3), '二次分析未完成'
p3 = total_particles(win3)
assert p3 > 0, '二次分析无粒子'
print(f'C. 二次分析 OK: 粒子数={p3}')
win3.close()
app.processEvents()
assert win3.video_loader_thread.isFinished() and win3.analyzer_thread.isFinished()

print('\nGUI 冒烟全部通过 ✅')
