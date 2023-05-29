from PySide6.QtWidgets import (QMainWindow, QWidget, QStackedWidget,
                             QBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon
import os

from views.components import (topbar, sidebar)
from views import firstPage, secondPage, thirdPage, forthPage

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger
from model.face_cut.face_cut import FaceCut

import resources_rc

class MyApp(QMainWindow):
    settings: Settings = None

    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QStackedWidget = None

    topBarWidget: topbar.TopBarWidget = None
    sideBarWidget: sidebar.SideBarWidget = None
    firstPageWidget: firstPage.FirstPageWidget = None
    secondPageWidget: secondPage.SecondPageWidget = None
    thirdPageWidget: thirdPage.ThirdPageWidget = None


    def __init__(self, settings):
        super().__init__()
        # 导入设置
        self.settings = settings
        # 加载UI
        Assets.loadUi('main_window', self)
        # 加载样式表
        Assets.loadQdef(self.settings.get('theme'))
        Assets.loadQss('main', self)

        # 窗体图标
        self.setWindowIcon(QIcon(":/icons/assets/images/icons/logo_fill.png"))
        import ctypes
        myappid = 'MicroDoc' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # 隐藏原有标题栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # 设置窗体为透明背景以显示圆角
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 加载组件
        self.initComponents()
        # 重设窗体大小
        self.resize(self.settings.get("default_width", int), self.settings.get("default_height", int))

        self.fc = FaceCut()
        self.frame_dir = os.path.join(QDir.currentPath(), "frames")
        if not os.path.exists(self.frame_dir):
            os.mkdir(self.frame_dir)

        
    def initComponents(self):

        # Topbar组件
        self.topBarWidget = topbar.TopBarWidget(self)
        self.topBar.addWidget(self.topBarWidget)
        # Sidebar组件
        self.sideBarWidget = sidebar.SideBarWidget(self)
        self.sideBar.addWidget(self.sideBarWidget)
        # stackWidget
        # 装载页面
        self.main.addWidget(firstPage.FirstPageWidget(self))
        self.main.addWidget(secondPage.SecondPageWidget(self))
        self.main.addWidget(thirdPage.ThirdPageWidget(self))
        self.main.addWidget(forthPage.ForthPageWidget(self))
        
        self.changePage(1)


    def changePage(self, index=1):
        self.main.setCurrentIndex(index)
        

    def getCurrentPageIndex(self):
        return self.main.currentIndex()


    def switchTheme(self):
        Assets.loadQdef(self.settings.get('theme'))
        pass

