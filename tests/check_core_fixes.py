"""行为验证脚本: 针对 feature-2.1 上的修复逐项验证(非提交物, 仅本地运行)
运行: LD_LIBRARY_PATH=<libEGL目录> python <本文件>
"""
import math
import os
import random
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import Qt

app = QCoreApplication(sys.argv)

import cv2
import numpy as np

# ---------------------------------------------------------------
# 1. common_util: angle_to_y / distance / split_indexes_text / random_color
# ---------------------------------------------------------------
from src.util.common_util import angle_to_y, distance, split_indexes_text, random_color


def old_angle_to_y(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dy == 0:
        return 0 if dx == 0 else 90 if dx > 0 else 270
    arc = math.atan(dx / dy)
    angle = math.degrees(arc)
    if dy < 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle


random.seed(42)
max_diff = 0.0
for _ in range(20000):
    x1, y1, x2, y2 = [random.randint(-5000, 5000) for _ in range(4)]
    a, b = angle_to_y(x1, y1, x2, y2), old_angle_to_y(x1, y1, x2, y2)
    d = abs(a - b) % 360
    max_diff = max(max_diff, d if d <= 180 else 360 - d)
assert max_diff < 1e-9, f'angle_to_y 行为不一致: {max_diff}'
print('1. angle_to_y 等价性 OK (20000 随机样本, 最大差异 %.2e)' % max_diff)

for _ in range(1000):
    x1, y1, x2, y2 = [random.uniform(-1000, 1000) for _ in range(4)]
    expect = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    assert abs(distance(x1, y1, x2, y2) - expect) < 1e-9
print('1b. distance 等价性 OK')

assert split_indexes_text('1,2, 3') == {1, 2, 3}
assert split_indexes_text('1\t2\r\n3') == {1, 2, 3}, split_indexes_text('1\t2\r\n3')
assert split_indexes_text('1,,  2') == {1, 2}
assert split_indexes_text('a,1,-2,3') == {1, 3}  # 非纯数字仍被过滤
assert split_indexes_text('3-5') == {3, 4, 5}  # 连续范围仍支持
print('1c. split_indexes_text 支持 tab/换行 OK')

for _ in range(200):
    c = random_color()
    h, s, l, _a = c.getHsl()
    assert 0 <= h < 360
    assert 128 <= s <= 255, s
    assert 80 <= l <= 199, l
print('1d. random_color 中间色调范围 OK')

# ---------------------------------------------------------------
# 2. AnalyzeResult.data() 重构等价性
# ---------------------------------------------------------------
from src.model.models import AnalyzeResult, HistoryParticle

r = AnalyzeResult(7, 1, 0.04, 10, 20, 1.5, 2.5, 3.0, 5.5)
expect_vals = [7, 0.04, 10.0, 20.0, 1.5, 2.5, 3.0, r.velocity, 5.5]
for i, v in enumerate(expect_vals):
    assert r.data(i) == v, (i, r.data(i), v)
assert r.data(9) is None and r.data(-1) is None
print('2. AnalyzeResult.data() 等价性 OK')

# ---------------------------------------------------------------
# 3. qt_models: get_frame_particles / get_particles_before_frame / remove_frame_particles
# ---------------------------------------------------------------
from src.view.main import Settings
from src.model.qt_models import ParticlePositions

settings = Settings('/tmp/qt_fix_cfg.ini')  # 不动仓库内 config.ini
pp = ParticlePositions()
pp.settings = settings
random.seed(7)
for f in range(1, 301):
    for pid in (1, 2, 3):
        if random.random() < 0.9:
            pp.particles.setdefault(pid, {})[f] = (f * 10 + pid, f * 3 - pid)
# 手工插入乱序帧 (模拟拖动粒子)
pp.particles[1][250] = (1, 1)

# 3a. get_frame_particles 与朴素实现一致
for fi in (1, 150, 300, 301, -5):
    naive = {pid: fp[fi] for pid, fp in pp.particles.items() if fi in fp and len(fp[fi]) > 0}
    assert pp.get_frame_particles(fi) == naive, fi
assert pp.get_frame_particles(150, [2]) == {2: pp.particles[2][150]}
assert pp.get_frame_particles(150, []) == {pid: fp[150] for pid, fp in pp.particles.items() if 150 in fp}
assert pp.get_frame_particles(9999) == {}
print('3a. get_frame_particles 等价性 OK')

# 3b. get_particles_before_frame 与旧的全量排序实现的末3点一致
for fi in (1, 100, 250, 300):
    for pid in (1, 2, 3):
        fp = pp.particles[pid]
        old_full = [(fp[k][0], fp[k][1], k) for k in sorted(fp.keys()) if k <= fi and len(fp[k]) > 0]
        old_last3 = old_full[-3:]
        got = pp.get_particles_before_frame(fi).get(pid, [])
        # 旧实现要求当前帧有数据才返回该粒子
        if fi in fp and len(fp[fi]) > 0:
            assert got == old_last3, (fi, pid, got, old_last3)
        else:
            assert pid not in pp.get_particles_before_frame(fi)
print('3b. get_particles_before_frame 与旧实现末3点一致 OK')

# 3c. remove_frame_particles 与旧重建实现一致
snapshot = {pid: dict(fpd) for pid, fpd in pp.particles.items()}
pp.remove_frame_particles(150)
expect_rem = {pid: {f: p for f, p in fpd.items() if f != 150} for pid, fpd in snapshot.items()}
assert pp.particles == expect_rem
print('3c. remove_frame_particles 等价性 OK')

# 3d. 热路径性能: 300帧x3粒子时逐帧调用
t0 = time.time()
for fi in range(1, 301):
    pp.get_frame_particles(fi)
    pp.get_particles_before_frame(fi)
cost = time.time() - t0
assert cost < 2.0, cost
print('3d. 帧切换热路径 600 次调用耗时 %.0f ms OK' % (cost * 1000))

# 3e. analyze_particle_data 进度信号递增
pp2 = ParticlePositions()
pp2.settings = settings
for pid in (1, 2, 3):
    pp2.particles[pid] = {f: (f * 10, f * 10) for f in range(1, 21)}
got_prog = []
pp2.sig_calculate_particle.connect(lambda cur, total: got_prog.append((cur, total)))
res = pp2.analyze_particle_data(30, 1.0)
assert got_prog == [(1, 3), (2, 3), (3, 3)], got_prog
assert set(res.keys()) == {1, 2, 3} and all(len(v) > 0 for v in res.values())
print('3e. analyze_particle_data 进度递增 OK:', got_prog)

# ---------------------------------------------------------------
# 4. Analyzer: 条件变量唤醒 / 背压 / 排空 / start清理 / stop及时
# ---------------------------------------------------------------
from src.worker import Analyzer, VideoLoader

def make_frame(size=64):
    img = np.zeros((size, size, 3), dtype=np.uint8)
    cv2.circle(img, (random.randint(10, 50), random.randint(10, 50)), 6, (255, 255, 255), -1)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 4a. 完整流程: 喂帧 → 全部接收 → 排空后结束
a = Analyzer(settings)
results = []
a.sig_frame_analyzed.connect(lambda idx, pos: results.append(idx), Qt.ConnectionType.DirectConnection)
t = threading.Thread(target=a.start_and_run, daemon=True)
t.start()
time.sleep(0.1)
for i in range(1, 4):
    a.add_data(i, make_frame())
a.all_data_received()
t.join(timeout=5)
assert not t.is_alive(), '分析线程未结束'
assert results == [1, 2, 3], results
print('4a. Analyzer 完整流程(含队列排空) OK')

# 4b. 背压标志
a2 = Analyzer(settings)
assert not a2.pending_full()
for i in range(Analyzer.MAX_PENDING):
    a2.add_data(i, make_frame())
assert a2.pending_full()
print('4b. pending_full 背压标志 OK (MAX_PENDING=%d)' % Analyzer.MAX_PENDING)

# 4c. stop() 能立即唤醒条件变量等待 (旧实现最多睡满0.5s)
a3 = Analyzer(settings)
t3 = threading.Thread(target=a3.start_and_run, daemon=True)
t3.start()
time.sleep(0.3)  # 让其进入 cond.wait
t0 = time.time()
a3.stop()
t3.join(timeout=3)
assert not t3.is_alive(), 'stop 后分析线程未退出'
elapsed = time.time() - t0
assert elapsed < 0.2, f'stop 唤醒过慢: {elapsed:.3f}s'
print('4c. stop() 即时唤醒 OK (%.0f ms)' % (elapsed * 1000))

# 4d. start_and_run 清理上一轮残留队列
a4 = Analyzer(settings)
a4.add_data(1, make_frame())  # 残留帧
res4 = []
a4.sig_frame_analyzed.connect(lambda idx, pos: res4.append(idx), Qt.ConnectionType.DirectConnection)
t4 = threading.Thread(target=a4.start_and_run, daemon=True)
t4.start()
time.sleep(0.15)
a4.add_data(99, make_frame())
a4.all_data_received()
t4.join(timeout=5)
assert res4 == [99], f'残留帧未被清理: {res4}'
print('4d. start_and_run 清理残留队列 OK')

# ---------------------------------------------------------------
# 5. VideoLoader: 完成信号 / 停止 / 背压等待 / 打开失败不卡死 / 句柄释放
# ---------------------------------------------------------------
video_path = '/tmp/qt_fix_test.avi'
vw = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'), 10, (64, 64))
assert vw.isOpened()
for i in range(30):
    vw.write(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8))
