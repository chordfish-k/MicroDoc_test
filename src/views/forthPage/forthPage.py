import os

from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter
from PySide6.QtCore import Qt
from src.components import ImageWidget, StackPage
from src.util.settings import settings
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

        self.leftImg = ImageWidget(self)
        splitter.addWidget(self.leftImg)

        self.rightImg = ImageWidget(self)
        splitter.addWidget(self.rightImg)

        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        splitter.handle(1).setDisabled(True)  # 不可拖动分割器

        self.outside.layout().addWidget(splitter)

        self.refresh()

    def refresh(self):
        path = os.path.join(settings.get("eeg_folder"), 'output/PSD/psd.png')
        if os.path.exists(path):
            self.leftImg.loadImage(path)

        path = os.path.join(settings.get("eeg_folder"), 'output/PSD/psd_topomap.png')
        if os.path.exists(path):
            self.rightImg.loadImage(path)

    def onPageChanged(self):
        self.refresh()
