import os
import html
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel, QTextEdit, QFileDialog
from src.components import StackPage
from src.util.settings import settings
from src.util.share import ObjectManager
from src.util.eeg import eegAnalyse

class EEGPageWidget(StackPage):
    window: QMainWindow = None
    splitter: QSplitter = None

    btnOpen: QPushButton = None
    btnAnalyse: QPushButton = None
    lbPath: QLabel = None
    teLog: QTextEdit = None

    matPath: str

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="eeg_page")

    def initComponents(self):
        self.btnOpen.clicked.connect(self.openMatFile)
        self.btnAnalyse.clicked.connect(self.startAnalyse)

    def openMatFile(self):
        # 选择脑电数据文件
        current_path = os.path.join(settings.get("eeg_folder"))
        title = '选择MAT文件'
        filt = "MAT文件(*.mat);"
        self.matPath, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
        if self.matPath:
            self.lbPath.setText(os.path.basename(self.matPath))
            self.btnAnalyse.setEnabled(True)

    def startAnalyse(self):
        self.teLog.clear()
        eegAnalyse(self.matPath, self.logFunc)

    def logFunc(self, msg):
        # msg = msg.replace('\n', '<br/>')
        msgs = msg.split("\n")
        msg = ""
        for m in msgs:
            msg += html.escape(m) + "<br/>"
        self.teLog.append(f"<p>{msg}</p>")
