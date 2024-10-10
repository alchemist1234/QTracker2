from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, Slot, QThread, Qt

from src.view.setting import *
from src.analyzer import Analyzer
from src.video_view import VideoView
from src.video_scene import VideoScene
from src.ui.main_ui import Ui_main_window
from src.ui.view_btn_grp_ui import Ui_wid_button_group


class ViewButtonGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui = Ui_wid_button_group()
        self.ui.setupUi(self)
        self.resize(36, 260)


class MainWindow(QMainWindow):
    sig_update_path = Signal(str)
    sig_start_analyze = Signal(str)

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        # 从设置文件获取窗口大小
        self.resize(settings.int_value(main_width), settings.int_value(main_height))
        self.setting_dialog = SettingDialog(settings)
        # 设置Graphics相关组件
        self.view = VideoView()
        self.scene = VideoScene(self.view)

        self.setup_graphics()

        self.analyzer_worker = QThread()
        self.analyzer = Analyzer()
        self.analyzer.moveToThread(self.analyzer_worker)
        self.analyzer_worker.start()

        self.setup_signals()

        self.total_frames = 0

    def setup_graphics(self) -> None:
        self.view.setScene(self.scene)
        self.ui.hbl_video.addWidget(self.view)
        self.ui.view_btn_grp = ViewButtonGroup()
        self.view.add_fixed_widget(self.ui.view_btn_grp, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

    def setup_signals(self) -> None:
        """
        设置信号/槽连接
        """
        self.ui.act_open.triggered.connect(self.open_file)
        self.ui.act_setting.triggered.connect(self.open_settings)
        self.setting_dialog.accepted.connect(self.setting_accepted)
        self.sig_update_path.connect(self.update_file_path)
        self.sig_start_analyze.connect(self.analyzer.analyze)
        self.analyzer.sig_frame_finished.connect(self.scene.add_frame)
        self.analyzer.sig_meta_info_updated.connect(self.total_frames_updated)
        self.analyzer.sig_first_frame_finished.connect(self.scene.change_display)
        self.analyzer.sig_first_frame_finished.connect(self.update_slider_value)
        self.ui.sl_frame.valueChanged.connect(self.scene.change_display)
        self.ui.sl_frame.valueChanged.connect(self.update_lcd_value)

    def open_file(self) -> None:
        """
        打开文件
        """
        path, _ = QFileDialog.getOpenFileName(self, caption='Open File', filter='*.mp4|*.avi|*.mkv|*.flv')
        self.sig_update_path.emit(path)
        self.sig_start_analyze.emit(path)

    def open_settings(self) -> None:
        """
        打开设置
        """
        self.setting_dialog.show()

    @Slot()
    def setting_accepted(self):
        self.setting_dialog.save_settings()

    @Slot(str)
    def update_file_path(self, file_path: str) -> None:
        """
        更新文件路径
        :param file_path: 文件全路径
        """
        self.ui.lb_file_path.setText(file_path)

    @Slot(int)
    def total_frames_updated(self, max_index: int) -> None:
        """
        更新帧最大值
        :param max_index: 最大帧数
        """
        self.total_frames = max_index
        self.ui.sl_frame.setMaximum(max_index)
        if self.ui.sl_frame.value() > max_index:
            self.ui.sl_frame.setValue(max_index)

    @Slot(int)
    def update_slider_value(self, value: int) -> None:
        if value > self.ui.sl_frame.maximum():
            value = self.ui.sl_frame.maximum()
        self.ui.sl_frame.setValue(value)

    @Slot(int)
    def update_lcd_value(self, value: int) -> None:
        self.ui.lcd_frame.display(f'{value}-{self.total_frames}')

    def closeEvent(self, event) -> None:
        """
        重写退出方法，关闭线程
        :param event: 退出事件
        """
        self.analyzer_worker.quit()
        self.analyzer_worker.wait()
        super().closeEvent(event)
