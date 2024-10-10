# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_btn_grp.ui'
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
from PySide6.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_wid_button_group(object):
    def setupUi(self, wid_button_group):
        if not wid_button_group.objectName():
            wid_button_group.setObjectName(u"wid_button_group")
        wid_button_group.resize(172, 258)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wid_button_group.sizePolicy().hasHeightForWidth())
        wid_button_group.setSizePolicy(sizePolicy)
        wid_button_group.setMinimumSize(QSize(20, 0))
        wid_button_group.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.vboxLayout = QVBoxLayout(wid_button_group)
        self.vboxLayout.setSpacing(2)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.vboxLayout.setContentsMargins(4, 4, 4, 4)
        self.btn_move = QPushButton(wid_button_group)
        self.btn_move.setObjectName(u"btn_move")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_move.sizePolicy().hasHeightForWidth())
        self.btn_move.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u":/icon/cursor", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_move.setIcon(icon)
        self.btn_move.setIconSize(QSize(16, 20))
        self.btn_move.setCheckable(True)
        self.btn_move.setChecked(True)
        self.btn_move.setAutoExclusive(True)

        self.vboxLayout.addWidget(self.btn_move)

        self.btn_add = QPushButton(wid_button_group)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy1.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy1)
        icon1 = QIcon()
        icon1.addFile(u":/icon/add", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_add.setIcon(icon1)
        self.btn_add.setIconSize(QSize(16, 20))
        self.btn_add.setCheckable(True)
        self.btn_add.setAutoExclusive(True)

        self.vboxLayout.addWidget(self.btn_add)

        self.btn_crop = QPushButton(wid_button_group)
        self.btn_crop.setObjectName(u"btn_crop")
        sizePolicy1.setHeightForWidth(self.btn_crop.sizePolicy().hasHeightForWidth())
        self.btn_crop.setSizePolicy(sizePolicy1)
        icon2 = QIcon()
        icon2.addFile(u":/icon/crop", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_crop.setIcon(icon2)
        self.btn_crop.setIconSize(QSize(16, 20))
        self.btn_crop.setCheckable(True)
        self.btn_crop.setAutoExclusive(True)

        self.vboxLayout.addWidget(self.btn_crop)

        self.btn_combine = QPushButton(wid_button_group)
        self.btn_combine.setObjectName(u"btn_combine")
        sizePolicy1.setHeightForWidth(self.btn_combine.sizePolicy().hasHeightForWidth())
        self.btn_combine.setSizePolicy(sizePolicy1)
        icon3 = QIcon()
        icon3.addFile(u":/icon/combine", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_combine.setIcon(icon3)
        self.btn_combine.setIconSize(QSize(16, 20))
        self.btn_combine.setCheckable(True)
        self.btn_combine.setAutoExclusive(True)

        self.vboxLayout.addWidget(self.btn_combine)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.vboxLayout.addItem(self.verticalSpacer)

        self.btn_show_particle = QPushButton(wid_button_group)
        self.btn_show_particle.setObjectName(u"btn_show_particle")
        sizePolicy1.setHeightForWidth(self.btn_show_particle.sizePolicy().hasHeightForWidth())
        self.btn_show_particle.setSizePolicy(sizePolicy1)
        icon4 = QIcon()
        icon4.addFile(u":/icon/bubble", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_show_particle.setIcon(icon4)
        self.btn_show_particle.setIconSize(QSize(16, 20))
        self.btn_show_particle.setCheckable(True)

        self.vboxLayout.addWidget(self.btn_show_particle)

        self.btn_show_mark = QPushButton(wid_button_group)
        self.btn_show_mark.setObjectName(u"btn_show_mark")
        sizePolicy1.setHeightForWidth(self.btn_show_mark.sizePolicy().hasHeightForWidth())
        self.btn_show_mark.setSizePolicy(sizePolicy1)
        icon5 = QIcon()
        icon5.addFile(u":/icon/numeric", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_show_mark.setIcon(icon5)
        self.btn_show_mark.setIconSize(QSize(16, 20))
        self.btn_show_mark.setCheckable(True)

        self.vboxLayout.addWidget(self.btn_show_mark)

        self.btn_show_trajectory = QPushButton(wid_button_group)
        self.btn_show_trajectory.setObjectName(u"btn_show_trajectory")
        sizePolicy1.setHeightForWidth(self.btn_show_trajectory.sizePolicy().hasHeightForWidth())
        self.btn_show_trajectory.setSizePolicy(sizePolicy1)
        icon6 = QIcon()
        icon6.addFile(u":/icon/ray", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_show_trajectory.setIcon(icon6)
        self.btn_show_trajectory.setIconSize(QSize(16, 20))
        self.btn_show_trajectory.setCheckable(True)

        self.vboxLayout.addWidget(self.btn_show_trajectory)


        self.retranslateUi(wid_button_group)

        QMetaObject.connectSlotsByName(wid_button_group)
    # setupUi

    def retranslateUi(self, wid_button_group):
        wid_button_group.setWindowTitle("")
        self.btn_move.setText("")
        self.btn_add.setText("")
        self.btn_crop.setText("")
        self.btn_combine.setText("")
        self.btn_show_particle.setText("")
        self.btn_show_mark.setText("")
        self.btn_show_trajectory.setText("")
    # retranslateUi

