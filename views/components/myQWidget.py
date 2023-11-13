from PySide6.QtWidgets import QWidget

from assets.assets_loader import Assets

class MyQWidget(QWidget):

    name:str = None

    def __init__(self,  window=None, name=None):
        super().__init__()
        self.name = name

        if self.name:
            Assets.loadUi(self.name, self)
            Assets.loadQss(self.name, self)

        self.initComponents()
        self.refresh()

    def initComponents(self):
       pass

    def refresh(self):
        if self.name:
            Assets.loadQss(self.name, self)
            
        for k in self.__dict__:
            v = self.__dict__[k]
            if isinstance(v, MyQWidget):
                v.refresh()