from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets
from views.components import videoPlayer, subVideoButtons

from util.settings import Settings


class RightPartWidget(QWidget):
    window: QMainWindow = None

    subVideo: QBoxLayout = None
    subVideoBtn: QBoxLayout = None

    videoWidget: videoPlayer.VideoPlayerWidget = None
    subVideoButtonsWidget: subVideoButtons.SubVIdeoButtonsWidget = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        Assets.loadUi('right_part', self)

        self.initComponents()


    def initComponents(self):
        self.subVideo = self.ui.subVideo
        self.subVideo = self.ui.subVideo

        self.videoWidget = videoPlayer.VideoPlayerWidget(self.window)
        self.subVideo.addWidget(self.videoWidget)

        self.subVideoButtonsWidget = subVideoButtons.SubVIdeoButtonsWidget(self.window)
        self.subVideo.addWidget(self.subVideoButtonsWidget)