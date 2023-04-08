# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sidebar.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_leftMenuBg(object):
    def setupUi(self, leftMenuBg):
        if not leftMenuBg.objectName():
            leftMenuBg.setObjectName(u"leftMenuBg")
        leftMenuBg.resize(60, 661)
        leftMenuBg.setMinimumSize(QSize(60, 0))
        leftMenuBg.setMaximumSize(QSize(60, 16777215))
        leftMenuBg.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(60, 50))
        self.topLogoInfo.setMaximumSize(QSize(60, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogoInfo.setLineWidth(0)
        self.logo = QLabel(self.topLogoInfo)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(5, 0, 50, 50))
        self.logo.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.leftMenuFrame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.leftMenu = QFrame(self.leftMenuFrame)
        self.leftMenu.setObjectName(u"leftMenu")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenu.sizePolicy().hasHeightForWidth())
        self.leftMenu.setSizePolicy(sizePolicy)
        self.leftMenu.setFrameShape(QFrame.NoFrame)
        self.leftMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.leftMenu)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btnFile = QPushButton(self.leftMenu)
        self.btnFile.setObjectName(u"btnFile")
        self.btnFile.setMinimumSize(QSize(60, 50))
        self.btnFile.setMaximumSize(QSize(60, 50))
        self.btnFile.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.btnFile)

        self.btnSettings = QPushButton(self.leftMenu)
        self.btnSettings.setObjectName(u"btnSettings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnSettings.sizePolicy().hasHeightForWidth())
        self.btnSettings.setSizePolicy(sizePolicy1)
        self.btnSettings.setMinimumSize(QSize(60, 50))
        self.btnSettings.setMaximumSize(QSize(60, 50))
        self.btnSettings.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.btnSettings)

        self.btnSecondPage = QPushButton(self.leftMenu)
        self.btnSecondPage.setObjectName(u"btnSecondPage")
        self.btnSecondPage.setMinimumSize(QSize(60, 50))
        self.btnSecondPage.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.btnSecondPage)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.verticalLayout_4.addWidget(self.leftMenu)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.retranslateUi(leftMenuBg)

        QMetaObject.connectSlotsByName(leftMenuBg)
    # setupUi

    def retranslateUi(self, leftMenuBg):
        self.logo.setText("")
#if QT_CONFIG(tooltip)
        self.btnFile.setToolTip(QCoreApplication.translate("leftMenuBg", u"<html><head/><body><p>\u6253\u5f00\u89c6\u9891\u6587\u4ef6\u5939</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnFile.setText("")
#if QT_CONFIG(tooltip)
        self.btnSettings.setToolTip(QCoreApplication.translate("leftMenuBg", u"<html><head/><body><p>\u8bbe\u7f6e</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnSettings.setText("")
        self.btnSecondPage.setText("")
        pass
    # retranslateUi

