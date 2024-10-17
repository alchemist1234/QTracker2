# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_group_editor.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lw = QListWidget(Dialog)
        self.lw.setObjectName(u"lw")
        self.lw.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.lw.setMovement(QListView.Movement.Snap)
        self.lw.setGridSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.lw)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_add = QPushButton(Dialog)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(Dialog)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.btn_random = QPushButton(Dialog)
        self.btn_random.setObjectName(u"btn_random")

        self.verticalLayout.addWidget(self.btn_random)

        self.btn_move_up = QPushButton(Dialog)
        self.btn_move_up.setObjectName(u"btn_move_up")

        self.verticalLayout.addWidget(self.btn_move_up)

        self.btn_move_down = QPushButton(Dialog)
        self.btn_move_down.setObjectName(u"btn_move_down")

        self.verticalLayout.addWidget(self.btn_move_down)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_ok = QPushButton(Dialog)
        self.btn_ok.setObjectName(u"btn_ok")

        self.verticalLayout.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(Dialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.verticalLayout.addWidget(self.btn_cancel)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.btn_add.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u989c\u8272", None))
        self.btn_delete.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664\u989c\u8272", None))
        self.btn_random.setText(QCoreApplication.translate("Dialog", u"\u968f\u673a\u989c\u8272", None))
        self.btn_move_up.setText(QCoreApplication.translate("Dialog", u"\u4e0a\u79fb\u4e00\u4f4d", None))
        self.btn_move_down.setText(QCoreApplication.translate("Dialog", u"\u4e0b\u79fb\u4e00\u4f4d", None))
        self.btn_ok.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

