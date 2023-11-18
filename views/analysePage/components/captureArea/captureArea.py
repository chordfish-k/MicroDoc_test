import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtGui import Qt, QMouseEvent
from util.logger import logger
from components.myQWidget import MyQWidget
from PIL import Image
from PIL import ImageQt
import base64

from util.share import ObjectManager


class CaptureAreaWidget(MyQWidget):
    window: QMainWindow = None
    scrollAreaLayout: QVBoxLayout = None

    datas = []

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="capture_area")


    def initComponents(self):
        self.scrollAreaLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)


    def addCaptureItem(self, img_path:str, time:str, state:str, old:int, new:int):
        item = CaptureItemWidget(self.scrollAreaLayout.widget())
        item.setStatus(img_path, time, state)
        self.scrollAreaLayout.addWidget(item)

        with open(img_path, "rb") as image_file:
            encoded_string = "data:image/png;base64," + base64.b64encode(image_file.read()).decode("utf-8")

        # 保存到数据结构
        self.datas.append({
            'imgB64': encoded_string,
            'before': str(old),
            'after': str(new),
            'time': time
        })
        # print(self.datas)

    def getData(self):
        return self.datas


    def cleanAll(self):
        self.datas = []
        for i in range(self.scrollAreaLayout.count()):
	        self.scrollAreaLayout.itemAt(i).widget().deleteLater()





#侧边栏组件，显示捕获的微表情状态
class CaptureItemWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.img_path = ''
        self.img = None
        self.timestamp = '00:00:00'
        self.judge = 'Null'

        self.pth = None
        self.pth1 = None
        self.pth2 = None

        self.box = QHBoxLayout(self)
        self.qimg = QLabel(self)
        self.qtimeLabel = QLabel(self)
        self.qjudgeLabel = QLabel(self)

        self.box.addWidget(self.qimg)
        self.box.addWidget(self.qtimeLabel)
        self.box.addWidget(self.qjudgeLabel)
        self.setLayout(self.box)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMaximumHeight(100)

        self.setToolTip("双击查看")


    # 信息设置
    def setStatus(self, img_path: str, timestamp='00:00:00', judge='Null'):
        self.img_path = img_path
        if self.img_path:
            self.img = ImageQt.toqpixmap(Image.open(img_path))
            w = 80
            h = int(self.img.height() * w / self.img.width())
            self.qimg.setPixmap(self.img.scaled(w, h))  # 拉伸图片
        
        self.timestamp = timestamp
        self.judge = judge
        self.qtimeLabel.setText(self.timestamp)
        self.qjudgeLabel.setText(self.judge)


    #双击打开图片查看
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            os.startfile(self.img_path)
            event.accept()