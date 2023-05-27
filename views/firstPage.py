from PySide6.QtWidgets import (QMainWindow, QWidget, 
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt, QTimer
from PySide6.QtGui import QIcon, QImage, QPixmap, QMouseEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components import (myChart, videoPlayer, captureArea, 
                              videoController, subVideoButtons)

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
    captureAreaWidget: captureArea.CaptureAreaWidget = None

    modelTimer1 = None

    def __init__(self, window):
        super().__init__()
        self.window = window

        self.modelManager = Manager(self.window.settings)
        self.modelManager.setOutputFn(self.showResult)

        self.modelTimer1 = QTimer()
        self.modelTimer1.timeout.connect(self.onModelTimer)
        self.modelTimer1.start(1)
       
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
        # VideoContent组件
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        videoBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = videoController.VideoControllerWidget(self.window)
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        videoBox.addWidget(self.videoControllerWidget)

        # MyChart
        # self.chartWidget = myChart.MyChartWidget(self)
        # leftSplitter.addWidget(self.chartWidget)

        # leftSplitter.setStretchFactor(0, 2)
        # leftSplitter.setStretchFactor(1, 3)

        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.subVideoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        
        subVLayout = QVBoxLayout(self)
        subVLayout.setContentsMargins(0, 0, 0, 0)
        self.subVideoButtonsWidget = subVideoButtons.SubVideoButtonsWidget(self.window, self.subVideoPlayerWidget, self.modelManager)
        subVLayout.addWidget(self.subVideoButtonsWidget)
        # 绑定帧事件
        self.subVideoPlayerWidget.setFrameReadEvent(self.modelManager.onFrameRead)

        self.captureAreaWidget = captureArea.CaptureAreaWidget(self.window)
        subVLayout.addWidget(self.captureAreaWidget)
        subVLayoutWidget = QWidget()
        subVLayoutWidget.setLayout(subVLayout)
        rightSplitter.addWidget(subVLayoutWidget)
        
        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 8)
        
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.addWidget(videoBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        # self.modelManager.setChartWidget(self.chartWidget)

    def onModelTimer(self):
        if self.modelManager.modelActive:
            self.modelManager.activate_network()


    def showResult(self, img_path:str, time:str, state:str):
        logger.debug("output: "+img_path)
        logger.debug(time + state)
        item = CaptureItemWidget()
        item.setStatus(img_path, time, state)
        self.captureAreaWidget.layout.addWidget(item)


