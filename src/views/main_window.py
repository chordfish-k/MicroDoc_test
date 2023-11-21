import datetime
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QBoxLayout
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
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint )

        # 放到公共区
        ObjectManager.set("window",self)

        # 加载组件
        self.initComponents()

        # 重设窗体大小
        self.resize(self.settings.get("default_width", int), self.settings.get("default_height", int))

        self.frame_dir = os.path.join(QDir.currentPath(), "frames")
        if not os.path.exists(self.frame_dir):
            os.mkdir(self.frame_dir)

        # self.setMouseTracking(True)

        
    def initComponents(self):

        # Topbar组件
        self.topBarWidget = TopBarWidget()
        self.topBar.addWidget(self.topBarWidget)
        self.topBarWidget.logout.connect(self.doLogout)
        # Sidebar组件
        self.sideBarWidget = SideBarWidget()
        self.sideBar.addWidget(self.sideBarWidget)
        self.sideBarWidget.change.connect(self.changePage)
        # stackWidget
        # 装载页面
        self.addPage(RecordPageWidget, tooltip="录制", icon="cil-chart", default=True)
        self.addPage(AnalysePageWidget, tooltip="检测", icon="cil-chart-line")
        self.addPage(ThirdPageWidget, icon="cil-featured-playlist")
        self.addPage(ForthPageWidget, icon="cil-satelite")
        self.addPage(UserPageWidget, icon="cil-user", btnGroup=SideBarWidget.ButtonGroup.DOWN)

        self.sideBarWidget.addToolBtn(self.switchTheme, tooltip="切换主题", icon="cil-lightbulb")            

        self.changePage(1)

        # 测试token有效性
        self.testToken()


    def addPage(self, pageWidgetClass, **kwargs):
        pageWidget = pageWidgetClass()
        self.pages.append(pageWidget)
        def func(page:int):
            def wapper():
                self.changePage(page)
            return wapper
        self.sideBarWidget.addPageBtn(func(len(self.pages)), **kwargs)
        self.main.addWidget(pageWidget)


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
        ObjectManager.set("refreshFlag", datetime.datetime.now())
        # print("refreshFlag", datetime.datetime.now())
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
