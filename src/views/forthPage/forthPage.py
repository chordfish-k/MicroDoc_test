from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter
from PySide6.QtCore import Qt
from src.components import ImageWidget, StackPage
from src.util.share import ObjectManager


class ForthPageWidget(StackPage):
    window: QMainWindow = None
    outside: QWidget = None

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="forth_page")

    def initComponents(self):
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Vertical)

        leftImg = ImageWidget(self)
        splitter.addWidget(leftImg)

        rightImg = ImageWidget(self)
        splitter.addWidget(rightImg)

        leftImg.loadImage('src/assets/res/PSD/psd.jpg')
        rightImg.loadImage('src/assets/res/PSD/psd_topomap.jpg')
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        splitter.handle(1).setDisabled(True)  # 不可拖动分割器

        self.outside.layout().addWidget(splitter)
