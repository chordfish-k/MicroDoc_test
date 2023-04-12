from PySide6.QtWidgets import (QMainWindow, QWidget,
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon
import os

from views.components import (topbar, sidebar)
from views import firstPage, testPage

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
    secondPageWidget: testPage.TestPageWidget = None


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
        self.secondPageWidget = testPage.TestPageWidget(self)
        self.main.addWidget(self.firstPageWidget)


    def setVideoPath(self, path):
        if self.firstPageWidget:
            logger.debug('got path: '+ path)
            self.firstPageWidget.videoPlayerWidget.load(path)


    def openFirstPage(self):
        self.main.replaceWidget(self.secondPageWidget, self.firstPageWidget)
        self.firstPageWidget.show()
        self.secondPageWidget.hide()
        # if self.main.itemAt(0):
        #     wid = self.main.itemAt(0).widget()
        #     if wid is not self.firstPageWidget:
        #         self.main.replaceWidget(wid, self.firstPageWidget)
        #         # wid.deleteLater()
        #         #self.firstPageWidget = firstPage.FirstPageWidget(self)
        # #self.main.addWidget(self.firstPageWidget)
            
        
    def openSecondPage(self):
        self.main.replaceWidget(self.firstPageWidget, self.secondPageWidget)
        self.firstPageWidget.hide()
        self.secondPageWidget.show()
        # if self.main.itemAt(0):
        #     wid = self.main.itemAt(0).widget()
        #     if wid is not self.secondPageWidget:
        #         self.main.replaceWidget(wid, self.secondPageWidget)
        #         # wid.deleteLater()
        #         #self.secondPageWidget = testPage.TestPageWidget(self)
        # #self.main.addWidget(self.secondPageWidget)


