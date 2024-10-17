# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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

class Ui_dialog_color_editor(object):
    def setupUi(self, dialog_color_editor):
        if not dialog_color_editor.objectName():
            dialog_color_editor.setObjectName(u"dialog_color_editor")
        dialog_color_editor.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(dialog_color_editor)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lw_colors = QListWidget(dialog_color_editor)
        self.lw_colors.setObjectName(u"lw_colors")
        self.lw_colors.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.lw_colors.setMovement(QListView.Movement.Snap)
        self.lw_colors.setGridSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.lw_colors)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_add = QPushButton(dialog_color_editor)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(dialog_color_editor)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.btn_random = QPushButton(dialog_color_editor)
        self.btn_random.setObjectName(u"btn_random")

        self.verticalLayout.addWidget(self.btn_random)

        self.btn_move_up = QPushButton(dialog_color_editor)
        self.btn_move_up.setObjectName(u"btn_move_up")

        self.verticalLayout.addWidget(self.btn_move_up)

        self.btn_move_down = QPushButton(dialog_color_editor)
        self.btn_move_down.setObjectName(u"btn_move_down")

        self.verticalLayout.addWidget(self.btn_move_down)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_ok = QPushButton(dialog_color_editor)
        self.btn_ok.setObjectName(u"btn_ok")

        self.verticalLayout.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(dialog_color_editor)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.verticalLayout.addWidget(self.btn_cancel)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(dialog_color_editor)

        QMetaObject.connectSlotsByName(dialog_color_editor)
    # setupUi

    def retranslateUi(self, dialog_color_editor):
        dialog_color_editor.setWindowTitle(QCoreApplication.translate("dialog_color_editor", u"Dialog", None))
        self.btn_add.setText(QCoreApplication.translate("dialog_color_editor", u"\u6dfb\u52a0\u989c\u8272", None))
        self.btn_delete.setText(QCoreApplication.translate("dialog_color_editor", u"\u5220\u9664\u989c\u8272", None))
        self.btn_random.setText(QCoreApplication.translate("dialog_color_editor", u"\u968f\u673a\u989c\u8272", None))
        self.btn_move_up.setText(QCoreApplication.translate("dialog_color_editor", u"\u4e0a\u79fb\u4e00\u4f4d", None))
        self.btn_move_down.setText(QCoreApplication.translate("dialog_color_editor", u"\u4e0b\u79fb\u4e00\u4f4d", None))
        self.btn_ok.setText(QCoreApplication.translate("dialog_color_editor", u"\u786e\u5b9a", None))
        self.btn_cancel.setText(QCoreApplication.translate("dialog_color_editor", u"\u53d6\u6d88", None))
    # retranslateUi

