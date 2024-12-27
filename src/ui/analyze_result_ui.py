# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analyze_result.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)
import resources_rc

class Ui_dialog_result(object):
    def setupUi(self, dialog_result):
        if not dialog_result.objectName():
            dialog_result.setObjectName(u"dialog_result")
        dialog_result.resize(466, 311)
        icon = QIcon()
        icon.addFile(u":/icon/favicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialog_result.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(dialog_result)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lb_particle = QLabel(dialog_result)
        self.lb_particle.setObjectName(u"lb_particle")

        self.horizontalLayout_3.addWidget(self.lb_particle)

        self.cb_particle = QComboBox(dialog_result)
        self.cb_particle.setObjectName(u"cb_particle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_particle.sizePolicy().hasHeightForWidth())
        self.cb_particle.setSizePolicy(sizePolicy)
        self.cb_particle.setEditable(True)

        self.horizontalLayout_3.addWidget(self.cb_particle)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tv_data = QTableView(dialog_result)
        self.tv_data.setObjectName(u"tv_data")

        self.horizontalLayout_2.addWidget(self.tv_data)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_export = QPushButton(dialog_result)
        self.btn_export.setObjectName(u"btn_export")

        self.horizontalLayout.addWidget(self.btn_export)

        self.btn_close = QPushButton(dialog_result)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(dialog_result)

        QMetaObject.connectSlotsByName(dialog_result)
    # setupUi

    def retranslateUi(self, dialog_result):
        dialog_result.setWindowTitle(QCoreApplication.translate("dialog_result", u"\u5206\u6790\u7ed3\u679c", None))
        self.lb_particle.setText(QCoreApplication.translate("dialog_result", u"\u7c92\u5b50", None))
        self.btn_export.setText(QCoreApplication.translate("dialog_result", u"\u5bfc\u51fa\u6570\u636e", None))
        self.btn_close.setText(QCoreApplication.translate("dialog_result", u"\u5173\u95ed", None))
    # retranslateUi

