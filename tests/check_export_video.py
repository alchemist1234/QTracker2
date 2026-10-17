"""导出端到端测试: 加载分析后直接调用 scene.export, 验证正常导出与格式校验路径
运行: LD_LIBRARY_PATH=<libEGL目录> python <本文件>
"""
import os
import sys
import time

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import cv2
import numpy as np

video_path = '/tmp/qt_gui_smoke.avi'  # 由GUI冒烟测试生成(2000帧)或现场生成
if not os.path.exists(video_path):
    vw = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (320, 240))
    for i in range(60):
        f = np.zeros((240, 320, 3), dtype=np.uint8)
        cv2.circle(f, (20 + (i % 40), 100), 5, (255, 255, 255), -1)
        vw.write(f)
    vw.release()

from PySide6.QtWidgets import QApplication, QProgressDialog

app = QApplication(sys.argv)
from src.view.main import MainWindow, Settings

settings = Settings('/tmp/qt_gui_cfg/config.ini')
win = MainWindow(settings)
win.show()
# 与 export_video 的真实流程一致: 先创建等待对话框再导出
win.waiting_dialog = QProgressDialog(win)
win.waiting_dialog.setAutoClose(False)
win.waiting_dialog.setAutoReset(False)

t0 = time.time()
win.pre_analyze(video_path)


def wait_done():
    if win.analyzer.running:
        wait_done.seen = True
    return (getattr(wait_done, 'seen', False) and not win.analyzer.running
            and not win.analyzer.receiving and win.analyzer.working)


wait_done.seen = False
deadline = time.time() + 60
ok = False
while time.time() < deadline:
    app.processEvents()
    if wait_done():
        ok = True
        break
    time.sleep(0.005)
assert ok, '分析未完成'
print(f'分析完成 {time.time() - t0:.1f}s, 帧数={len(win.scene.frame_cache)}')

# ---------------- 正常导出 ----------------
out_path = '/tmp/qt_export_out.avi'
if os.path.exists(out_path):
    os.unlink(out_path)
events = {'start': [], 'frames': [], 'finish': 0, 'error': []}
win.scene.sig_export_start.connect(lambda total: events['start'].append(total))
win.scene.sig_export_frame.connect(lambda frame: events['frames'].append(frame))
win.scene.sig_export_finish.connect(lambda: events.__setitem__('finish', events['finish'] + 1))
win.scene.sig_export_error.connect(lambda msg: events['error'].append(msg))

win.scene.export(out_path, 10)
app.processEvents()

assert not events['error'], f'导出报错: {events["error"]}'
assert events['finish'] == 1, f'未收到完成信号: {events}'
assert events['start'] and events['frames'], events
assert os.path.exists(out_path) and os.path.getsize(out_path) > 0, '导出文件为空'

cap = cv2.VideoCapture(out_path)
n = 0
while True:
    ret, _f = cap.read()
    if not ret:
        break
    n += 1
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap.release()
assert n == len(win.scene.sorted_frame_indexes()), f'导出帧数{n} != 源帧数'
assert win.waiting_dialog.labelText() == '导出完成', win.waiting_dialog.labelText()
print(f'正常导出 OK: {n} 帧 {w}px, 进度信号{len(events["frames"])}次')

# ---------------- 不支持格式 → error 信号 ----------------
events['error'].clear()
events['finish'] = 0
win.scene.export('/tmp/qt_export_bad.xyz', 10)
assert events['error'] and '不支持' in events['error'][0], events['error']
assert events['finish'] == 0
assert '导出失败' in win.waiting_dialog.labelText(), win.waiting_dialog.labelText()
print(f'格式校验 OK: {events["error"][0]}')

# ---------------- 主窗口前置校验逻辑 ----------------
import src.view.main as main_mod
assert '.xyz' not in main_mod.VideoScene.codes_map
print('codes_map 校验与主窗口一致 OK')

win.close()
app.processEvents()
print('\n导出端到端全部通过 ✅')
