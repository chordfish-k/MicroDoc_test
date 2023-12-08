from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from src.components.myQWidget import MyQWidget
import webbrowser

class ReportListItemWidget(MyQWidget):
    window: QMainWindow = None
    lbId: QLabel = None
    lbTime: QLabel = None
    btnLink: QPushButton = None

    def __init__(self, window):
        self.window = window
        super().__init__(name="report_item")

    def initComponents(self):
        self.btnLink.clicked.connect(self.openLink)

    def openLink(self):
        webbrowser.open("http://localhost:5173/chart-show/" + self.lbId.text())

    def setData(self, id: str, time: str):
        self.lbId.setText(id)
        self.lbTime.setText(time)
