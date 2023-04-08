# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_player.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_viewComponent(object):
    def setupUi(self, viewComponent):
        if not viewComponent.objectName():
            viewComponent.setObjectName(u"viewComponent")
        viewComponent.resize(448, 288)
        self.verticalLayout_2 = QVBoxLayout(viewComponent)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.videobg = QVBoxLayout()
        self.videobg.setSpacing(0)
        self.videobg.setObjectName(u"videobg")
        self.video_zoom = QLabel(viewComponent)
        self.video_zoom.setObjectName(u"video_zoom")
        self.video_zoom.setMinimumSize(QSize(0, 180))
        self.video_zoom.setStyleSheet(u"")
        self.video_zoom.setFrameShape(QFrame.NoFrame)
        self.video_zoom.setAlignment(Qt.AlignCenter)

        self.videobg.addWidget(self.video_zoom)


        self.verticalLayout_2.addLayout(self.videobg)


        self.retranslateUi(viewComponent)

        QMetaObject.connectSlotsByName(viewComponent)
    # setupUi

    def retranslateUi(self, viewComponent):
        viewComponent.setWindowTitle(QCoreApplication.translate("viewComponent", u"Form", None))
        self.video_zoom.setText(QCoreApplication.translate("viewComponent", u"data", None))
    # retranslateUi

