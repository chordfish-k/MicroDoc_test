import os.path
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QSizePolicy, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QMouseEvent
from src.util.share import ObjectManager
from src.util.tools import *
from src.components import ImageWidget, StackPage
from .components import GridImageButton
from PIL import Image


class ThirdPageWidget(StackPage):
    window: QMainWindow = None
    outside: QWidget = None
    rightGridLayout: QGridLayout = None
    rightImg: QLabel = None
    leftImg = None
    lastChosen = None
    gw = 5
    gh = 6

    def __init__(self):
        self.m_position = None
        self.m_flag = None
        self.window = ObjectManager.get("window")
        super().__init__(name="third_page")

    def initComponents(self):
        splitter = QWidget(self)
        splitterLayout = QHBoxLayout(splitter)
        splitterLayout.setContentsMargins(0, 0, 0, 0)

        self.leftImg = ImageWidget(self)
        splitterLayout.addWidget(self.leftImg)

        rightGrid = QWidget(self)
        self.rightGridLayout = QGridLayout(rightGrid)
        self.rightGridLayout.setContentsMargins(0, 0, 0, 0)
        self.rightGridLayout.setSpacing(0)

        icons = Image.open("src/assets/res/ICA/plot_components.jpg")
        head = 151
        icons = copyImage(icons, 0, head, icons.width, icons.height - head)
        iw = icons.width // self.gw
        ih = icons.height // self.gh
        # print(icons.width, icons.height, iw, ih)

        for i in range(self.gh):
            for j in range(self.gw):
                ic = copyImage(icons, j * iw, i * ih, iw, ih)

                btn = GridImageButton(self)
                btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
                btn.loadImage(ic)
                btn.setIndex(i * 5 + j)
                btn.clicked.connect(self.onGridBtnClick)

                self.rightGridLayout.addWidget(btn, i, j)
        # 默认选中第一个
        self.rightGridLayout.itemAtPosition(0, 0).widget().setItemFocus(True)
        self.lastChosen = (0, 0)

        splitterLayout.addWidget(rightGrid)

        self.outside.layout().addWidget(splitter)

        self.leftImg.loadImage('src/assets/res/ICA/ICA_0.jpg')

        splitterLayout.setStretch(0, 5)
        splitterLayout.setStretch(1, 3)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.window.isMaximized():
            pos = event.globalPosition().toPoint()
            self.m_flag = True
            self.m_position = pos - self.window.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def onGridBtnClick(self, index: int):
        self.rightGridLayout.itemAtPosition(*self.lastChosen).widget().setItemFocus(False)
        self.lastChosen = (index // self.gw, index % self.gw)
        self.rightGridLayout.itemAtPosition(*self.lastChosen).widget().setItemFocus(True)

        self.leftImg.loadImage(f'src/assets/res/ICA/ICA_{index}.jpg')
