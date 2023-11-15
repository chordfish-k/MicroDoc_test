from PySide6.QtWidgets import QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from components import MyQWidget
from .components import ReportListItemWidget
from util.logger import logger
from util.settings import settings
from api.report import getReportListAPI
from api.user import getUserTestAPI, postUserLoginAPI


class UserPageWidget(MyQWidget):
    window: QMainWindow = None
    btnLogin: QPushButton = None
    stackedWidget: QStackedWidget = None
    editAccount: QLineEdit = None
    editPassword: QLineEdit = None

    list = None

    def __init__(self, window):
        self.window = window
        super().__init__(name="user_page")
        
        # 测试token有效性
        self.testToken()


    def initComponents(self):
        self.btnLogin.clicked.connect(self.doLogin)
        self.window.logouted.connect(self.logoutSuccess)

        # 填充记录的账号
        account = settings.get("account")
        if account != None:
            self.editAccount.setText(account)

        self.lyScroll.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)


    def testToken(self):
        res = getUserTestAPI()
        print("test:",res)
        if (res['code']==1):
            self.window.loginSuccess()
            self.loginSuccess()
        else:
            settings.setItem("user", "")
            settings.setItem("token", "")
            self.logoutSuccess()


    def doLogin(self):
        account = self.editAccount.text()
        password = self.editPassword.text()
        print(account, password)

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
        self.getReportList()


    def logoutSuccess(self):
        self.stackedWidget.setCurrentIndex(0)


    def getReportList(self):
        res = getReportListAPI()
        if not res['code']:
            return
        
        print("report:", res['data'])
        self.list = res['data']

        # 准备容器
        ly: QVBoxLayout = self.lyScroll
        for i in range(ly.count()):
            ly.itemAt(i).widget().deleteLater()

        for item in self.list:
            li = ReportListItemWidget(self.window)
            li.setData(str(item['id']), item['uploadTime'])
            ly.addWidget(li)
