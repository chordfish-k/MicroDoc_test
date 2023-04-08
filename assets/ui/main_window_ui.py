# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(772, 600)
        MainWindow.setStyleSheet(u"")
        self.bgApp = QWidget(MainWindow)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.bgApp)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sideBar = QVBoxLayout()
        self.sideBar.setSpacing(0)
        self.sideBar.setObjectName(u"sideBar")

        self.horizontalLayout_2.addLayout(self.sideBar)

        self.content = QVBoxLayout()
        self.content.setSpacing(0)
        self.content.setObjectName(u"content")
        self.topBar = QHBoxLayout()
        self.topBar.setSpacing(0)
        self.topBar.setObjectName(u"topBar")

        self.content.addLayout(self.topBar)

        self.main = QVBoxLayout()
        self.main.setSpacing(0)
        self.main.setObjectName(u"main")

        self.content.addLayout(self.main)


        self.horizontalLayout_2.addLayout(self.content)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.bgApp)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MicroDoc", None))
    # retranslateUi

