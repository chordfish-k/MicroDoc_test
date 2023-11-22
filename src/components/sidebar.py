import enum
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal
from src.components.myQWidget import MyQWidget
from src.util.share import ObjectManager


class SideBarWidget(MyQWidget):
    class Constants:
        BTN_MIN_W = 60
        BTN_MAX_H = 50
        BTN_POLICY_W = QSizePolicy.Policy.Fixed
        BTN_POLICY_H = QSizePolicy.Policy.Fixed

    class ButtonGroup(enum.IntEnum):
        UP = 0
        DOWN = 1

    window: QMainWindow = None

    navTopBtns: QVBoxLayout = None
    navBottomBtns: QVBoxLayout = None

    btnTheme: QPushButton = None
    btnFirstPage: QPushButton = None
    btnSecondPage: QPushButton = None
    btnThirdPage: QPushButton = None
    btnForthPage: QPushButton = None
    btnUser: QPushButton = None

    __pages = []

    change = Signal(int)

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="nav_sidebar")

    def __newNavBtn(self, **kwargs) -> QPushButton:
        """
        kwargs:
            tooltip:str
            icon:str
        """
        btn = QPushButton(self)
        btn.setMinimumSize(self.Constants.BTN_MIN_W, self.Constants.BTN_MAX_H)
        btn.setSizePolicy(self.Constants.BTN_POLICY_W, self.Constants.BTN_POLICY_H)
        if kwargs.get("tooltip"):
            btn.setToolTip(kwargs.get("tooltip"))
        if kwargs.get("icon"):
            btn.setStyleSheet("background-image: url(:/icons/assets/images/icons/{}.png)".format(kwargs.get("icon")))
        return btn

    def addToolBtn(self, func, btnGroup: ButtonGroup = ButtonGroup.DOWN, **kwargs):
        """
        kwargs:
            tooltip:str
            icon:str
        """
        layout = self.navBottomBtns
        if btnGroup == self.ButtonGroup.UP:
            layout = self.navTopBtns

        btn = self.__newNavBtn(**kwargs)

        btn.clicked.connect(func)
        layout.addWidget(btn)

    def addPageBtn(self, func, default: bool = False, btnGroup: ButtonGroup = ButtonGroup.UP, **kwargs):
        """
        kwargs:
            tooltip:str
            icon:str
        """
        layout = self.navTopBtns
        if btnGroup == self.ButtonGroup.DOWN:
            layout = self.navBottomBtns

        btn = self.__newNavBtn(**kwargs)
        btn.setProperty("selected", default)

        def _func(f, _btn: QPushButton):
            def wrapper():
                for b in self.__pages:
                    b.setProperty("selected", False)
                    b.setStyle(b.style())
                _btn.setProperty("selected", True)
                _btn.setStyle(_btn.style())
                f()

            return wrapper

        btn.clicked.connect(_func(func, btn))
        self.__pages.append(btn)
        layout.addWidget(btn)
