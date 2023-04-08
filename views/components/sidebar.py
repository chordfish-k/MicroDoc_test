from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QFileDialog)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets

from util.settings import Settings


class SideBarWidget(QWidget):
    window: QMainWindow
    
    btnFile: QPushButton

    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('sidebar', self)
        Assets.loadQss('sidebar', self)

        self.initComponents()
    
    
    def initComponents(self):
        self.btnFile = self.ui.btnFile
        self.btnFile.clicked.connect(self.openVideoFile)


    def openVideoFile(self):

        current_path = QDir.currentPath()
        title = '选择视频文件'
        filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
        file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
        if file_path:

            # 存储上次打开的文件夹路径
            settings:Settings = self.window.settings
            path = settings.get('last_dir_path')
            self.last_dir_path = os.path.dirname(file_path)  if not path else path
            settings.setItem('last_dir_path', self.last_dir_path)
            settings.save()

            # 调用MyApp的函数来处理
            self.window.setVideoPath(file_path)

        
