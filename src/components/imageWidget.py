from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PIL import ImageQt, Image


class ImageWidget(QWidget):
    imglb: QLabel = None
    __img: QPixmap = None
    __imgsize: tuple = (0, 0)

    _inited: bool = False

    def __init__(self, parent, label: QLabel = None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        self.imglb = QLabel(self) if not label else label
        self.imglb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.imglb)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.imglb.setScaledContents(True)

        self.imglb.setMouseTracking(True)  # 监听鼠标
        self.setMouseTracking(True)

    def loadImage(self, pathOrImage: str):
        self.__img = ImageQt.toqpixmap(Image.open(path))
        self.__imgsize = (self.__img.width(), self.__img.height())
        self.refreshImage()

    def loadImage(self, img: Image):
        self.__img = ImageQt.toqpixmap(img)
        self.__imgsize = (self.__img.width(), self.__img.height())
        self.refreshImage()

    def refreshImage(self):
        pixmap = self.__img
        if not pixmap:
            return
        pixmap = pixmap.scaled(self.imglb.size() - QSize(10, 10), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        self.imglb.setPixmap(pixmap)

    def resizeEvent(self, event):
        self.refreshImage()

    def setAlignment(self, flag: Qt.AlignmentFlag):
        self.imglb.setAlignment(flag)

