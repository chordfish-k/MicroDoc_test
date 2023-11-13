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

class UserPageWidget(QWidget):
    window: QMainWindow = None


    def __init__(self, window):
        super().__init__()
        self.window = window
       

        Assets.loadUi("user_page", self)
    
        # 加载组件
        self.initComponents()

        


    def initComponents(self):
       
       pass

