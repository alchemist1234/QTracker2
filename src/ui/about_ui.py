# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_dialog_about(object):
    def setupUi(self, dialog_about):
        if not dialog_about.objectName():
            dialog_about.setObjectName(u"dialog_about")
        dialog_about.resize(395, 360)
        self.verticalLayout = QVBoxLayout(dialog_about)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lb_favicon = QLabel(dialog_about)
        self.lb_favicon.setObjectName(u"lb_favicon")
        self.lb_favicon.setTextFormat(Qt.TextFormat.AutoText)
        self.lb_favicon.setPixmap(QPixmap(u":/icon/favicon"))
        self.lb_favicon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.lb_favicon)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lb_github = QLabel(dialog_about)
        self.lb_github.setObjectName(u"lb_github")

        self.horizontalLayout_2.addWidget(self.lb_github)

        self.lb_github_url = QLabel(dialog_about)
        self.lb_github_url.setObjectName(u"lb_github_url")
        self.lb_github_url.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lb_github_url.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.lb_github_url)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.lb_gitee = QLabel(dialog_about)
        self.lb_gitee.setObjectName(u"lb_gitee")

        self.horizontalLayout_4.addWidget(self.lb_gitee)

        self.lb_gitee_url = QLabel(dialog_about)
        self.lb_gitee_url.setObjectName(u"lb_gitee_url")
        self.lb_gitee_url.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lb_gitee_url.setStyleSheet(u"QLabel {color: blue; text-decoration: underline}")
        self.lb_gitee_url.setOpenExternalLinks(True)

        self.horizontalLayout_4.addWidget(self.lb_gitee_url)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.lb_email = QLabel(dialog_about)
        self.lb_email.setObjectName(u"lb_email")

        self.horizontalLayout_3.addWidget(self.lb_email)

        self.lb_email_addr = QLabel(dialog_about)
        self.lb_email_addr.setObjectName(u"lb_email_addr")

        self.horizontalLayout_3.addWidget(self.lb_email_addr)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(dialog_about)

        QMetaObject.connectSlotsByName(dialog_about)
    # setupUi

    def retranslateUi(self, dialog_about):
        dialog_about.setWindowTitle(QCoreApplication.translate("dialog_about", u"\u5173\u4e8e", None))
        self.lb_favicon.setText("")
        self.lb_github.setText(QCoreApplication.translate("dialog_about", u"Github: ", None))
        self.lb_github_url.setText(QCoreApplication.translate("dialog_about", u"<a style='color:blue' href=https://github.com/alchemist1234/QTracker>https://github.com/alchemist1234/QTracker", None))
        self.lb_gitee.setText(QCoreApplication.translate("dialog_about", u"Gitee: ", None))
        self.lb_gitee_url.setText(QCoreApplication.translate("dialog_about", u"<a style='color:blue' href=https://gitee.com/celoran/QTracker>https://gitee.com/celoran/QTracker", None))
        self.lb_email.setText(QCoreApplication.translate("dialog_about", u"E-mail: ", None))
        self.lb_email_addr.setText(QCoreApplication.translate("dialog_about", u"alchemist1234@163.com", None))
    # retranslateUi

