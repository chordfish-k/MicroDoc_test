from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from src.util.settings import settings
from src.components.myQWidget import MyQWidget
from src.util.share import ObjectManager


class TopBarWidget(MyQWidget):
    window: QMainWindow = None
    tbBtnClose: QPushButton = None
    tbBtnMinimize: QPushButton = None
    tbBtnMaximize: QPushButton = None
    btnLogout: QPushButton = None

    userInfoBox: QWidget = None
    lbUserTag: QLabel = None

    isMaximized = False
    m_flag = False
    m_position = None

    logout = Signal()

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="topbar")

    def initComponents(self):
        self.tbBtnClose.clicked.connect(self.window.close)
        self.tbBtnMinimize.clicked.connect(self.window.showMinimized)
        self.tbBtnMaximize.clicked.connect(self.toggleMaximize)

        self.btnLogout.clicked.connect(self.doLogout)

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

    def refreshUserTag(self):
        userName = settings.get("user")
        if userName:
            self.userInfoBox.setMaximumWidth(10000)
            self.lbUserTag.setText(userName)
        else:
            self.userInfoBox.setMaximumWidth(0)

    def doLogout(self):
        self.logout.emit()
