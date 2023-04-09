from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtUiTools import loadUiType, QUiLoader
import os, sys

from views.components import (topbar, sidebar, videoPlayer, 
                              videoController, subVideoButtons)

from assets.assets_loader import Assets
import resources_rc

from util.settings import Settings
from util.logger import logger




class MyApp(QMainWindow):
    settings: Settings = None

    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QBoxLayout = None
    splitter: QSplitter = None

    topBarWidget: topbar.TopBarWidget = None
    sideBarWidget: sidebar.SideBarWidget = None
    videoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    subVideoPlayerWidget: videoPlayer.VideoPlayerWidget = None
    videoControllerWidget: videoController.VideoControllerWidget = None


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

        
        leftBox = QVBoxLayout()
        # VideoContent组件
        self.videoPlayerWidget = videoPlayer.VideoPlayerWidget(self)
        leftBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = videoController.VideoControllerWidget(self)
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        leftBox.addWidget(self.videoControllerWidget)
        leftBoxWidget = QWidget() 
        leftBoxWidget.setLayout(leftBox)

        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.subVideoPlayerWidget = videoPlayer.VideoPlayerWidget(self)
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        self.subVideoButtonsWidget = subVideoButtons.SubVIdeoButtonsWidget(self, self.subVideoPlayerWidget)
        rightSplitter.addWidget(self.subVideoButtonsWidget)
        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 4)
        
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName('mainContent')
        self.splitter.addWidget(leftBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.main.addWidget(self.splitter)


    def setVideoPath(self, path):
        logger.debug('got path: '+ path)
        self.videoPlayerWidget.load(path)


    def splitterMousePressEvent(self, e:QMouseEvent):
        logger.debug('clicked')
        return super().mousePressEvent(e)



