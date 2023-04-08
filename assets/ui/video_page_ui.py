# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_page(object):
    def setupUi(self, page):
        if not page.objectName():
            page.setObjectName(u"page")
        page.resize(796, 514)
        self.verticalLayout = QVBoxLayout(page)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.videoPage = QFrame(page)
        self.videoPage.setObjectName(u"videoPage")
        self.videoPage.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.videoPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftSide = QVBoxLayout()
        self.leftSide.setSpacing(0)
        self.leftSide.setObjectName(u"leftSide")

        self.horizontalLayout.addLayout(self.leftSide)

        self.rightSide = QVBoxLayout()
        self.rightSide.setSpacing(0)
        self.rightSide.setObjectName(u"rightSide")

        self.horizontalLayout.addLayout(self.rightSide)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.videoPage)


        self.retranslateUi(page)

        QMetaObject.connectSlotsByName(page)
    # setupUi

    def retranslateUi(self, page):
        page.setWindowTitle(QCoreApplication.translate("page", u"Form", None))
    # retranslateUi

