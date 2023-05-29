from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout, QFileDialog)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir, QTimer
import os

from assets.assets_loader import Assets
from views.components import videoPlayer

from util.settings import Settings
from util.logger import logger




class SubVideoButtonsWidget(QWidget):
    window: QMainWindow = None

    svBtnCamera: QPushButton = None
    svBtnFile: QPushButton = None
    svBtnActive: QPushButton = None

    videoWidget: videoPlayer.VideoPlayerWidget = None

    manager = None


    def __init__(self, window, videoWidget, manager):
        super().__init__()
        self.window = window
        self.videoWidget = videoWidget
        self.manager = manager

        Assets.loadUi('sub_video_buttons', self)
        Assets.loadQss('sub_video_buttons', self)

        self.initComponents()


    def initComponents(self):

        # self.svBtnCamera.clicked.connect(self.toggleCamera)
        self.svBtnFile.clicked.connect(self.toggleFile)
        self.svBtnActive.clicked.connect(self.toggleActive)


    def toggleCamera(self):
        logger.debug('toggle camera')
        self.videoWidget.toggleCamera()
        self.svBtnCamera.setText(
            "关闭摄像头" if self.videoWidget.isOpenedCamera else "打开摄像头")


    def toggleFile(self):
        logger.debug('toggle file')

        if not self.videoWidget.isLoaded:
            
            settings:Settings = self.window.settings
            last_path = "videos"#settings.get('last_dir_path')
            logger.debug("last_path: " + last_path)
            current_path = QDir.currentPath() if not last_path else last_path
            title = '选择视频文件'
            filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
            file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
            if file_path:

                # 存储上次打开的文件夹路径
                path = os.path.dirname(file_path)
                settings.setItem('last_dir_path', path)
                settings.save()

                self.videoWidget.load(file_path)
                self.videoWidget.play()

        else:
            self.videoWidget.stop()

        self.svBtnFile.setText(
            "关闭本地文件" if self.videoWidget.isLoaded else "打开本地文件")
        

    def toggleActive(self):
        if not self.manager.modelActive:
            self.manager.modelActive = True
        else:
            self.manager.modelActive = False

        self.svBtnActive.setText(
            "停止模型" if self.manager.modelActive else "启动模型")
