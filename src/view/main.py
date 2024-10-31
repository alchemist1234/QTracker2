import os

import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, QThread, QTimer, Slot, Qt
from PySide6.QtGui import QIcon

from src.settings.settings import Settings
from src.settings.default_settings import SettingKey
from src.view.setting import SettingDialog
from src.view.analyze_result import ResultDialog
from src.view.about import AboutDialog
from src.view.status_bar import StatusBar
from src.view.video_scene import VideoScene
from src.worker import VideoLoader, Analyzer
from src.ui.main_ui import Ui_main_window
from src.model.models import VideoMetaInfo
from src.model.enums import OperationMode, WorkingState


class MainWindow(QMainWindow):
    sig_pre_analyze = Signal(str)
    sig_update_path = Signal(str)
    sig_start_load = Signal(str)
    sig_start_analyze = Signal()
    sig_progress_update = Signal(WorkingState, int, int)

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        # 状态栏
        self.status_bar = StatusBar()
        self.setup_status_bar()

        self.icon_play = QIcon(':/icon/play')
        self.icon_pause = QIcon(':/icon/pause')
        # 从设置文件获取窗口大小
        self.resize(settings.int_value(SettingKey.main_width), settings.int_value(SettingKey.main_height))
        self.setting_dialog = SettingDialog(settings)

        self.file_path = None

        # 设置Graphics相关组件
        self.scene = VideoScene(self, self.settings)
        self.ui.gv_video.setScene(self.scene)

        # 粒子运动结果窗口
        self.result_dialog = ResultDialog(self.scene)

        # 关于窗口
        self.about_dialog = None

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
        self.video_loader_thread.start()
        self.analyzer_thread.start()

    def setup_status_bar(self):
        self.setStatusBar(self.status_bar)

    def setup_connects(self) -> None:
        """
        设置信号/槽连接
        """
        # 菜单按钮点击
        self.ui.m_act_open.triggered.connect(self.open_file)
        self.ui.m_act_setting.triggered.connect(self.open_settings)
        self.ui.m_act_export.triggered.connect(self.export_video)
        self.ui.m_act_analyze.triggered.connect(lambda: self.pre_analyze(self.file_path))
        self.ui.m_act_compute.triggered.connect(self.analyze_result)
        self.ui.m_act_exit.triggered.connect(self.close)
        self.ui.m_act_about.triggered.connect(self.open_about)
        # 工具栏按钮点击
        self.ui.t_act_open.triggered.connect(self.open_file)
        self.ui.t_act_setting.triggered.connect(self.open_settings)
        self.ui.t_act_analyze.triggered.connect(lambda: self.pre_analyze(self.file_path))
        self.ui.t_act_compute.triggered.connect(self.analyze_result)
        self.ui.t_act_export.triggered.connect(self.export_video)
        # 状态栏
        self.sig_progress_update.connect(self.status_bar.update_progress)
        # 设置
        self.setting_dialog.sig_display_settings_changed.connect(self.scene.refresh_items)
        # 视频加载/分析
        self.analyzer_thread.finished.connect(self.analyzer.stop)
        self.sig_update_path.connect(self.update_file_path)
        self.sig_pre_analyze.connect(self.pre_analyze)
        self.sig_start_load.connect(self.video_loader.load)
        self.sig_start_analyze.connect(self.analyzer.start_and_run)
        self.video_loader.sig_meta_info_updated.connect(self.video_meta_updated)
        self.video_loader.sig_frame_finished.connect(self.scene.add_frame)
        self.video_loader.sig_frame_finished.connect(self.analyze_data)
        self.video_loader.sig_frame_finished.connect(self.update_loading_progress)
        self.video_loader.sig_first_frame_finished.connect(self.scene.change_display)
        self.video_loader.sig_all_frame_finished.connect(self.all_analyze_data_send)
        self.ui.sl_frame.valueChanged.connect(self.scene.change_display)
        self.ui.sl_frame.valueChanged.connect(self.update_lcd_value)
        self.analyzer.sig_frame_analyzed.connect(self.scene.add_frame_particles)
        self.analyzer.sig_frame_analyzed.connect(self.update_analyzing_progress)
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
        self.ui.gv_video.btn_group.ui.btn_show_result.clicked.connect(self.show_result)
        self.result_dialog.sig_closed.connect(lambda: self.ui.gv_video.btn_group.ui.btn_show_result.setChecked(False))
        self.ui.le_filter.textChanged.connect(self.scene.set_filter)
        self.scene.sig_export_start.connect(lambda total: self.waiting_dialog.setRange(0, total))
        self.scene.sig_export_frame.connect(lambda frame: self.waiting_dialog.setValue(frame))
        self.scene.sig_export_frame.connect(self.update_export_progress)
        self.scene.sig_export_finish.connect(self.export_finished)
        self.scene.sig_frame_changed.connect(self.update_lcd_value)
        self.scene.sig_frame_changed.connect(self.update_slider_value)
        self.scene.sig_calculate_particle.connect(self.update_analyzing_progress)

    @Slot(int, np.ndarray)
    def analyze_data(self, frame_index: int, data: np.ndarray):
        """
        视频加载完后将数据发送到分析器
        :param frame_index: 帧ID
        :param data: 视频帧数据
        """
        self.analyzer.add_data(frame_index, data)

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
            self.file_path = path
            self.sig_update_path.emit(path)
            self.sig_pre_analyze.emit(path)

    @Slot(str)
    def pre_analyze(self, path: str) -> None:
        """
        分析前的清理工作，
        1. 停止现有分析循环
        2. 清除Scene上的Item
        :param path: 视频文件路径, 用于向sig_start_load信号传递参数
        """
        if path:
            self.analyzer.stop()
            self.scene.clear_data()
            self.sig_start_analyze.emit()
            self.sig_start_load.emit(path)

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
        self.ui.sl_frame.setMinimum(1)
        self.ui.sl_frame.setMaximum(meta_info.frame_count)
        if self.ui.sl_frame.value() > meta_info.frame_count:
            self.ui.sl_frame.setValue(meta_info.frame_count)
        # 更新配置中的FPS
        self.settings.set_value(SettingKey.fps, meta_info.fps)

    @Slot(int)
    def update_slider_value(self, value: int) -> None:
        """
        更新进度条
        :param value: 进度条值
        """
        if value > self.ui.sl_frame.maximum():
            value = self.ui.sl_frame.maximum()
        self.ui.sl_frame.setValue(value)

    @Slot(int)
    def update_lcd_value(self, value: int) -> None:
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
    def export_video(self) -> None:
        """
        导出视频
        """
        file_dir = ''
        file_name, file_type = QFileDialog.getSaveFileName(self, 'Export Video', file_dir,
                                                           filter='AVI File(*.avi);;FLV File(*.flv);;OGV File(*.ogv)')
        if not file_name:
            return
        file_path = os.path.join(file_dir, file_name)
        if len(file_path) > 0:
            self.waiting_dialog = QProgressDialog(self)
            self.waiting_dialog.setAutoClose(False)
            self.waiting_dialog.setWindowTitle('请稍候')
            self.waiting_dialog.setLabelText('正在导出...')
            self.waiting_dialog.setMinimumDuration(100)
            self.waiting_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            # 修改进度条样式
            self.waiting_dialog.setStyleSheet(u'QProgressBar{text-align: center;border: 1px;background: rgba(0,0,0,0)} QProgressBar::chunk{background: #22cc4a}')
            # 进度条满了之后不重置
            self.waiting_dialog.setAutoReset(False)
            # 禁用取消按钮
            btn = QPushButton('关闭')
            btn.setEnabled(False)
            self.waiting_dialog.setCancelButton(btn)
            # 禁用关闭按钮
            self.waiting_dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
            self.waiting_dialog.show()
            self.scene.export(file_path, self.video_meta.fps)

    def export_finished(self) -> None:
        """
        视频导出完成
        """
        self.waiting_dialog.setLabelText('导出完成')
        self.waiting_dialog.setCancelButton(QPushButton('关闭'))

    @Slot(bool)
    def show_result(self, show: bool) -> None:
        """
        显示/隐藏结果弹窗
        :param show: 是否显示
        """
        self.result_dialog.show() if show else self.result_dialog.hide()

    @Slot()
    def analyze_result(self) -> None:
        """
        分析粒子动动结果
        """
        fps = self.settings.int_value(SettingKey.fps)
        scale = self.settings.float_value(SettingKey.scale)
        if fps <= 0:
            fps, ok = QInputDialog.getInt(self, '未检测到FPS, 请输入', 'FPS')
            if not ok or fps <= 0:
                QMessageBox.warning(self, '结束', '无效FPS, 结果分析终止')
                return
        if scale <= 0:
            scale, ok = QInputDialog.getDouble(self, '未设置比例尺, 请输入', '比例尺(px/μm)')
            if not ok or scale <= 0:
                QMessageBox.warning(self, '结束', '无效比例尺, 结果分析终止')
                return
            else:
                # 更新配置中的scale值
                self.settings.set_value(SettingKey.scale, scale)
        self.scene.data_helper.analyze(fps, scale)

    @Slot()
    def open_about(self) -> None:
        """
        打开关于窗口
        """
        self.about_dialog = AboutDialog()
        self.about_dialog.show()

    def update_loading_progress(self, frame: int) -> None:
        """
        更新加载视频时状态栏进度
        :param frame: 当前帧
        """
        self.sig_progress_update.emit(WorkingState.LOAD, frame, self.video_meta.frame_count)

    def update_analyzing_progress(self, frame: int) -> None:
        """
        更新分析视频时状态栏进度
        :param frame: 当前帧
        """
        self.sig_progress_update.emit(WorkingState.ANALYZE, frame, self.video_meta.frame_count)

    def update_calculate_progress(self, current: int, total: int) -> None:
        """
        更新计算粒子数据时状态栏进度
        :param current: 当前已计算完粒子数
        :param total: 总粒子数
        """
        self.sig_progress_update.emit(WorkingState.CALCULATE, current, total)

    def update_export_progress(self, frame: int) -> None:
        """
        更新导出视频时状态栏进度
        :param frame: 当前帧
        """
        self.sig_progress_update.emit(WorkingState.EXPORT, frame, self.video_meta.frame_count)

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
