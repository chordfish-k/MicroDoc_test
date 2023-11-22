from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Signal

from src.components import ImageWidget


class GridImageButton(ImageWidget):
    _index = 0
    focusd: bool = False
    is_hovered: bool = False
    _fn = None

    clicked = Signal(int)
    
    def __init__(self, parent):
        super().__init__(parent)

        self.imglb.setMouseTracking(True) # 监听鼠标
        self.imglb.setStyleSheet("border:1px solid transparent;")
        self.setMouseTracking(True)


    def setFocus(self, focus:bool):
        self.focusd = focus
        if focus:
            self.imglb.setStyleSheet("border:1px solid black;")
        else:
            self.imglb.setStyleSheet("border:1px solid transparent;")

        
    def setIndex(self, index: int):
        self._index = index

        
    def enterEvent(self, event):
        self.is_hovered = True
        self.imglb.setStyleSheet("border:1px solid black;")
        self.update()


    def leaveEvent(self, event):
        self.is_hovered = False
        if  not self.focusd:
            self.imglb.setStyleSheet("border:1px solid transparent;")
        self.update()


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clicked.emit(self._index)
        return super().mousePressEvent(event)
