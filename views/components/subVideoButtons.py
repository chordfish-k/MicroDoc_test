from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets
from views.components import videoPlayer

from util.settings import Settings


class SubVIdeoButtonsWidget(QWidget):
    window: QMainWindow = None

    subVideo: QBoxLayout = None

    videoWidget: videoPlayer.VideoPlayerWidget = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        Assets.loadUi('sub_video_buttons', self)
        Assets.loadQss('sub_video_buttons', self)
