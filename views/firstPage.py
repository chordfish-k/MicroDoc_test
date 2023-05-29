from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel,
                             QBoxLayout, QVBoxLayout, QSplitter, QCheckBox)
from PySide6.QtCore import QDir, Qt, QTimer
from PySide6.QtGui import QIcon, QImage, QPixmap, QMouseEvent, QResizeEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components import (myChart, videoPlayer, captureArea, 
                              videoController, subVideoButtons,
                              subTools)

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger
from model.manager import Manager
from views.components.captureItem import CaptureItemWidget

class FirstPageWidget(QWidget):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    subVideoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    videoControllerWidget: videoController.VideoControllerWidget = None
    subToolsWidget: subTools.SubToolsWidget = None
    # captureAreaWidget: captureArea.CaptureAreaWidget = None


    def __init__(self, window):
        super().__init__()
        self.window = window
       
        # 加载组件
        self.initComponents()

        


    def initComponents(self):
        """
        [old]
        self
            |_splitter(hor)
                |_leftSplitter(ver)
                |   |_videoBoxWidget
                |   |   |_videoPlayerWidget
                |   |   |_videoControllerWidget
                |   |_chartWidget
                |_rightSplitter(ver)
                    |_subVideoPlayerWidget
                    |_subVLayoutWidget
                        |_subVideoButtonsWidget
                        |_captureAreaWidget
        [new]
        self
            |_splitter(hor)
                |_videoBoxWidget
                |   |_videoPlayerWidget
                |   |_videoControllerWidget
                |_rightSplitter
                    |_subVideoPlayerWidget
                    |_toolListWiget
        """      

        videoBoxWidget = QWidget()
        videoBox = QVBoxLayout(videoBoxWidget)
        videoBox.setContentsMargins(0, 0, 0, 0)
        # VideoContent组件
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        self.videoPlayerWidget.setHintText("请选择情绪诱发视频")
        videoBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = videoController.VideoControllerWidget(self.window)
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        self.videoControllerWidget.setShowStopBtn(False)
        videoBox.addWidget(self.videoControllerWidget)

        # MyChart
        # self.chartWidget = myChart.MyChartWidget(self)
        # leftSplitter.addWidget(self.chartWidget)

        # leftSplitter.setStretchFactor(0, 2)
        # leftSplitter.setStretchFactor(1, 3)

        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        # right UP
        self.subVideoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        self.subVideoPlayerWidget.setHintText("摄像头未连接")
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        # right DOWN
        self.subToolsWidget = subTools.SubToolsWidget(
            self.window, self.videoPlayerWidget,
            self.subVideoPlayerWidget, self.videoControllerWidget)
        rightSplitter.addWidget(self.subToolsWidget)

        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 8)
        
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.addWidget(videoBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)


