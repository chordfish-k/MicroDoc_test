from PIL import Image
from PIL import ImageQt

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import Qt, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from util.logger import logger

#侧边栏组件，显示捕获的微表情状态
class CaptureItemWidget(QWidget):
    def __init__(self):
        super().__init__()

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


    class Thread_1(QThread):  # 线程1
        over = Signal(QThread)
        def __init__(self, img:Image):
            super().__init__()
            self.img = img

        def run(self):
            self.img.show()
            self.over.emit(self)



    #双击打开图片查看
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        
        if event.buttons() == Qt.MouseButton.LeftButton:
            #self.open_dialog(self.img)
            img = Image.open(self.img_path)

            if img:
                def onImgClose1():
                    self.pth1.quit()
                    self.pth1 = None
                    logger.debug("close img broswer thread1")

                def onImgClose2():
                    self.pth2.quit()
                    self.pth2 = None
                    logger.debug("close img broswer thread2")

                if not self.pth1:
                    #self.pth = self.pth1
                    self.pth1 = self.Thread_1(img)
                    self.pth1.start()
                    self.pth1.over.connect(onImgClose1)
                    logger.debug("start img broswer thread1")
                elif not self.pth2:
                    #self.pth = self.pth2
                    self.pth2 = self.Thread_1(img)
                    self.pth2.start()
                    self.pth2.over.connect(onImgClose2)
                    logger.debug("start img broswer thread2")

            event.accept()