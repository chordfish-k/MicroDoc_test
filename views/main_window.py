from PySide6.QtWidgets import (QMainWindow, QWidget,
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt, QTimer
from PySide6.QtGui import QIcon, QImage, QMouseEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components import (topbar, sidebar)
from views import firstPage

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger
from model.face_cut.face_cut import FaceCut

import resources_rc



class MyApp(QMainWindow):
    settings: Settings = None

    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QBoxLayout = None

    topBarWidget: topbar.TopBarWidget = None
    sideBarWidget: sidebar.SideBarWidget = None
    firstPageWidget: firstPage.FirstPageWidget = None



    def __init__(self, settings):
        super().__init__()
        # 加载UI
        Assets.loadUi('main_window', self)
        # 加载样式表
        Assets.loadQss('main', self)
        # 导入设置
        self.settings = settings

        # 窗体图标
        self.setWindowIcon(QIcon(":/icons/assets/images/icons/md.png"))
        import ctypes
        myappid = 'MicreDoc' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # 隐藏原有标题栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # 设置窗体为透明背景以显示圆角
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 加载组件
        self.initComponents()
        # 重设窗体大小
        self.resize(1088, 722)

        self.fc = FaceCut()
        self.frame_dir = os.path.join(QDir.currentPath(), "frames")
        if not os.path.exists(self.frame_dir):
            os.mkdir(self.frame_dir)


    def initComponents(self):
        self.topBar = self.ui.topBar
        self.sideBar = self.ui.sideBar
        self.main = self.ui.main

        # Topbar组件
        self.topBarWidget = topbar.TopBarWidget(self)
        self.topBar.addWidget(self.topBarWidget)
        # Sidebar组件
        self.sideBarWidget = sidebar.SideBarWidget(self)
        self.sideBar.addWidget(self.sideBarWidget)

        self.firstPageWidget = firstPage.FirstPageWidget(self)
        self.main.addWidget(self.firstPageWidget)


    def setVideoPath(self, path):
        if self.firstPageWidget:
            logger.debug('got path: '+ path)
            self.firstPageWidget.videoPlayerWidget.load(path)


    