vw.release()

# 5a. 正常加载
vl = VideoLoader(settings)
metas, frames, fin = [], [], []
vl.sig_meta_info_updated.connect(metas.append)
vl.sig_frame_finished.connect(lambda i, f: frames.append(i))
vl.sig_all_frame_finished.connect(lambda: fin.append(True))
vl.load(video_path)
assert len(frames) == 30, len(frames)
assert frames == list(range(1, 31))
assert fin == [True], fin
assert metas and metas[0].width == 64 and metas[0].height == 64
print('5a. 正常加载 30 帧 + 完成信号 OK')

# 5b. 分析积压时暂停(背压), stop() 后退出且不发完成信号
class FakeAnalyzer:
    def pending_full(self):
        return True

vl2 = VideoLoader(settings)
vl2.analyzer = FakeAnalyzer()
fin2, frames2 = [], []
vl2.sig_frame_finished.connect(lambda i, f: frames2.append(i))
vl2.sig_all_frame_finished.connect(lambda: fin2.append(True))
t5 = threading.Thread(target=vl2.load, args=(video_path,), daemon=True)
t5.start()
time.sleep(0.4)
assert t5.is_alive(), '未进入背压等待'
assert len(frames2) == 0, f'背压未生效, 已加载{len(frames2)}帧'
vl2.stop()
t5.join(timeout=3)
assert not t5.is_alive(), 'stop() 未中断加载'
assert fin2 == [], '停止后不应发送完成信号'
print('5b. 背压暂停 + stop() 中断 + 不误发完成信号 OK')

