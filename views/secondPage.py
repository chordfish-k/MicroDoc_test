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

class SecondPageWidget(QWidget):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    videoControllerWidget: videoController.VideoControllerWidget = None
    subToolsWidget: subTools.SubToolsWidget = None
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
        self
            |_splitter(hor)
                |_leftSplitter(ver)
                |   |_videoBoxWidget
                |   |   |_videoPlayerWidget
                |   |_chartWidget
                |_rightBoxWidget
                    |_subVideoButtonWidget
                    |_captureAreaWiget
        """      
        # splitter(hor)
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.setOrientation(Qt.Orientation.Horizontal)

        # leftSplitter(ver)
        leftSplitter = QSplitter(self.splitter)
        leftSplitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(leftSplitter)
        # videoBoxWidget
        videoBoxWidget = QWidget(leftSplitter)
        videoBox = QVBoxLayout(videoBoxWidget)
        videoBox.setContentsMargins(0, 0, 0, 0)
        # videoBoxWidget
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self.window)
        self.videoPlayerWidget.setFrameReadEvent(self.modelManager.onFrameRead)
        videoBox.addWidget(self.videoPlayerWidget)
        # chartWidget
        self.chartWidget = myChart.MyChartWidget(leftSplitter)
        self.modelManager.setChartWidget(self.chartWidget)
        leftSplitter.addWidget(self.chartWidget)

        leftSplitter.setStretchFactor(0, 3)
        leftSplitter.setStretchFactor(1, 2)
        leftSplitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # rightBoxWidget
        rightBoxWidget = QWidget(self.splitter)
        rightBox = QVBoxLayout(rightBoxWidget)
        rightBox.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(rightBoxWidget)
        # subVideoButtonWidget
        self.subToolsWidget = subVideoButtons.SubVideoButtonsWidget(self.window, self.videoPlayerWidget, self.modelManager)
        rightBox.addWidget(self.subToolsWidget)
        # captureAreaWiget
        self.captureAreaWidget = captureArea.CaptureAreaWidget(self.window)
        rightBox.addWidget(self.captureAreaWidget)

        
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        

    def onModelTimer(self):
        if self.modelManager.modelActive:
            self.modelManager.activate_network()


    def showResult(self, img_path:str, time:str, state:str):
        logger.debug("output: "+img_path)
        logger.debug(time + state)
        item = CaptureItemWidget()
        item.setStatus(img_path, time, state)
        self.captureAreaWidget.layout.addWidget(item)
