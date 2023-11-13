from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout, QFileDialog)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir, QTimer
import os

from assets.assets_loader import Assets
from views.components import videoPlayer

from util.settings import Settings
from util.logger import logger
from views.components.myQWidget import MyQWidget




class SubVideoButtonsWidget(MyQWidget):
    window: QMainWindow = None

    svBtnCamera: QPushButton = None
    svBtnFile: QPushButton = None
    svBtnActive: QPushButton = None

    videoWidget: videoPlayer.VideoPlayerWidget = None

    manager = None


    def __init__(self, window, videoWidget, manager):
        
        self.window = window
        self.videoWidget = videoWidget
        self.manager = manager

        super().__init__(window=window, name="sub_video_buttons")


    def initComponents(self):

        # self.svBtnCamera.clicked.connect(self.toggleCamera)
        self.svBtnFile.clicked.connect(self.toggleFile)
        self.svBtnActive.clicked.connect(self.toggleActive)

    
    def connectChartsWidget(self, charts):
        self.charts = charts


    def connectCaptureAreaWidget(self, capture):
        self.captureArea = capture


    def toggleCamera(self):
        logger.debug('toggle camera')
        self.videoWidget.toggleCamera()
        self.svBtnCamera.setText(
            "关闭摄像头" if self.videoWidget.isOpenedCamera else "打开摄像头")


    def toggleFile(self):
        logger.debug('toggle file-----------------------')

        if not self.videoWidget.isLoaded:
            
            settings:Settings = self.window.settings
            # 默认打开存放录制视频的文件夹
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
                
                self.charts.clean_datas()
                self.captureArea.cleanAll()
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
