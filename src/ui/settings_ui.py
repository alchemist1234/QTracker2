# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(485, 512)
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_analyze = QWidget()
        self.tab_analyze.setObjectName(u"tab_analyze")
        self.verticalLayout1 = QVBoxLayout(self.tab_analyze)
        self.verticalLayout1.setObjectName(u"verticalLayout1")
        self.groupBox = QGroupBox(self.tab_analyze)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.verticalLayout2 = QVBoxLayout(self.groupBox)
        self.verticalLayout2.setSpacing(4)
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.verticalLayout2.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lb_median_blur = QLabel(self.groupBox)
        self.lb_median_blur.setObjectName(u"lb_median_blur")

        self.horizontalLayout.addWidget(self.lb_median_blur)

        self.spb_median_blur = QSpinBox(self.groupBox)
        self.spb_median_blur.setObjectName(u"spb_median_blur")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spb_median_blur.sizePolicy().hasHeightForWidth())
        self.spb_median_blur.setSizePolicy(sizePolicy)
        self.spb_median_blur.setFrame(False)

        self.horizontalLayout.addWidget(self.spb_median_blur)

        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lb_opening_size = QLabel(self.groupBox)
        self.lb_opening_size.setObjectName(u"lb_opening_size")

        self.horizontalLayout.addWidget(self.lb_opening_size)

        self.spb_opening_size = QSpinBox(self.groupBox)
        self.spb_opening_size.setObjectName(u"spb_opening_size")
        sizePolicy.setHeightForWidth(self.spb_opening_size.sizePolicy().hasHeightForWidth())
        self.spb_opening_size.setSizePolicy(sizePolicy)
        self.spb_opening_size.setFrame(False)

        self.horizontalLayout.addWidget(self.spb_opening_size)


        self.verticalLayout2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lb_gaussian_blur = QLabel(self.groupBox)
        self.lb_gaussian_blur.setObjectName(u"lb_gaussian_blur")

        self.horizontalLayout_2.addWidget(self.lb_gaussian_blur)

        self.spb_gaussian_blur = QSpinBox(self.groupBox)
        self.spb_gaussian_blur.setObjectName(u"spb_gaussian_blur")
        sizePolicy.setHeightForWidth(self.spb_gaussian_blur.sizePolicy().hasHeightForWidth())
        self.spb_gaussian_blur.setSizePolicy(sizePolicy)
        self.spb_gaussian_blur.setFrame(False)

        self.horizontalLayout_2.addWidget(self.spb_gaussian_blur)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lb_closing_size = QLabel(self.groupBox)
        self.lb_closing_size.setObjectName(u"lb_closing_size")

        self.horizontalLayout_2.addWidget(self.lb_closing_size)

        self.spb_closing_size = QSpinBox(self.groupBox)
        self.spb_closing_size.setObjectName(u"spb_closing_size")
        sizePolicy.setHeightForWidth(self.spb_closing_size.sizePolicy().hasHeightForWidth())
        self.spb_closing_size.setSizePolicy(sizePolicy)
        self.spb_closing_size.setFrame(False)

        self.horizontalLayout_2.addWidget(self.spb_closing_size)


        self.verticalLayout2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.chb_apply_hist_eq = QCheckBox(self.groupBox)
        self.chb_apply_hist_eq.setObjectName(u"chb_apply_hist_eq")

        self.horizontalLayout_3.addWidget(self.chb_apply_hist_eq)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.lb_adaptive_hist_eq = QLabel(self.groupBox)
        self.lb_adaptive_hist_eq.setObjectName(u"lb_adaptive_hist_eq")

        self.horizontalLayout_3.addWidget(self.lb_adaptive_hist_eq)

        self.spb_adaptive_hist_eq = QSpinBox(self.groupBox)
        self.spb_adaptive_hist_eq.setObjectName(u"spb_adaptive_hist_eq")
        sizePolicy.setHeightForWidth(self.spb_adaptive_hist_eq.sizePolicy().hasHeightForWidth())
        self.spb_adaptive_hist_eq.setSizePolicy(sizePolicy)
        self.spb_adaptive_hist_eq.setFrame(False)

        self.horizontalLayout_3.addWidget(self.spb_adaptive_hist_eq)


        self.verticalLayout2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lb_bilateral_filter = QLabel(self.groupBox)
        self.lb_bilateral_filter.setObjectName(u"lb_bilateral_filter")

        self.horizontalLayout_4.addWidget(self.lb_bilateral_filter)

        self.spb_bilateral_filter_size = QSpinBox(self.groupBox)
        self.spb_bilateral_filter_size.setObjectName(u"spb_bilateral_filter_size")
        sizePolicy.setHeightForWidth(self.spb_bilateral_filter_size.sizePolicy().hasHeightForWidth())
        self.spb_bilateral_filter_size.setSizePolicy(sizePolicy)
        self.spb_bilateral_filter_size.setFrame(False)

        self.horizontalLayout_4.addWidget(self.spb_bilateral_filter_size)

        self.spb_bilateral_filter_color = QSpinBox(self.groupBox)
        self.spb_bilateral_filter_color.setObjectName(u"spb_bilateral_filter_color")
        sizePolicy.setHeightForWidth(self.spb_bilateral_filter_color.sizePolicy().hasHeightForWidth())
        self.spb_bilateral_filter_color.setSizePolicy(sizePolicy)
        self.spb_bilateral_filter_color.setFrame(False)

        self.horizontalLayout_4.addWidget(self.spb_bilateral_filter_color)

        self.spb_bilateral_filter_space = QSpinBox(self.groupBox)
        self.spb_bilateral_filter_space.setObjectName(u"spb_bilateral_filter_space")
        sizePolicy.setHeightForWidth(self.spb_bilateral_filter_space.sizePolicy().hasHeightForWidth())
        self.spb_bilateral_filter_space.setSizePolicy(sizePolicy)
        self.spb_bilateral_filter_space.setFrame(False)

        self.horizontalLayout_4.addWidget(self.spb_bilateral_filter_space)


        self.verticalLayout2.addLayout(self.horizontalLayout_4)


        self.verticalLayout1.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_analyze)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout3.setSpacing(4)
        self.verticalLayout3.setObjectName(u"verticalLayout3")
        self.verticalLayout3.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lb_search_radius = QLabel(self.groupBox_2)
        self.lb_search_radius.setObjectName(u"lb_search_radius")

        self.horizontalLayout_5.addWidget(self.lb_search_radius)

        self.spb_search_radius = QSpinBox(self.groupBox_2)
        self.spb_search_radius.setObjectName(u"spb_search_radius")
        sizePolicy.setHeightForWidth(self.spb_search_radius.sizePolicy().hasHeightForWidth())
        self.spb_search_radius.setSizePolicy(sizePolicy)
        self.spb_search_radius.setFrame(False)

        self.horizontalLayout_5.addWidget(self.spb_search_radius)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.lb_min_detect_area = QLabel(self.groupBox_2)
        self.lb_min_detect_area.setObjectName(u"lb_min_detect_area")

        self.horizontalLayout_5.addWidget(self.lb_min_detect_area)

        self.spb_min_detect_area = QSpinBox(self.groupBox_2)
        self.spb_min_detect_area.setObjectName(u"spb_min_detect_area")
        sizePolicy.setHeightForWidth(self.spb_min_detect_area.sizePolicy().hasHeightForWidth())
        self.spb_min_detect_area.setSizePolicy(sizePolicy)
        self.spb_min_detect_area.setFrame(False)

        self.horizontalLayout_5.addWidget(self.spb_min_detect_area)


        self.verticalLayout3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lb_memory_frames = QLabel(self.groupBox_2)
        self.lb_memory_frames.setObjectName(u"lb_memory_frames")

        self.horizontalLayout_6.addWidget(self.lb_memory_frames)

        self.spb_memory_frames = QSpinBox(self.groupBox_2)
        self.spb_memory_frames.setObjectName(u"spb_memory_frames")
        sizePolicy.setHeightForWidth(self.spb_memory_frames.sizePolicy().hasHeightForWidth())
        self.spb_memory_frames.setSizePolicy(sizePolicy)
        self.spb_memory_frames.setFrame(False)
        self.spb_memory_frames.setAccelerated(True)

        self.horizontalLayout_6.addWidget(self.spb_memory_frames)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.lb_max_detect_area = QLabel(self.groupBox_2)
        self.lb_max_detect_area.setObjectName(u"lb_max_detect_area")

        self.horizontalLayout_6.addWidget(self.lb_max_detect_area)

        self.spb_max_detect_area = QSpinBox(self.groupBox_2)
        self.spb_max_detect_area.setObjectName(u"spb_max_detect_area")
        sizePolicy.setHeightForWidth(self.spb_max_detect_area.sizePolicy().hasHeightForWidth())
        self.spb_max_detect_area.setSizePolicy(sizePolicy)
        self.spb_max_detect_area.setFrame(False)

        self.horizontalLayout_6.addWidget(self.spb_max_detect_area)


        self.verticalLayout3.addLayout(self.horizontalLayout_6)


        self.verticalLayout1.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.tab_analyze)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout4.setSpacing(4)
        self.verticalLayout4.setObjectName(u"verticalLayout4")
        self.verticalLayout4.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lb_threshold = QLabel(self.groupBox_3)
        self.lb_threshold.setObjectName(u"lb_threshold")

        self.horizontalLayout_7.addWidget(self.lb_threshold)

        self.spb_threshold = QSpinBox(self.groupBox_3)
        self.spb_threshold.setObjectName(u"spb_threshold")
        sizePolicy.setHeightForWidth(self.spb_threshold.sizePolicy().hasHeightForWidth())
        self.spb_threshold.setSizePolicy(sizePolicy)
        self.spb_threshold.setWrapping(False)
        self.spb_threshold.setFrame(False)

        self.horizontalLayout_7.addWidget(self.spb_threshold)

        self.lb_derivative_order = QLabel(self.groupBox_3)
        self.lb_derivative_order.setObjectName(u"lb_derivative_order")

        self.horizontalLayout_7.addWidget(self.lb_derivative_order)

        self.spb_derivative_order = QSpinBox(self.groupBox_3)
        self.spb_derivative_order.setObjectName(u"spb_derivative_order")
        sizePolicy.setHeightForWidth(self.spb_derivative_order.sizePolicy().hasHeightForWidth())
        self.spb_derivative_order.setSizePolicy(sizePolicy)
        self.spb_derivative_order.setFrame(False)

        self.horizontalLayout_7.addWidget(self.spb_derivative_order)

        self.lb_kernel_size = QLabel(self.groupBox_3)
        self.lb_kernel_size.setObjectName(u"lb_kernel_size")

        self.horizontalLayout_7.addWidget(self.lb_kernel_size)

        self.spb_kernel_size = QSpinBox(self.groupBox_3)
        self.spb_kernel_size.setObjectName(u"spb_kernel_size")
        sizePolicy.setHeightForWidth(self.spb_kernel_size.sizePolicy().hasHeightForWidth())
        self.spb_kernel_size.setSizePolicy(sizePolicy)
        self.spb_kernel_size.setFrame(False)

        self.horizontalLayout_7.addWidget(self.spb_kernel_size)


        self.verticalLayout4.addLayout(self.horizontalLayout_7)


        self.verticalLayout1.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab_analyze)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout5.setSpacing(4)
        self.verticalLayout5.setObjectName(u"verticalLayout5")
        self.verticalLayout5.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.chb_split_particles = QCheckBox(self.groupBox_4)
        self.chb_split_particles.setObjectName(u"chb_split_particles")

        self.horizontalLayout_8.addWidget(self.chb_split_particles)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.lb_particle_radius_for_split = QLabel(self.groupBox_4)
        self.lb_particle_radius_for_split.setObjectName(u"lb_particle_radius_for_split")

        self.horizontalLayout_8.addWidget(self.lb_particle_radius_for_split)

        self.spb_particle_radius_for_split = QSpinBox(self.groupBox_4)
        self.spb_particle_radius_for_split.setObjectName(u"spb_particle_radius_for_split")
        sizePolicy.setHeightForWidth(self.spb_particle_radius_for_split.sizePolicy().hasHeightForWidth())
        self.spb_particle_radius_for_split.setSizePolicy(sizePolicy)
        self.spb_particle_radius_for_split.setFrame(False)

        self.horizontalLayout_8.addWidget(self.spb_particle_radius_for_split)


        self.verticalLayout5.addLayout(self.horizontalLayout_8)


        self.verticalLayout1.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_analyze)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout6 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout6.setSpacing(4)
        self.verticalLayout6.setObjectName(u"verticalLayout6")
        self.verticalLayout6.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.chb_fit_to_screen = QCheckBox(self.groupBox_5)
        self.chb_fit_to_screen.setObjectName(u"chb_fit_to_screen")

        self.horizontalLayout_9.addWidget(self.chb_fit_to_screen)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.lb_skip_frames = QLabel(self.groupBox_5)
        self.lb_skip_frames.setObjectName(u"lb_skip_frames")

        self.horizontalLayout_9.addWidget(self.lb_skip_frames)

        self.spb_skip_frames = QSpinBox(self.groupBox_5)
        self.spb_skip_frames.setObjectName(u"spb_skip_frames")
        sizePolicy.setHeightForWidth(self.spb_skip_frames.sizePolicy().hasHeightForWidth())
        self.spb_skip_frames.setSizePolicy(sizePolicy)
        self.spb_skip_frames.setFrame(False)

        self.horizontalLayout_9.addWidget(self.spb_skip_frames)


        self.verticalLayout6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lb_from_frames = QLabel(self.groupBox_5)
        self.lb_from_frames.setObjectName(u"lb_from_frames")

        self.horizontalLayout_10.addWidget(self.lb_from_frames)

        self.spb_from_frames = QSpinBox(self.groupBox_5)
        self.spb_from_frames.setObjectName(u"spb_from_frames")
        sizePolicy.setHeightForWidth(self.spb_from_frames.sizePolicy().hasHeightForWidth())
        self.spb_from_frames.setSizePolicy(sizePolicy)
        self.spb_from_frames.setFrame(False)

        self.horizontalLayout_10.addWidget(self.spb_from_frames)

        self.lb_to_frames = QLabel(self.groupBox_5)
        self.lb_to_frames.setObjectName(u"lb_to_frames")

        self.horizontalLayout_10.addWidget(self.lb_to_frames)

        self.spb_to_frames = QSpinBox(self.groupBox_5)
        self.spb_to_frames.setObjectName(u"spb_to_frames")
        sizePolicy.setHeightForWidth(self.spb_to_frames.sizePolicy().hasHeightForWidth())
        self.spb_to_frames.setSizePolicy(sizePolicy)
        self.spb_to_frames.setFrame(False)

        self.horizontalLayout_10.addWidget(self.spb_to_frames)


        self.verticalLayout6.addLayout(self.horizontalLayout_10)


        self.verticalLayout1.addWidget(self.groupBox_5)

        self.verticalLayout1.setStretch(0, 4)
        self.verticalLayout1.setStretch(1, 2)
        self.verticalLayout1.setStretch(2, 1)
        self.verticalLayout1.setStretch(3, 1)
        self.verticalLayout1.setStretch(4, 2)
        self.tabWidget.addTab(self.tab_analyze, "")
        self.tab_display = QWidget()
        self.tab_display.setObjectName(u"tab_display")
        self.verticalLayout7 = QVBoxLayout(self.tab_display)
        self.verticalLayout7.setObjectName(u"verticalLayout7")
        self.tabWidget.addTab(self.tab_display, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle("")
        self.lb_median_blur.setText(QCoreApplication.translate("Dialog", u"\u4e2d\u503c\u6a21\u7cca", None))
        self.lb_opening_size.setText(QCoreApplication.translate("Dialog", u"\u5f00\u8fd0\u7b97", None))
        self.lb_gaussian_blur.setText(QCoreApplication.translate("Dialog", u"\u9ad8\u65af\u6a21\u7cca", None))
        self.lb_closing_size.setText(QCoreApplication.translate("Dialog", u"\u95ed\u8fd0\u7b97", None))
        self.chb_apply_hist_eq.setText(QCoreApplication.translate("Dialog", u"\u76f4\u65b9\u56fe\u5747\u8861\u5316", None))
        self.lb_adaptive_hist_eq.setText(QCoreApplication.translate("Dialog", u"\u5747\u8861\u5316\u6b21\u6570", None))
        self.lb_bilateral_filter.setText(QCoreApplication.translate("Dialog", u"\u53cc\u8fb9\u6ee4\u6ce2(size/color/space)", None))
        self.groupBox_2.setTitle("")
        self.lb_search_radius.setText(QCoreApplication.translate("Dialog", u"\u641c\u7d22\u534a\u5f84", None))
        self.lb_min_detect_area.setText(QCoreApplication.translate("Dialog", u"\u6700\u5c0f\u68c0\u6d4b\u9762\u79ef", None))
        self.lb_memory_frames.setText(QCoreApplication.translate("Dialog", u"\u8bb0\u5fc6\u5e27\u6570", None))
        self.lb_max_detect_area.setText(QCoreApplication.translate("Dialog", u"\u6700\u5927\u68c0\u6d4b\u9762\u79ef", None))
        self.groupBox_3.setTitle("")
        self.lb_threshold.setText(QCoreApplication.translate("Dialog", u"\u9608\u503c", None))
        self.lb_derivative_order.setText(QCoreApplication.translate("Dialog", u"Sobel\u5dee\u5206\u9636\u6570", None))
        self.lb_kernel_size.setText(QCoreApplication.translate("Dialog", u"Sobel\u6838\u5927\u5c0f", None))
        self.groupBox_4.setTitle("")
        self.chb_split_particles.setText(QCoreApplication.translate("Dialog", u"\u5206\u5272\u7c92\u5b50", None))
        self.lb_particle_radius_for_split.setText(QCoreApplication.translate("Dialog", u"\u5206\u5272\u7c92\u5b50\u5c3a\u5bf8", None))
        self.groupBox_5.setTitle("")
        self.chb_fit_to_screen.setText(QCoreApplication.translate("Dialog", u"\u9002\u5e94\u5c4f\u5e55", None))
        self.lb_skip_frames.setText(QCoreApplication.translate("Dialog", u"\u8df3\u8fc7\u5e27", None))
        self.lb_from_frames.setText(QCoreApplication.translate("Dialog", u"\u8d77\u59cb\u5e27", None))
        self.lb_to_frames.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u675f\u5e27", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analyze), QCoreApplication.translate("Dialog", u"\u5206\u6790", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_display), QCoreApplication.translate("Dialog", u"\u663e\u793a", None))
    # retranslateUi

