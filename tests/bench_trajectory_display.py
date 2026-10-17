"""轨迹显示性能基准: 顺序/逆序切换全部帧(模拟播放/导出与回看路径)。"""
import os, sys, time, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QColor
app = QApplication([])
from src.settings.settings import Settings
from src.settings.default_settings import SettingKey
from src.view.video_scene import VideoScene

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
tmp = tempfile.mkdtemp(prefix='qtb_')
shutil.copy(os.path.join(sys.path[0], '..', 'config.ini'), os.path.join(tmp, 'config.ini'))
settings = Settings(os.path.join(tmp, 'config.ini'))

# 启用轨迹与速度着色(压力最大路径)
settings.set_value(SettingKey.show_trajectory, True)
settings.set_value(SettingKey.trajectory_color_with_speed, True)

scene = VideoScene(None, settings)

# 帧缓存: 一张共享小图灌满(帧内容对轨迹渲染无影响)
img = QImage(300, 200, QImage.Format.Format_RGB888)
img.fill(QColor(0, 0, 0))
scene.cache_frame(1, img)
first = scene.frame_cache[1]
for i in range(1, N + 1):
    scene.frame_cache[i] = first

# 直接喂已知2粒子轨迹(等价分析完成后的状态)
for frame in range(1, N + 1):
    scene.data_helper.add_frame_particles(frame, {
        1: (50 + frame // 4, 60 + (frame % 40) // 4),
        2: (250 - frame // 6, 150 - (frame % 30) // 5),
    })

helper = scene.data_helper.trajectory_items
print(f'轨迹item: {len(helper)} 帧, 条目合计 {sum(len(v) for v in helper.values())}')

t0 = time.time()
for f in range(1, N + 1):
    scene.change_display(f)
seq = time.time() - t0
print(f'顺序切换 {N} 帧: {seq*1000:.1f} ms  (平均 {seq/N*1e6:.1f} us/帧), 当前显示轨迹 {len(scene.trajectory_items)}')

t0 = time.time()
for f in range(N, 0, -1):
    scene.change_display(f)
back = time.time() - t0
print(f'逆序切换 {N} 帧: {back*1000:.1f} ms, 当前显示轨迹 {len(scene.trajectory_items)}')

scene.clear_data()
shutil.rmtree(tmp, ignore_errors=True)