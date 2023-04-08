# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'topbar.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_contentTopBg(object):
    def setupUi(self, contentTopBg):
        if not contentTopBg.objectName():
            contentTopBg.setObjectName(u"contentTopBg")
        contentTopBg.resize(738, 50)
        contentTopBg.setMinimumSize(QSize(0, 50))
        contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(contentTopBg)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.title = QLabel(contentTopBg)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.title)

        self.horizontalSpacer = QSpacerItem(510, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.topBar = QFrame(contentTopBg)
        self.topBar.setObjectName(u"topBar")
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.tbBtnMinimize = QPushButton(self.topBar)
        self.tbBtnMinimize.setObjectName(u"tbBtnMinimize")
        self.tbBtnMinimize.setMinimumSize(QSize(40, 35))
        self.tbBtnMinimize.setMaximumSize(QSize(40, 35))

        self.topBarLayout.addWidget(self.tbBtnMinimize)

        self.tbBtnMaximize = QPushButton(self.topBar)
        self.tbBtnMaximize.setObjectName(u"tbBtnMaximize")
        self.tbBtnMaximize.setMinimumSize(QSize(40, 35))
        self.tbBtnMaximize.setMaximumSize(QSize(40, 35))

        self.topBarLayout.addWidget(self.tbBtnMaximize)

        self.tbBtnClose = QPushButton(self.topBar)
        self.tbBtnClose.setObjectName(u"tbBtnClose")
        self.tbBtnClose.setMinimumSize(QSize(40, 35))
        self.tbBtnClose.setMaximumSize(QSize(40, 35))

        self.topBarLayout.addWidget(self.tbBtnClose)


        self.horizontalLayout.addWidget(self.topBar)


        self.retranslateUi(contentTopBg)

        QMetaObject.connectSlotsByName(contentTopBg)
    # setupUi

    def retranslateUi(self, contentTopBg):
        contentTopBg.setWindowTitle(QCoreApplication.translate("contentTopBg", u"Form", None))
        self.title.setText(QCoreApplication.translate("contentTopBg", u"MicroDoc \u2014\u2014 \u610f\u8bc6\u969c\u788d\u8f85\u52a9\u8bca\u65ad\u7cfb\u7edf", None))
        self.tbBtnMinimize.setText("")
        self.tbBtnMaximize.setText("")
        self.tbBtnClose.setText("")
    # retranslateUi

