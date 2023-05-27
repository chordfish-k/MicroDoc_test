from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel)

from assets.assets_loader import Assets


class TestPageWidget(QWidget):
    window: QMainWindow = None
    
    btnSelModel: QPushButton = None
    btnSelData: QPushButton = None
    btnTest: QPushButton = None
    lbResult: QLabel = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        
        Assets.loadUi("test_page", self)
        Assets.loadQss("test_page", self)
        # 加载组件
        self.initComponents()


    def initComponents(self):


        self.btnSelModel.clicked.connect(self.selectModel)
        self.btnSelData.clicked.connect(self.selectData)
        self.btnTest.clicked.connect(self.startTest)


    def selectModel(self):
        pass


    def selectData(self):
        pass


    def startTest(self):
        pass