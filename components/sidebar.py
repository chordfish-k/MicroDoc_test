from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QFileDialog
from PySide6.QtCore import QDir
import os
from assets.assets_loader import Assets
from util.logger import logger
from util.settings import Settings



class SideBarWidget(QWidget):
    window: QMainWindow = None
    
    btnTheme: QPushButton = None
    btnFirstPage: QPushButton = None
    btnSecondPage: QPushButton = None
    btnThirdPage: QPushButton = None
    btnForthPage: QPushButton = None
    btnUser: QPushButton = None

    __pages = []

    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('sidebar', self)
        Assets.loadQss('sidebar', self)

        self.initComponents()
    
    
    def initComponents(self):
        self.btnTheme.clicked.connect(self.window.switchTheme)

        # self.btnFile.clicked.connect(self.openVideoFile)
        self.__pages = [
            (self.btnFirstPage, 1),
            (self.btnSecondPage, 2),
            (self.btnThirdPage, 3),
            (self.btnForthPage, 4),
            (self.btnUser, 5),
        ]

        for b, p in self.__pages:
            b.clicked.connect(self.changePage(p, b))

        self.changePage(self.__pages[0][1], self.__pages[0][0])()

    # 函数闭包，有参转无参
    def changePage(self, index, btn:QPushButton):
        def __changePage():
            
            for b, _ in self.__pages:
                b.setProperty("selected", False)
                b.setStyle(btn.style())

            btn.setProperty("selected", True)
            btn.setStyle(btn.style())

            self.window.changePage(index)
            
        return __changePage


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
