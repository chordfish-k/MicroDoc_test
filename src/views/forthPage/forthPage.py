from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter
from PySide6.QtCore import Qt
from assets.assets_loader import Assets
from components import ImageWidget, StackPage
from util.share import ObjectManager


class ForthPageWidget(StackPage):
    window: QMainWindow = None
    outside: QWidget = None

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="forth_page")


    def initComponents(self):

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Vertical)

        leftimg = ImageWidget(self)
        splitter.addWidget(leftimg)

        rightimg = ImageWidget(self)
        splitter.addWidget(rightimg)
        
        leftimg.loadImage('src/assets/res/PSD/psd.jpg')
        rightimg.loadImage('src/assets/res/PSD/psd_topomap.jpg')
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        splitter.handle(1).setDisabled(True) # 不可拖动分割器

        self.outside.layout().addWidget(splitter)