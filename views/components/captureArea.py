from PySide6.QtWidgets import (QMainWindow, QWidget,
                                QVBoxLayout)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QIcon, QImage, QMouseEvent
from PIL import Image, ImageQt
import os, sys
import cv2
import numpy as np

from views.components.captureItem import CaptureItemWidget

from assets.assets_loader import Assets

from util.settings import Settings
from util.logger import logger
from views.components.myQWidget import MyQWidget


class CaptureAreaWidget(MyQWidget):
    window: QMainWindow = None
    scrollAreaLayout: QVBoxLayout = None

    def __init__(self, window):
        
        self.window = window

        # Assets.loadUi("capture_area", self)
        # Assets.loadQss("capture_area", self)

        super().__init__(window=window, name="capture_area")

        # self.initComponents()


    def initComponents(self):
        self.scrollAreaLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)



        