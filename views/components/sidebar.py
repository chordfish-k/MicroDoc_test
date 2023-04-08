from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap
import os

from assets.assets_loader import Assets

class SideBarWidget(QWidget):
    logo: QLabel

    def __init__(self):
        super().__init__()

        Assets.loadUi('sidebar', self)
        Assets.loadQss('sidebar', self)
