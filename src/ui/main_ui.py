# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLCDNumber, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSlider,
    QStatusBar, QToolBar, QVBoxLayout, QWidget)

from src.view.video_view import VideoView
import resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/icon/favicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main_window.setWindowIcon(icon)
        self.t_act_open = QAction(main_window)
        self.t_act_open.setObjectName(u"t_act_open")
        icon1 = QIcon()
        icon1.addFile(u":/icon/open_file", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.t_act_open.setIcon(icon1)
        self.t_act_open.setMenuRole(QAction.MenuRole.NoRole)
        self.t_act_analyze = QAction(main_window)
        self.t_act_analyze.setObjectName(u"t_act_analyze")
        icon2 = QIcon()
        icon2.addFile(u":/icon/analyze", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.t_act_analyze.setIcon(icon2)
        self.t_act_analyze.setMenuRole(QAction.MenuRole.NoRole)
        self.t_act_setting = QAction(main_window)
        self.t_act_setting.setObjectName(u"t_act_setting")
        icon3 = QIcon()
        icon3.addFile(u":/icon/settings", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.t_act_setting.setIcon(icon3)
        self.t_act_setting.setMenuRole(QAction.MenuRole.NoRole)
        self.t_act_export = QAction(main_window)
        self.t_act_export.setObjectName(u"t_act_export")
        icon4 = QIcon()
        icon4.addFile(u":/icon/export", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.t_act_export.setIcon(icon4)
        self.t_act_export.setMenuRole(QAction.MenuRole.NoRole)
        self.m_act_open = QAction(main_window)
        self.m_act_open.setObjectName(u"m_act_open")
        self.m_act_open.setIcon(icon1)
        self.m_act_setting = QAction(main_window)
        self.m_act_setting.setObjectName(u"m_act_setting")
        self.m_act_setting.setIcon(icon3)
        self.m_act_analyze = QAction(main_window)
        self.m_act_analyze.setObjectName(u"m_act_analyze")
        self.m_act_analyze.setIcon(icon2)
        self.m_act_export = QAction(main_window)
        self.m_act_export.setObjectName(u"m_act_export")
        self.m_act_export.setIcon(icon4)
        self.m_act_exit = QAction(main_window)
        self.m_act_exit.setObjectName(u"m_act_exit")
        self.m_act_exit.setMenuRole(QAction.MenuRole.QuitRole)
        self.m_act_about = QAction(main_window)
        self.m_act_about.setObjectName(u"m_act_about")
        self.m_act_compute = QAction(main_window)
        self.m_act_compute.setObjectName(u"m_act_compute")
        icon5 = QIcon()
        icon5.addFile(u":/icon/compute", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.m_act_compute.setIcon(icon5)
        self.m_act_compute.setMenuRole(QAction.MenuRole.NoRole)
        self.t_act_compute = QAction(main_window)
        self.t_act_compute.setObjectName(u"t_act_compute")
        self.t_act_compute.setIcon(icon5)
        self.t_act_compute.setMenuRole(QAction.MenuRole.NoRole)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.centralLayout = QVBoxLayout(self.central_widget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.hbl_top = QHBoxLayout()
        self.hbl_top.setObjectName(u"hbl_top")
        self.lb_file_path = QLabel(self.central_widget)
        self.lb_file_path.setObjectName(u"lb_file_path")

        self.hbl_top.addWidget(self.lb_file_path)


        self.centralLayout.addLayout(self.hbl_top)

        self.hbl_video = QHBoxLayout()
        self.hbl_video.setObjectName(u"hbl_video")
        self.gv_video = VideoView(self.central_widget)
        self.gv_video.setObjectName(u"gv_video")

        self.hbl_video.addWidget(self.gv_video)


        self.centralLayout.addLayout(self.hbl_video)

        self.hbl_control = QHBoxLayout()
        self.hbl_control.setObjectName(u"hbl_control")
        self.hbl_control.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.lb_frame = QLabel(self.central_widget)
        self.lb_frame.setObjectName(u"lb_frame")

        self.hbl_control.addWidget(self.lb_frame)

        self.sl_frame = QSlider(self.central_widget)
        self.sl_frame.setObjectName(u"sl_frame")
        self.sl_frame.setMaximum(0)
        self.sl_frame.setOrientation(Qt.Orientation.Horizontal)
        self.sl_frame.setTickPosition(QSlider.TickPosition.NoTicks)

        self.hbl_control.addWidget(self.sl_frame)

        self.lcd_frame = QLCDNumber(self.central_widget)
        self.lcd_frame.setObjectName(u"lcd_frame")
        self.lcd_frame.setDigitCount(9)
        self.lcd_frame.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.hbl_control.addWidget(self.lcd_frame)

        self.btn_play = QPushButton(self.central_widget)
        self.btn_play.setObjectName(u"btn_play")
        icon6 = QIcon()
        icon6.addFile(u":/icon/play", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_play.setIcon(icon6)
        self.btn_play.setIconSize(QSize(20, 20))

        self.hbl_control.addWidget(self.btn_play)

        self.le_filter = QLineEdit(self.central_widget)
        self.le_filter.setObjectName(u"le_filter")

        self.hbl_control.addWidget(self.le_filter)


        self.centralLayout.addLayout(self.hbl_control)

        self.centralLayout.setStretch(1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_about = QMenu(self.menu_bar)
        self.menu_about.setObjectName(u"menu_about")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName(u"status_bar")
        main_window.setStatusBar(self.status_bar)
        self.tool_bar = QToolBar(main_window)
        self.tool_bar.setObjectName(u"tool_bar")
        main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_about.menuAction())
        self.menu_file.addAction(self.m_act_open)
        self.menu_file.addAction(self.m_act_setting)
        self.menu_file.addAction(self.m_act_analyze)
        self.menu_file.addAction(self.m_act_compute)
        self.menu_file.addAction(self.m_act_export)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.m_act_exit)
        self.menu_about.addAction(self.m_act_about)
        self.tool_bar.addAction(self.t_act_open)
        self.tool_bar.addAction(self.t_act_setting)
        self.tool_bar.addAction(self.t_act_analyze)
        self.tool_bar.addAction(self.t_act_compute)
        self.tool_bar.addAction(self.t_act_export)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"QTracker", None))
        self.t_act_open.setText(QCoreApplication.translate("main_window", u"\u6253\u5f00\u6587\u4ef6", None))
        self.t_act_analyze.setText(QCoreApplication.translate("main_window", u"\u7c92\u5b50\u5206\u6790", None))
#if QT_CONFIG(tooltip)
        self.t_act_analyze.setToolTip(QCoreApplication.translate("main_window", u"\u7c92\u5b50\u5206\u6790", None))
#endif // QT_CONFIG(tooltip)
        self.t_act_setting.setText(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.t_act_setting.setToolTip(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.t_act_export.setText(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u89c6\u9891", None))
#if QT_CONFIG(tooltip)
        self.t_act_export.setToolTip(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u89c6\u9891", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_open.setText(QCoreApplication.translate("main_window", u"\u6253\u5f00\u6587\u4ef6", None))
        self.m_act_setting.setText(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.m_act_setting.setToolTip(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_analyze.setText(QCoreApplication.translate("main_window", u"\u7c92\u5b50\u5206\u6790", None))
#if QT_CONFIG(tooltip)
        self.m_act_analyze.setToolTip(QCoreApplication.translate("main_window", u"\u7c92\u5b50\u5206\u6790", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_export.setText(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u89c6\u9891", None))
#if QT_CONFIG(tooltip)
        self.m_act_export.setToolTip(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u89c6\u9891", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_exit.setText(QCoreApplication.translate("main_window", u"\u9000\u51fa", None))
#if QT_CONFIG(tooltip)
        self.m_act_exit.setToolTip(QCoreApplication.translate("main_window", u"\u9000\u51fa", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_about.setText(QCoreApplication.translate("main_window", u"\u5173\u4e8e", None))
#if QT_CONFIG(tooltip)
        self.m_act_about.setToolTip(QCoreApplication.translate("main_window", u"\u5173\u4e8e", None))
#endif // QT_CONFIG(tooltip)
        self.m_act_compute.setText(QCoreApplication.translate("main_window", u"\u7ed3\u679c\u8ba1\u7b97", None))
#if QT_CONFIG(tooltip)
        self.m_act_compute.setToolTip(QCoreApplication.translate("main_window", u"\u7ed3\u679c\u8ba1\u7b97", None))
#endif // QT_CONFIG(tooltip)
        self.t_act_compute.setText(QCoreApplication.translate("main_window", u"\u7ed3\u679c\u8ba1\u7b97", None))
#if QT_CONFIG(tooltip)
        self.t_act_compute.setToolTip(QCoreApplication.translate("main_window", u"\u7ed3\u679c\u8ba1\u7b97", None))
#endif // QT_CONFIG(tooltip)
        self.lb_file_path.setText("")
        self.lb_frame.setText(QCoreApplication.translate("main_window", u"\u5e27", None))
        self.btn_play.setText("")
        self.menu_file.setTitle(QCoreApplication.translate("main_window", u"\u6587\u4ef6", None))
        self.menu_about.setTitle(QCoreApplication.translate("main_window", u"\u5173\u4e8e", None))
        self.tool_bar.setWindowTitle(QCoreApplication.translate("main_window", u"toolBar", None))
    # retranslateUi

