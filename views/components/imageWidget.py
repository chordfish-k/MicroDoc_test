from typing import Union
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import QDir, Qt
import os
from PIL import ImageQt, Image


class ImageWidget(QWidget):
    
    __imglb: QLabel = None
    __img: QPixmap = None
    __imgsize: tuple = (0,0)
    
    def __init__(self, parent):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        self.__imglb = QLabel()
        self.__imglb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.__imglb)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)


    def loadImage(self, path: str):
        self.__img = ImageQt.toqpixmap(Image.open(path))
        self.__imgsize = (self.__img.width(), self.__img.height())
        self.refreshImage()


    def refreshImage(self):
        self.__imglb.setPixmap(self.__img)
        w, h = self.size().toTuple()
        lw, lh = self.__imgsize
        pw, ph = w, h
        
        if w/h <= lw/lh:
            # fit width
            ph = int(lh * w / lw)
        else:
            # fit height
            pw = int(lw * h / lh)
        self.__imglb.setPixmap(self.__img.scaled(pw, ph))  # 拉伸图片


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.refreshImage()
        return super().resizeEvent(event)

    
    def setAlignment(self, flag: Qt.AlignmentFlag):
        self.__imglb.setAlignment(flag)