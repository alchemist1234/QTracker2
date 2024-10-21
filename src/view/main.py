import os

import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, QThread, QTimer, Slot, Qt
from PySide6.QtGui import QIcon

from src.settings.settings import Settings
from src.settings.default_settings import SettingKey
from src.view.setting import SettingDialog
from src.view.video_scene import VideoScene
from src.worker import VideoLoader, Analyzer
from src.ui.main_ui import Ui_main_window
from src.model.models import VideoMetaInfo, OperationMode


class MainWindow(QMainWindow):
    sig_update_path = Signal(str)
    sig_start_analyze = Signal(str)

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.icon_play = QIcon(':/icon/play')
        self.icon_pause = QIcon(':/icon/pause')
        # self.icon_pause.addFile(u":/icon/pause", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # 从设置文件获取窗口大小
        self.resize(settings.int_value(SettingKey.main_width), settings.int_value(SettingKey.main_height))
        self.setting_dialog = SettingDialog(settings)
        # 设置Graphics相关组件
        self.scene = VideoScene(self, self.settings)
        self.ui.gv_video.setScene(self.scene)

        # 视频加载线程
        self.video_loader_thread = QThread()
        self.video_loader = VideoLoader()
        self.video_loader.moveToThread(self.video_loader_thread)

        # 视频分析线程
        self.analyzer_thread = QThread()
        self.analyzer = Analyzer(settings)
        self.analyzer.moveToThread(self.analyzer_thread)

        self.play_timer = QTimer(self)
        self.playing = False

        self.waiting_dialog = None

        # 设置信息/槽连接
        self.setup_connects()

        # 额外数据
        self.video_meta = VideoMetaInfo()

        # 开启线程
        # TODO 是否可以在需要时开启和关闭
        self.video_loader_thread.start()
        self.analyzer_thread.start()

    def setup_connects(self) -> None:
        """
        设置信号/槽连接
        """
        # 工具栏按钮点击
        self.ui.act_open.triggered.connect(self.open_file)
        self.ui.act_setting.triggered.connect(self.open_settings)
        self.ui.act_export.triggered.connect(self.export_video)
        # 设置窗口
        # self.setting_dialog.accepted.connect(self.setting_accepted)
        # 视频加载/分析
        self.analyzer_thread.started.connect(self.analyzer.start)
        self.analyzer_thread.finished.connect(self.analyzer.stop)
        self.sig_update_path.connect(self.update_file_path)
        self.sig_start_analyze.connect(self.video_loader.load)
        self.video_loader.sig_meta_info_updated.connect(self.video_meta_updated)
        self.video_loader.sig_meta_info_updated.connect(self.analyzer_thread.start)
        self.video_loader.sig_frame_finished.connect(self.scene.add_frame)
        self.video_loader.sig_frame_finished.connect(self.analyze_data)
        self.video_loader.sig_first_frame_finished.connect(self.scene.change_display)
        self.video_loader.sig_first_frame_finished.connect(self.update_slider_value)
        self.video_loader.sig_all_frame_finished.connect(self.all_analyze_data_send)
        self.ui.sl_frame.valueChanged.connect(self.scene.change_display)
        self.ui.sl_frame.valueChanged.connect(self.update_lcd_value)
        self.analyzer.sig_frame_analyzed.connect(self.scene.add_frame_particles)
        self.analyzer_thread.started.connect(self.analyzer.run)
        self.ui.btn_play.clicked.connect(self.play_video)
        self.play_timer.timeout.connect(self.scene.change_to_next_frame)
        # view & scene
        self.ui.gv_video.btn_group.ui.btn_add.clicked.connect(lambda checked: self.scene.update_mode(OperationMode.ADD))
        self.ui.gv_video.btn_group.ui.btn_move.clicked.connect(
            lambda checked: self.scene.update_mode(OperationMode.MOVE))
        self.ui.gv_video.btn_group.ui.btn_crop.clicked.connect(
            lambda checked: self.scene.update_mode(OperationMode.CROP))
        self.ui.gv_video.btn_group.ui.btn_combine.clicked.connect(self.scene.combine_particles)
        self.ui.gv_video.btn_group.ui.btn_show_particle.clicked.connect(self.scene.set_particle_visible)
        self.ui.gv_video.btn_group.ui.btn_show_mark.clicked.connect(self.scene.set_mark_visible)
        self.ui.gv_video.btn_group.ui.btn_show_trajectory.clicked.connect(self.scene.set_trajectory_visible)
        self.ui.gv_video.btn_group.ui.btn_show_frame_index.clicked.connect(self.scene.set_frame_label_visible)
        self.ui.le_filter.textChanged.connect(self.scene.set_filter)
        self.scene.sig_export_start.connect(lambda total: self.waiting_dialog.setRange(0, total))
        self.scene.sig_export_frame.connect(lambda frame: self.waiting_dialog.setValue(frame))
        self.scene.sig_export_finish.connect(lambda: self.waiting_dialog.close())

    @Slot(int, np.ndarray)
    def analyze_data(self, frame_index: int, data: np.ndarray):
        """
        视频加载完后将数据发送到分析器
        :param frame_index: 帧ID
        :param data: 视频帧数据
        """
        self.analyzer.add_data(frame_index, data)

    @Slot()
    def stop_analyze(self):
        """
        停止分析
        """
        self.analyzer.stop()

    @Slot()
    def all_analyze_data_send(self):
        """
        所有帧数据发送完毕
        """
        self.analyzer.all_data_received()

    @Slot()
    def open_file(self) -> None:
        """
        打开文件
        """
        path, _ = QFileDialog.getOpenFileName(self, caption='Open File',
                                              filter='Video Files(*.mp4 *.avi *.mkv *.flv);;All File(*.*)')
        if path:
            print(f'path: {path}, ext: {_}')
            self.sig_update_path.emit(path)
            self.sig_start_analyze.emit(path)

    def open_settings(self) -> None:
        """
        打开设置
        """
        self.setting_dialog.load_settings()
        self.setting_dialog.show()

    @Slot(str)
    def update_file_path(self, file_path: str) -> None:
        """
        更新文件路径
        :param file_path: 文件全路径
        """
        self.ui.lb_file_path.setText(file_path)

    @Slot(int)
    def video_meta_updated(self, meta_info: VideoMetaInfo) -> None:
        """
        更新视频元数据
        :param meta_info: 视频元数据
        """
        self.video_meta = meta_info
        self.ui.sl_frame.setMaximum(meta_info.frame_count)
        if self.ui.sl_frame.value() > meta_info.frame_count:
            self.ui.sl_frame.setValue(meta_info.frame_count)

    @Slot(int)
    def update_slider_value(self, value: int) -> None:
        # TODO 改成从scene的change_frame发起信号连接本函数
        """
        更新进度条
        :param value: 进度条值
        """
        if value > self.ui.sl_frame.maximum():
            value = self.ui.sl_frame.maximum()
        self.ui.sl_frame.setValue(value)

    @Slot(int)
    def update_lcd_value(self, value: int) -> None:
        # TODO 改成从scene的change_frame发起信号连接本函数
        """
        更新LCD值
        :param value: 帧
        """
        self.ui.lcd_frame.display(f'{value}-{self.video_meta.frame_count}')

    @Slot()
    def play_video(self) -> None:
        """
        播放视频
        """
        if self.playing:
            # 停止播放
            self.play_timer.stop()
            self.playing = False
            self.ui.btn_play.setIcon(self.icon_play)
        else:
            # 播放
            fps = self.video_meta.fps
            if fps != 0:
                self.play_timer.setInterval(int(1000 / fps))
                self.play_timer.start()
                self.playing = True
                self.ui.btn_play.setIcon(self.icon_pause)

    @Slot()
    def export_video(self):
        file_dir = ''
        file_name, file_type = QFileDialog.getSaveFileName(self, 'Export Video', file_dir,
                                                           filter='AVI File(*.avi);;FLV File(*.flv);;OGV File(*.ogv)')
        if not file_name:
            return
        file_path = os.path.join(file_dir, file_name)
        if len(file_path) > 0:
            self.waiting_dialog = QProgressDialog(self)
            self.waiting_dialog.setWindowTitle('请稍候')
            self.waiting_dialog.setLabelText('正在导出...')
            self.waiting_dialog.setMinimumDuration(100)
            self.waiting_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            self.waiting_dialog.show()
            self.scene.export(file_path, self.video_meta.fps)

    def closeEvent(self, event) -> None:
        """
        重写退出方法，关闭线程
        :param event: 退出事件
        """
        # 停止子线程
        self.analyzer.stop()
        self.video_loader_thread.quit()
        # 等待子线程退出
        self.video_loader_thread.wait()
        self.analyzer_thread.quit()
        self.analyzer_thread.wait()
        super().closeEvent(event)
