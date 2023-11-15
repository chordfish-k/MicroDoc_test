from PySide6.QtWidgets import QMainWindow, QWidget, QLabel,QSizePolicy, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from assets.assets_loader import Assets
from components import ImageWidget
from .components import GridImageButton
from PIL import Image
from util.tools import *


class ThirdPageWidget(QWidget):
    window: QMainWindow = None
    outside: QWidget = None

    rightimg: QLabel = None

    gw = 5
    gh = 6

    def __init__(self, window):
        super().__init__()
        self.window = window
        
        Assets.loadUi("third_page", self)
        Assets.loadQss("third_page", self)
        # 加载组件
        self.initComponents()


    def initComponents(self):
        splitter = QWidget(self)
        splitterLayout = QHBoxLayout(splitter)
        splitterLayout.setContentsMargins(0, 0, 0, 0)
        # splitter = QSplitter(self)
        # splitter.setOrientation(Qt.Orientation.Horizontal)

        self.leftimg = ImageWidget(self)
        splitterLayout.addWidget(self.leftimg)

        # self.rightimg = ImageWidget(self)
        # splitter.addWidget(self.rightimg)
        
        
        # self.rightimg.loadImage('assets/res/ICA/plot_components.jpg')

        rightGrid = QWidget(self)
        self.rightGridLayout = QGridLayout(rightGrid)
        self.rightGridLayout.setContentsMargins(0,0,0,0)
        self.rightGridLayout.setSpacing(0)
        

        icons = Image.open("assets/res/ICA/plot_components.jpg")
        head = 151
        icons = copyImage(icons, 0, head, icons.width, icons.height-head)
        iw = icons.width // self.gw
        ih = icons.height // self.gh
        # print(icons.width, icons.height, iw, ih)

        for i in range(self.gh):
            for j in range(self.gw):
                ic = copyImage(icons, j*iw, i*ih, iw, ih)

                btn = GridImageButton(self)
                btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
                btn.loadImage(ic)
                btn.setIndex(i*5+j)
                btn.clicked.connect(self.onGridBtnClick)
                

                self.rightGridLayout.addWidget(btn, i, j)
        #默认选中第一个
        self.rightGridLayout.itemAtPosition(0,0).widget().setFocus(True)
        self.lastChosen = (0,0)

        splitterLayout.addWidget(rightGrid)


        # splitter.setStretchFactor(0, 5)
        # splitter.setStretchFactor(1, 5)

        # splitter.handle(1).setDisabled(True) # 不可拖动分割器

        self.outside.layout().addWidget(splitter)

        self.leftimg.loadImage('assets/res/ICA/ICA_0.jpg')

        splitterLayout.setStretch(0, 5)
        splitterLayout.setStretch(1, 3)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.window.isMaximized():
            pos = event.globalPosition().toPoint()
            self.m_flag = True
            self.m_position = pos - self.window.pos()  # 获取鼠标相对窗口的位置
            # print(self.rightimg.frameGeometry().topLeft(), self.m_position - self.rightimg.frameGeometry().topLeft())
            event.accept()


    def onGridBtnClick(self, index: int):
        self.rightGridLayout.itemAtPosition(*self.lastChosen).widget().setFocus(False)
        self.lastChosen = (index//self.gw, index%self.gw)
        self.rightGridLayout.itemAtPosition(*self.lastChosen).widget().setFocus(True)
        # for i in range(self.gh):
        #     for j in range(self.gw):
        #         gib: GridImageButton = self.rightGridLayout.itemAtPosition(i,j).widget()
        #         gib.setFocus(index == i*self.gw+j)
        self.leftimg.loadImage(f'assets/res/ICA/ICA_{index}.jpg')
