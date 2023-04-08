from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QBoxLayout, QSplitter)
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QIcon, QResizeEvent
import os, sys

from views.components import (topbar, sidebar, 
                              videoPlayer, rightPart)

from assets.assets_loader import Assets
from assets.images.resources_rc import *

from util.settings import Settings
from util.logger import logger


class MyApp(QMainWindow):
    settings = Settings()

    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QBoxLayout = None

    topBarWidget: topbar.TopBarWidget = None
    sideBarWidget: sidebar.SideBarWidget = None
    videoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    rightPartWidget: rightPart.RightPartWidget = None


    def __init__(self):
        super().__init__()
        # 加载UI
        Assets.loadUi('main_window', self)
        # 加载样式表
        Assets.loadQss('main', self)
        # 窗体图标
        self.setWindowIcon(QIcon(":/images/images/md.png"))
        # 隐藏原有标题栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # 设置窗体为透明背景以显示圆角
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 加载组件
        self.initComponents()
        # 重设窗体大小
        self.resize(1088, 722)
        

    def initComponents(self):
        # Topbar组件
        self.topBarWidget = topbar.TopBarWidget(self)
        self.topBar.addWidget(self.topBarWidget)
        # Sidebar组件
        self.sideBarWidget = sidebar.SideBarWidget(self)
        self.sideBar.addWidget(self.sideBarWidget)
        # VideoContent组件
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self)
        # RightPart组件
        self.rightPartWidget = rightPart.RightPartWidget(self)
        # 使用分离器装载VideoContent和RightPart
        self.splitter = QSplitter(self)
        self.splitter.setObjectName('mainContent')
        self.splitter.addWidget(self.videoPlayerWidget)
        self.splitter.addWidget(self.rightPartWidget)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 8)
        self.splitter.setStretchFactor(1, 5)
        self.main.addWidget(self.splitter)


    def setVideoPath(self, path):
        logger.debug('got path: '+ path)
        self.videoPlayerWidget.load(path)



