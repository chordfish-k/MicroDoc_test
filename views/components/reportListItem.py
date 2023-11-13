from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QFileDialog)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir, Qt
import os

from assets.assets_loader import Assets
from util.logger import logger
from util.settings import Settings
from views.components.myQWidget import MyQWidget



class ReportListItemWidget(MyQWidget):
    window: QMainWindow = None
    
    lbId: QLabel = None
    lbTime: QLabel = None
    btnLink: QPushButton = None

    def __init__(self, window):
        
        self.window = window

        super().__init__(window=window, name="report_item")
    
    def initComponents(self):
        pass

    def setData(self, id: str, time: str):
        self.lbId.setText(id)
        self.lbTime.setText(time)
        
