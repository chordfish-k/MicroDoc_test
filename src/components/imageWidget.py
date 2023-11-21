from typing import Union
from PySide6.QtGui import QPixmap, QResizeEvent, QPainter, QPen
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QFrame
from PySide6.QtCore import QDir, Qt, QRect, QEvent, QObject,QSize
import os
from PIL import ImageQt, Image

class ImageWidget(QWidget):
    
    imglb: QLabel = None
    __img: QPixmap = None
    __imgsize: tuple = (0,0)

    _inited: bool = False
    
    def __init__(self, parent, label:QLabel=None):
        super().__init__(parent)
        

        layout = QHBoxLayout(self)
        self.imglb = QLabel(self) if label==None else label
        self.imglb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.imglb)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.imglb.setScaledContents(True)

        self.imglb.setMouseTracking(True) # 监听鼠标
        self.setMouseTracking(True)
        



    def loadImage(self, path: str):
        self.__img = ImageQt.toqpixmap(Image.open(path))
        self.__imgsize = (self.__img.width(), self.__img.height())
        self.refreshImage()

    
    def loadImage(self, img : Image):
        self.__img = ImageQt.toqpixmap(img)
        self.__imgsize = (self.__img.width(), self.__img.height())
        self.refreshImage()


    def refreshImage(self):
        pixmap = self.__img
        pixmap = pixmap.scaled(self.imglb.size()-QSize(10,10), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        self.imglb.setPixmap(pixmap)


    def resizeEvent(self, event):
        self.refreshImage()

    
    def setAlignment(self, flag: Qt.AlignmentFlag):
        self.imglb.setAlignment(flag)

    # def fromQLabel(parent, lb: QLabel):
    #     return ImageWidget(parent, label=lb)