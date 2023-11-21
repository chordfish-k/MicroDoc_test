from PySide6.QtWidgets import QWidget
from assets.assets_loader import Assets
from util.share import ObjectManager
import datetime


class MyQWidget(QWidget):
    name:str = None
    noUi = False
    noQss = False

    def __init__(self, name=None, noUi=False, noQss=False):
        super().__init__()
        self.name = name
        self.noUi = noUi
        self.noQss = noQss
        self.lastRefreshTime = None

        if self.name:
            if not self.noUi:
                Assets.loadUi(self.name, self)
            if not self.noQss:
                Assets.loadQss(self.name, self)

        self.initComponents()
        # self.refresh()

    def initComponents(self):
       pass

    def refresh(self):
        # refreshFlag = ObjectManager.get("refreshFlag")
        # if not refreshFlag:
        #     refreshFlag = datetime.datetime.now()
        #     ObjectManager.set("refreshFlag", refreshFlag)
        # if ObjectManager.get("refreshFlag") == self.lastRefreshTime:
        #     return
        # self.lastRefreshTime = ObjectManager.get("refreshFlag")

        if self.name:
            if not self.noQss:
                Assets.loadQss(self.name, self)
            
        for k in self.__dict__:
            v = self.__dict__[k]
            if isinstance(v, MyQWidget) and v != self:
                v.refresh()