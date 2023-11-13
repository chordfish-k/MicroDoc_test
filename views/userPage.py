from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QStackedWidget,
                             QBoxLayout, QVBoxLayout, QSplitter, QCheckBox, QLineEdit)
from PySide6.QtCore import QDir, Qt, QTimer
from PySide6.QtGui import QIcon, QImage, QPixmap, QMouseEvent, QResizeEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np
from assets.api.report import getReportListAPI
from assets.api.user import getUserTestAPI, postUserLoginAPI

from views.components import (myChart, videoPlayer, captureArea, 
                              videoController, subVideoButtons,
                              subTools,reportListItem)

from assets.assets_loader import Assets
from util.http_request import requestAPI

from util.settings import Settings
from util.logger import logger
from model.manager import Manager
from views.components.captureItem import CaptureItemWidget
from views.components.imageWidget import ImageWidget
from views.components.myQWidget import MyQWidget

from util.settings import settings


class UserPageWidget(MyQWidget):

    window: QMainWindow = None
    btnLogin: QPushButton = None
    stackedWidget: QStackedWidget = None
    editAccount: QLineEdit = None
    editPassword: QLineEdit = None

    list = None

    def __init__(self, window):
       
        self.window = window
       
        super().__init__(window=window, name="user_page")
        
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
            li = reportListItem.ReportListItemWidget(self.window)
            li.setData(str(item['id']), item['uploadTime'])
            ly.addWidget(li)
