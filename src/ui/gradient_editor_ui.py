# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gradient_editor.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from src.view.custom_widget import GradientLabel

class Ui_dialog_gradient_editor(object):
    def setupUi(self, dialog_gradient_editor):
        if not dialog_gradient_editor.objectName():
            dialog_gradient_editor.setObjectName(u"dialog_gradient_editor")
        dialog_gradient_editor.resize(400, 300)
        self.horizontalLayout_2 = QHBoxLayout(dialog_gradient_editor)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lb_gradient_display = GradientLabel(dialog_gradient_editor)
        self.lb_gradient_display.setObjectName(u"lb_gradient_display")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_gradient_display.sizePolicy().hasHeightForWidth())
        self.lb_gradient_display.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.lb_gradient_display)

        self.lw_colors = QListWidget(dialog_gradient_editor)
        self.lw_colors.setObjectName(u"lw_colors")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lw_colors.sizePolicy().hasHeightForWidth())
        self.lw_colors.setSizePolicy(sizePolicy1)
        self.lw_colors.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.lw_colors.setMovement(QListView.Movement.Snap)
        self.lw_colors.setGridSize(QSize(100, 32))

        self.verticalLayout_2.addWidget(self.lw_colors)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_add = QPushButton(dialog_gradient_editor)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(dialog_gradient_editor)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_ok = QPushButton(dialog_gradient_editor)
        self.btn_ok.setObjectName(u"btn_ok")

        self.verticalLayout.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(dialog_gradient_editor)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.verticalLayout.addWidget(self.btn_cancel)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(dialog_gradient_editor)

        QMetaObject.connectSlotsByName(dialog_gradient_editor)
    # setupUi

    def retranslateUi(self, dialog_gradient_editor):
        dialog_gradient_editor.setWindowTitle(QCoreApplication.translate("dialog_gradient_editor", u"\u989c\u8272\u8bbe\u7f6e", None))
        self.lb_gradient_display.setText("")
        self.btn_add.setText(QCoreApplication.translate("dialog_gradient_editor", u"\u6dfb\u52a0\u989c\u8272", None))
        self.btn_delete.setText(QCoreApplication.translate("dialog_gradient_editor", u"\u5220\u9664\u989c\u8272", None))
        self.btn_ok.setText(QCoreApplication.translate("dialog_gradient_editor", u"\u786e\u5b9a", None))
        self.btn_cancel.setText(QCoreApplication.translate("dialog_gradient_editor", u"\u53d6\u6d88", None))
    # retranslateUi