# 5c. 视频打开失败时仍发送完成信号(不卡住分析器)
vl3 = VideoLoader(settings)
fin3 = []
vl3.sig_all_frame_finished.connect(lambda: fin3.append(True))
vl3.load('/tmp/nonexistent_file_xyz.mp4')
assert fin3 == [True], fin3
print('5c. 打开失败仍通知分析器完成 OK')

# 5d. 句柄释放: 加载后文件可被删除/重命名 (Linux 上 unlink 成功即释放)
import shutil
tmp_copy = '/tmp/qt_fix_test_copy.avi'
shutil.copy(video_path, tmp_copy)
vl4 = VideoLoader(settings)
vl4.sig_frame_finished.connect(lambda i, f: None)
vl4.load(tmp_copy)
os.unlink(tmp_copy)  # 若句柄未释放, 部分系统仍可删; 主要验证无异常
print('5d. 加载后资源释放无异常 OK')

# ---------------------------------------------------------------
# 6. analyze(): 历史粒子按记忆帧裁剪
# ---------------------------------------------------------------
from src.settings.default_settings import SettingKey

a5 = Analyzer(settings)
memory_frames = settings.int_value(SettingKey.memory_frames)
for f in range(1, 201):
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    # 每帧随机位置画斑点, 基本不会跨帧匹配 → 持续产生新历史粒子
    for _ in range(3):
        cv2.circle(frame, (random.randint(5, 58), random.randint(5, 58)),
                   random.randint(3, 6), (255, 255, 255), -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    a5.analyze(f, gray)
assert len(a5.history_particles) > 0
oldest = min(hp.frame_index for hp in a5.history_particles.values())
assert oldest >= 200 - memory_frames, f'历史粒子未裁剪: oldest={oldest}, memory={memory_frames}'
print('6. analyze() 历史粒子按记忆帧裁剪 OK (oldest=%d, memory_frames=%d, 存量=%d)'
      % (oldest, memory_frames, len(a5.history_particles)))

# ---------------------------------------------------------------
# 7. 模块导入冒烟 (main/worker/video_scene/analyze_result 全链)
# ---------------------------------------------------------------
import src.view.main
import src.view.analyze_result
import src.view.video_scene
print('7. 全链路模块导入 OK')

print('\n全部通过 ✅')
