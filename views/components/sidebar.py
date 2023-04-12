from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QFileDialog)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets
from util.logger import logger
from util.settings import Settings



class SideBarWidget(QWidget):
    window: QMainWindow = None
    
    btnFile: QPushButton = None
    btnFirstPage: QPushButton = None
    btnSecondPage: QPushButton = None

    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('sidebar', self)
        Assets.loadQss('sidebar', self)

        self.initComponents()
    
    
    def initComponents(self):
        self.btnFile = self.ui.btnFile
        self.btnFirstPage = self.ui.btnFirstPage
        self.btnSecondPage = self.ui.btnSecondPage

        self.btnFile.clicked.connect(self.openVideoFile)
        self.btnFirstPage.clicked.connect(self.window.openFirstPage)
        self.btnSecondPage.clicked.connect(self.window.openSecondPage)


    def openVideoFile(self):
        settings:Settings = self.window.settings
        last_path = settings.get('last_dir_path')
        logger.debug("last_path: " + last_path)
        current_path = QDir.currentPath() if not last_path else last_path
        title = '选择视频文件'
        filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
        file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
        if file_path:

            # 存储上次打开的文件夹路径
            path = settings.get('last_dir_path')
            self.last_dir_path = os.path.dirname(file_path)  if not path else path
            settings.setItem('last_dir_path', self.last_dir_path)
            settings.save()

            # 调用MyApp的函数来处理
            self.window.setVideoPath(file_path)
