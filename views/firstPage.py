from PySide6.QtWidgets import (QMainWindow, QWidget, 
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap, QMouseEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components import (videoPlayer, captureArea,
                              videoController, subVideoButtons)

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger


class FirstPageWidget(QWidget):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    subVideoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    videoControllerWidget: videoController.VideoControllerWidget = None
    captureAreaWidget: captureArea.CaptureAreaWidget = None

    

    def __init__(self, window):
        super().__init__()
        self.window = window
       
        # 加载组件
        self.initComponents()


    def initComponents(self):
        leftBox = QVBoxLayout()
        # VideoContent组件
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        leftBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = videoController.VideoControllerWidget(self.window)
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        leftBox.addWidget(self.videoControllerWidget)
        leftBoxWidget = QWidget() 
        leftBoxWidget.setLayout(leftBox)

        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.subVideoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        
        subVLayout = QVBoxLayout(self)
        subVLayout.setContentsMargins(0, 0, 0, 0)
        self.subVideoButtonsWidget = subVideoButtons.SubVideoButtonsWidget(self.window, self.subVideoPlayerWidget)
        subVLayout.addWidget(self.subVideoButtonsWidget)
        # 绑定帧事件
        self.subVideoPlayerWidget.setFrameReadEvent(self.subVideoButtonsWidget.modelManager.onFrameRead)

        self.captureAreaWidget = captureArea.CaptureAreaWidget(self.window)
        subVLayout.addWidget(self.captureAreaWidget)
        subVLayoutWidget = QWidget()
        subVLayoutWidget.setLayout(subVLayout)
        rightSplitter.addWidget(subVLayoutWidget)
        
        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 4)
        
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.addWidget(leftBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)




