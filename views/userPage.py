from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel,
                             QBoxLayout, QVBoxLayout, QSplitter, QCheckBox)
from PySide6.QtCore import QDir, Qt, QTimer
from PySide6.QtGui import QIcon, QImage, QPixmap, QMouseEvent, QResizeEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components import (myChart, videoPlayer, captureArea, 
                              videoController, subVideoButtons,
                              subTools)

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger
from model.manager import Manager
from views.components.captureItem import CaptureItemWidget
from views.components.imageWidget import ImageWidget
from views.components.myQWidget import MyQWidget

class UserPageWidget(MyQWidget):

    window: QMainWindow = None

    def __init__(self, window):
       
        self.window = window
       
        super().__init__(window=window, name="user_page")

        


    def initComponents(self):
    #    img = ImageWidget.fromQLabel(self.ui.loginPage, self.ui.img)
    #    img.loadImage("assets/images/images/logo_fill.png")
       pass

