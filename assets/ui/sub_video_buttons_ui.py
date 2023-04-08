# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_video_buttons.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QWidget)

class Ui_subVideoButtons(object):
    def setupUi(self, subVideoButtons):
        if not subVideoButtons.objectName():
            subVideoButtons.setObjectName(u"subVideoButtons")
        subVideoButtons.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(subVideoButtons)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.subVideoBtnBg = QFrame(subVideoButtons)
        self.subVideoBtnBg.setObjectName(u"subVideoBtnBg")
        self.subVideoBtnBg.setStyleSheet(u"")
        self.subVideoBtnBgLayout = QHBoxLayout(self.subVideoBtnBg)
        self.subVideoBtnBgLayout.setObjectName(u"subVideoBtnBgLayout")
        self.subVideoBtnBgLayout.setContentsMargins(9, 9, 9, 9)
        self.sv_btn_camera = QPushButton(self.subVideoBtnBg)
        self.sv_btn_camera.setObjectName(u"sv_btn_camera")

        self.subVideoBtnBgLayout.addWidget(self.sv_btn_camera)

        self.sv_btn_file = QPushButton(self.subVideoBtnBg)
        self.sv_btn_file.setObjectName(u"sv_btn_file")

        self.subVideoBtnBgLayout.addWidget(self.sv_btn_file)


        self.horizontalLayout.addWidget(self.subVideoBtnBg)


        self.retranslateUi(subVideoButtons)

        QMetaObject.connectSlotsByName(subVideoButtons)
    # setupUi

    def retranslateUi(self, subVideoButtons):
        subVideoButtons.setWindowTitle(QCoreApplication.translate("subVideoButtons", u"Form", None))
        self.sv_btn_camera.setText(QCoreApplication.translate("subVideoButtons", u"\u6253\u5f00\u6444\u50cf\u5934", None))
        self.sv_btn_file.setText(QCoreApplication.translate("subVideoButtons", u"\u6253\u5f00\u672c\u5730\u6587\u4ef6", None))
    # retranslateUi

