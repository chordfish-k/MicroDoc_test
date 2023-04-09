from PIL import Image
from PIL import ImageQt

from PySide6.QtGui import Qt, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

#侧边栏组件，显示捕获的微表情状态
class CaptureItemWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.img_path = ''
        self.img = None
        self.timestamp = '00:00:00'
        self.judge = 'Null'

        self.box = QHBoxLayout(self)
        self.qimg = QLabel(self)
        self.qtimeLabel = QLabel(self)
        self.qjudgeLabel = QLabel(self)

        self.box.addWidget(self.qimg)
        self.box.addWidget(self.qtimeLabel)
        self.box.addWidget(self.qjudgeLabel)
        self.setLayout(self.box)


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
            #self.open_dialog(self.img)
            img = Image.open(self.img_path)
            if (img):
                img.show() 
            event.accept()