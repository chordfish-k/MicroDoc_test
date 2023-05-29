from PySide6.QtWidgets import (QMainWindow, QWidget, QSplitter, QPushButton, QLabel)
from PySide6.QtCore import Qt
from assets.assets_loader import Assets
from views.components.imageWidget import ImageWidget


class ForthPageWidget(QWidget):
    window: QMainWindow = None
    outside: QWidget = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        
        Assets.loadUi("forth_page", self)
        Assets.loadQss("forth_page", self)
        # 加载组件
        self.initComponents()


    def initComponents(self):

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Vertical)

        leftimg = ImageWidget(self)
        splitter.addWidget(leftimg)

        rightimg = ImageWidget(self)
        splitter.addWidget(rightimg)
        
        leftimg.loadImage('assets/res/PSD/psd.jpg')
        rightimg.loadImage('assets/res/PSD/psd_topomap.jpg')
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        self.outside.layout().addWidget(splitter)