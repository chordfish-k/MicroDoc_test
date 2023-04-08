from PySide6.QtWidgets import QMainWindow, QWidget,QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

import os

from assets.assets_loader import Assets

class TopBarWidget(QWidget):
    window: QMainWindow = None
    tbBtnClose: QPushButton = None
    tbBtnMinimize: QPushButton = None
    tbBtnMaximize: QPushButton = None

    isMaximized = False
    m_flag = False
    m_position = None


    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('topbar', self)
        Assets.loadQss('topbar', self)

        self.initComponents()


    def initComponents(self):
        self.tbBtnClose = self.ui.tbBtnClose
        self.tbBtnMinimize = self.ui.tbBtnMinimize
        self.tbBtnMaximize = self.ui.tbBtnMaximize

        self.tbBtnClose.clicked.connect(self.window.close)
        self.tbBtnMinimize.clicked.connect(self.window.showMinimized)
        self.tbBtnMaximize.clicked.connect(self.toggleMaximize)


    def toggleMaximize(self):
        if not self.isMaximized:
            self.window.showMaximized()
            self.tbBtnMaximize.setStyleSheet(
               "background-image: url(:/icons/assets/images/icons/icon_restore.png)")
        else:
            self.window.showNormal()
            self.tbBtnMaximize.setStyleSheet(
                "background-image: url(:/icons/assets/images/icons/icon_maximize.png)")
        
        self.isMaximized = not self.isMaximized


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self.window.isMaximized():
            pos = event.globalPosition().toPoint()
            self.m_flag = True
            self.m_position = pos - self.window.pos()  # 获取鼠标相对窗口的位置
            event.accept()


    def mouseMoveEvent(self, event: QMouseEvent):
        if Qt.MouseButton.LeftButton and self.m_flag:
            self.window.move(event.globalPosition().toPoint() - self.m_position)  # 更改窗口位置
            event.accept()


    def mouseReleaseEvent(self, event: QMouseEvent):
        self.m_flag = False

        
