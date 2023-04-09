from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets
from views.components import videoPlayer

from util.settings import Settings
from util.logger import logger


class SubVIdeoButtonsWidget(QWidget):
    window: QMainWindow = None

    svBtnCamera: QPushButton = None
    svBtnFile: QPushButton = None

    videoWidget: videoPlayer.VideoPlayerWidget = None

    def __init__(self, window, videoWidget):
        super().__init__()
        self.window = window
        self.videoWidget = videoWidget

        Assets.loadUi('sub_video_buttons', self)
        Assets.loadQss('sub_video_buttons', self)

        self.initComponents()


    def initComponents(self):
        self.svBtnCamera = self.ui.svBtnCamera
        self.svBtnFile = self.ui.svBtnFile

        self.svBtnCamera.clicked.connect(self.toggleCamera)
        self.svBtnFile.clicked.connect(self.toggleFile)


    def toggleCamera(self):
        logger.debug('toggle camera')
        self.videoWidget.toggleCamera()
        self.svBtnCamera.setText(
            "关闭摄像头" if self.videoWidget.isOpenedCamera else "打开摄像头")


    def toggleFile(self):
        logger.debug('toggle file')
        # self.svBtnCamera.setText("关闭文件")
