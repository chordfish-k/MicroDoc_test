from PySide6.QtWidgets import QMainWindow, QStackedWidget, QBoxLayout, QMessageBox, QPushButton
from PySide6.QtCore import QDir, Qt, Signal
from PySide6.QtGui import QIcon
import os
from api.user import getUserTestAPI
from components import TopBarWidget, SideBarWidget, MyQWidget,StackPage
from views import *
from assets.assets_loader import Assets
from util.settings import settings
from util.logger import logger
from util.share import ObjectManager
from model.face_cut.face_cut import FaceCut
import resources_rc



class MyApp(QMainWindow):
    # 布局
    topBar: QBoxLayout = None
    sideBar: QBoxLayout = None
    main: QStackedWidget = None
    # 窗口组件
    topBarWidget: TopBarWidget = None
    sideBarWidget: SideBarWidget = None
    # 页面
    pages: list[StackPage] = []
    recordPageWidget: RecordPageWidget = None
    analysePageWidget: AnalysePageWidget = None
    thirdPageWidget: ThirdPageWidget = None
    forthPageWidget: ForthPageWidget = None
    userPageWidget: UserPageWidget = None

    logouted = Signal()
    loginned = Signal()


    def __init__(self):
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
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint 
                        #    | Qt.WindowType.WindowMinMaxButtonsHint 
                        #    | Qt.WindowType.WindowCloseButtonHint 
                        #    | Qt.WindowType.WindowStaysOnTopHint
                           )
        # 设置窗体为透明背景以显示圆角
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        ObjectManager.set("window",self)

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
        self.topBarWidget = TopBarWidget()
        self.topBar.addWidget(self.topBarWidget)
        # Sidebar组件
        self.sideBarWidget = SideBarWidget()
        self.sideBar.addWidget(self.sideBarWidget)
        self.sideBarWidget.change.connect(self.changePage)
        # stackWidget
        # 装载页面
        self.recordPageWidget = RecordPageWidget()
        self.analysePageWidget = AnalysePageWidget()
        self.thirdPageWidget = ThirdPageWidget(self)
        self.forthPageWidget = ForthPageWidget(self)
        self.userPageWidget = UserPageWidget()
        self.pages.append(self.recordPageWidget)
        self.pages.append(self.analysePageWidget)
        self.pages.append(self.thirdPageWidget)
        self.pages.append(self.forthPageWidget)
        self.pages.append(self.userPageWidget)

        for page in self.pages:
            self.main.addWidget(page)

        self.changePage(1)
        # 测试token有效性
        self.testToken()


    def changePage(self, index=1):
        if index <= len(self.pages):
            self.main.setCurrentIndex(index)
            self.pages[index-1].onPageChanged()
        

    def getCurrentPageIndex(self):
        return self.main.currentIndex()


    def switchTheme(self):
        theme = self.settings.get('theme')
        theme = "dark" if theme=="light" else "light"
        self.settings.setItem("theme", theme)
        Assets.loadQdef(theme)
        self.refesh()


    def refesh(self):
        Assets.loadQss('main', self)

        for k in self.__dict__:
            v = self.__dict__[k]
            if isinstance(v, MyQWidget):
                v.refresh()

        for page in self.pages:
            if isinstance(page, MyQWidget):
                page.refresh()


    def loginSuccess(self, data=None):
        if (data):
            self.settings.setItem("token", data['token'])
            self.settings.setItem("account", data['phone'])
            self.settings.setItem("user", data['name'])
            self.settings.save()

        self.topBarWidget.refreshUserTag()
        self.loginned.emit()

    
    def doLogout(self):
        self.settings.setItem("token", "")
        self.settings.setItem("user", "")
        self.settings.save()

        self.topBarWidget.refreshUserTag()
        self.logouted.emit()


    def testToken(self):
        res = getUserTestAPI()
        # print("test:",res)
        if (res['code']==1):
            self.loginSuccess()
        else:
            settings.setItem("user", "")
            settings.setItem("token", "")
            self.doLogout()