from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout, QSplitter)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir, Qt
import os

from assets.assets_loader import Assets
from views.components import videoPlayer, subVideoButtons

from util.settings import Settings


class RightPartWidget(QWidget):
    window: QMainWindow = None

    subVideo: QBoxLayout = None
    subVideoBtn: QBoxLayout = None
    splitter: QSplitter = None

    videoWidget: videoPlayer.VideoPlayerWidget = None
    subVideoButtonsWidget: subVideoButtons.SubVideoButtonsWidget = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        Assets.loadUi('right_part', self)

        self.initComponents()


    def initComponents(self):

        self.videoWidget = videoPlayer.VideoPlayerWidget(self.window)
        # self.subVideo.addWidget(self.videoWidget)

        self.subVideoButtonsWidget = subVideoButtons.SubVideoButtonsWidget(self.window)
        # self.subVideo.addWidget(self.subVideoButtonsWidget)

        self.splitter = QSplitter()
        self.splitter.setObjectName('mainContent')
        self.splitter.addWidget(self.videoWidget)
        self.splitter.addWidget(self.subVideoButtonsWidget)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)
        self.subVideo.addWidget(self.splitter)

