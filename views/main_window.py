from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QBoxLayout
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QIcon
import os, sys

from views.components import topbar, sidebar, videoContent
from assets.assets_loader import Assets
from assets.images.resources_rc import *

class MyApp(QMainWindow):
    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QBoxLayout = None

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
        self.topBar.addWidget(topbar.TopBarWidget(self))
        # Sidebar组件
        self.sideBar.addWidget(sidebar.SideBarWidget())
        # Main组件
        self.main.addWidget(videoContent.MainContentWidget())

