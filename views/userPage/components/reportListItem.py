from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from util.logger import logger
from components.myQWidget import MyQWidget


class ReportListItemWidget(MyQWidget):
    window: QMainWindow = None
    lbId: QLabel = None
    lbTime: QLabel = None
    btnLink: QPushButton = None

    def __init__(self, window):
        self.window = window
        super().__init__(name="report_item")
    
    def initComponents(self):
        pass

    def setData(self, id: str, time: str):
        self.lbId.setText(id)
        self.lbTime.setText(time)
        
