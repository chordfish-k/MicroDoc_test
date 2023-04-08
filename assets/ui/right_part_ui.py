# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'right_part.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_rightPart(object):
    def setupUi(self, rightPart):
        if not rightPart.objectName():
            rightPart.setObjectName(u"rightPart")
        rightPart.resize(297, 628)
        self.verticalLayout_2 = QVBoxLayout(rightPart)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.subVideo = QVBoxLayout()
        self.subVideo.setObjectName(u"subVideo")

        self.verticalLayout.addLayout(self.subVideo)

        self.subVideoBtn = QVBoxLayout()
        self.subVideoBtn.setObjectName(u"subVideoBtn")

        self.verticalLayout.addLayout(self.subVideoBtn)

        self.scrollArea = QVBoxLayout()
        self.scrollArea.setObjectName(u"scrollArea")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scrollArea.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.scrollArea)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(rightPart)

        QMetaObject.connectSlotsByName(rightPart)
    # setupUi

    def retranslateUi(self, rightPart):
        rightPart.setWindowTitle(QCoreApplication.translate("rightPart", u"Form", None))
    # retranslateUi

