from PySide6.QtWidgets import QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from src.components import MyQWidget, StackPage, PaginationWidget
from src.util.share import ObjectManager
from .components import ReportListItemWidget
from src.util.logger import logger
from src.util.settings import settings
from src.api.report import getReportListAPI, getReportPageAPI
from src.api.user import getUserTestAPI, postUserLoginAPI


class UserPageWidget(StackPage):
    window: QMainWindow = None
    btnLogin: QPushButton = None
    stackedWidget: QStackedWidget = None
    editAccount: QLineEdit = None
    editPassword: QLineEdit = None

    lyPagination: QVBoxLayout = None

    list = None

    pageSize = 6

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="user_page")
        

        # 未登录
        self.loginSucceedFlag = False
        self.window.loginned.connect(self.loginSuccess)
        self.window.logouted.connect(self.logoutSuccess)


    def initComponents(self):
        self.btnLogin.clicked.connect(self.doLogin)
        self.window.logouted.connect(self.logoutSuccess)

        # 填充记录的账号
        account = settings.get("account")
        if account != None:
            self.editAccount.setText(account)

        self.lyScroll.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.pagination = PaginationWidget()
        self.pagination.changed.connect(self.onPaginationChanged)
        self.lyPagination.addWidget(self.pagination)



    def doLogin(self):
        account = self.editAccount.text()
        password = self.editPassword.text()
        # print(account, password)

        res = postUserLoginAPI({
            'phone': account,
            'pwd': password
        })

        print(res)
        if (res['code'] == 1):
            # 登录成功
            self.window.loginSuccess(res['data'])
            self.loginSuccess()


    def loginSuccess(self):
        self.stackedWidget.setCurrentIndex(1)
        self.loginSucceedFlag = True
        self.getReportList()


    def logoutSuccess(self):
        self.stackedWidget.setCurrentIndex(0)
        self.loginSucceedFlag = False


    def getReportList(self):
        # res = getReportListAPI()
        res = getReportPageAPI(self.pagination.currentPage, self.pagination.pageSize)

        if not res['code']:
            return
        
        # print("report:", res['data'])
        data = res['data']
        self.list = data['records']

        # 设置分页信息
        self.pagination.setPageParms(pageSize = self.pageSize, total=data['total'])

        # 准备容器
        ly: QVBoxLayout = self.lyScroll
        for i in range(ly.count()):
            ly.itemAt(i).widget().deleteLater()

        for item in self.list:
            li = ReportListItemWidget(self.window)
            li.setData(str(item['id']), item['uploadTime'])
            ly.addWidget(li)


    def onPageChanged(self):
        if self.loginSucceedFlag:
            self.getReportList()


    def onPaginationChanged(self, page:int):
        self.getReportList()