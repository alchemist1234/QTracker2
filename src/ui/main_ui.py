# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
import resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(800, 600)
        self.act_open = QAction(main_window)
        self.act_open.setObjectName(u"act_open")
        icon = QIcon()
        icon.addFile(u":/icon/open_file", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.act_open.setIcon(icon)
        self.act_open.setMenuRole(QAction.MenuRole.NoRole)
        self.act_analyze = QAction(main_window)
        self.act_analyze.setObjectName(u"act_analyze")
        icon1 = QIcon()
        icon1.addFile(u":/icon/analyze", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.act_analyze.setIcon(icon1)
        self.act_analyze.setMenuRole(QAction.MenuRole.NoRole)
        self.act_setting = QAction(main_window)
        self.act_setting.setObjectName(u"act_setting")
        icon2 = QIcon()
        icon2.addFile(u":/icon/settings", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.act_setting.setIcon(icon2)
        self.act_setting.setMenuRole(QAction.MenuRole.NoRole)
        self.act_export = QAction(main_window)
        self.act_export.setObjectName(u"act_export")
        icon3 = QIcon()
        icon3.addFile(u":/icon/export", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.act_export.setIcon(icon3)
        self.act_export.setMenuRole(QAction.MenuRole.NoRole)
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
        icon4 = QIcon()
        icon4.addFile(u":/icon/play", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_play.setIcon(icon4)
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
        self.menu = QMenu(self.menu_bar)
        self.menu.setObjectName(u"menu")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName(u"status_bar")
        main_window.setStatusBar(self.status_bar)
        self.tool_bar = QToolBar(main_window)
        self.tool_bar.setObjectName(u"tool_bar")
        main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        self.menu_bar.addAction(self.menu.menuAction())
        self.tool_bar.addAction(self.act_open)
        self.tool_bar.addAction(self.act_setting)
        self.tool_bar.addAction(self.act_analyze)
        self.tool_bar.addAction(self.act_export)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"MainWindow", None))
        self.act_open.setText(QCoreApplication.translate("main_window", u"\u6253\u5f00\u6587\u4ef6", None))
        self.act_analyze.setText(QCoreApplication.translate("main_window", u"\u5206\u6790", None))
#if QT_CONFIG(tooltip)
        self.act_analyze.setToolTip(QCoreApplication.translate("main_window", u"\u5206\u6790", None))
#endif // QT_CONFIG(tooltip)
        self.act_setting.setText(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.act_setting.setToolTip(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.act_export.setText(QCoreApplication.translate("main_window", u"\u5bfc\u51fa", None))
#if QT_CONFIG(tooltip)
        self.act_export.setToolTip(QCoreApplication.translate("main_window", u"\u5bfc\u51fa", None))
#endif // QT_CONFIG(tooltip)
        self.lb_file_path.setText("")
        self.lb_frame.setText(QCoreApplication.translate("main_window", u"\u5e27", None))
        self.btn_play.setText("")
        self.menu.setTitle(QCoreApplication.translate("main_window", u"\u6587\u4ef6", None))
        self.tool_bar.setWindowTitle(QCoreApplication.translate("main_window", u"toolBar", None))
    # retranslateUi

