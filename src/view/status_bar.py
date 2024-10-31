from PySide6.QtWidgets import QStatusBar, QProgressBar, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, Slot

from src.model.enums import WorkingState


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(24)
        # 进度条
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setRange(0, 100)
        self.pb_progress.setValue(0)
        self.pb_progress.setFixedWidth(80)
        self.pb_progress.setFixedHeight(16)
        self.pb_progress.setTextVisible(False)
        self.pb_progress.setStyleSheet(u'QProgressBar{border: 1px;background: rgba(0,0,0,0);margin: 0px 4px} QProgressBar::chunk{background: #22cc4a} ')
        # 信息标签
        self.lb_progress_status = QLabel('就绪', self)
        self.lb_progress_status.setStyleSheet(u'QLabel{margin: 0px 4px}')
        # 忙碌/空闲状态显示标签
        self.lb_state = QLabel(self)
        self.free_pixmap = QPixmap(u':/icon/free').scaled(16, 16,
                                                          Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)
        self.busy_pixmap = QPixmap(u':/icon/busy').scaled(16, 16,
                                                          Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)
        self.lb_state.setPixmap(self.free_pixmap)

        self.addWidget(self.lb_progress_status)
        self.addWidget(self.pb_progress)
        self.addPermanentWidget(self.lb_state)

        # 最新更新状态
        self.working_state = None
        # 最新进度
        self.percent = 0
        # 定时器，定期更新进度条和状态
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_progress_display)
        self.timer.start()

    @Slot()
    def update_progress_display(self) -> None:
        """
        定期更新信息和进度条
        """
        self.pb_progress.setValue(self.percent)
        if self.percent == 100 or self.percent == 0:
            self.lb_progress_status.setText('就绪')
            self.lb_state.setPixmap(self.free_pixmap)
        else:
            if self.working_state:
                self.lb_progress_status.setText(f'正在{self.working_state.value[1]}')
            else:
                self.lb_progress_status.setText('就绪')
            self.lb_state.setPixmap(self.busy_pixmap)

    @Slot(WorkingState, int, int)
    def update_progress(self, working_state: WorkingState, current: int, total: int) -> None:
        """
        当前进度和信息更新
        :param working_state: 状态
        :param current: 当前值
        :param total: 总值
        """
        self.working_state = working_state
        self.percent = int(current * 100 / total)
