from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel,
                             QBoxLayout, QSplitter)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import os

from assets.assets_loader import Assets
from views.components import videoPlayer, rightPart

class VideoContentWidget(QWidget):
    window: QMainWindow
    leftSide: QBoxLayout
    rightSide: QBoxLayout

    videoPlayerWidget: videoPlayer.VideoPlayerWidget

    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('video_page', self)
        Assets.loadQss('video_page', self)

        self.initComponents()


    def initComponents(self):
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        #policy = QSizePolicy()
        #self.videoPlayerWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Preferred)
        self.leftSide.addWidget(self.videoPlayerWidget)
        #self.rightSide.addWidget(self.videoPlayerWidget)
        
        
        self.rightSide.addWidget(rightPart.RightPartWidget(self))
        
        