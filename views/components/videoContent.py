from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap
import os

from assets.assets_loader import Assets

class MainContentWidget(QWidget):
    logo: QLabel

    def __init__(self):
        super().__init__()

        Assets.loadUi('video_page', self)

