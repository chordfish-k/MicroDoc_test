from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                             QPushButton, QBoxLayout, QSlider)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QDir
import os

from assets.assets_loader import Assets
from views.components import videoPlayer, subVideoButtons

from util.settings import Settings
from util.logger import logger


class VideoControllerWidget(QWidget):
    window: QMainWindow = None

    btnStart: QPushButton = None
    btnStop: QPushButton = None
    videoSlider: QSlider = None
    lbCurrTime: QLabel = None
    lbEndTime: QLabel = None

    player: videoPlayer.VideoPlayerWidget = None


    def __init__(self, window):
        super().__init__()
        self.window = window
        Assets.loadUi('video_controller', self)
        Assets.loadQss('video_controller', self)

        self.initComponents()


    def initComponents(self):
        self.btnStart = self.ui.btnStart
        self.btnStop = self.ui.btnStop
        self.videoSlider = self.ui.videoSlider
        self.lbCurrTime = self.ui.lbCurrTime
        self.lbEndTime = self.ui.lbEndTime

    
    def attachVideoPlayer(self, videoPlayer):
        self.player = videoPlayer
        self.btnStart.clicked.connect(self.onPlayBtnPress)
        self.btnStop.clicked.connect(self.onStopBtnPress)

    
    def onPlayBtnPress(self):
        if self.player.isLoaded:
            if not self.player.isPlaying:
                logger.debug("video started")
                self.player.play()
                self.btnStart.setStyleSheet(
                    "background-image: url(:/icons/assets/images/icons/cil-media-pause.png)")
            else:
                logger.debug("video paused")
                self.player.pause()
                self.btnStart.setStyleSheet(
                    "background-image: url(:/icons/assets/images/icons/cil-media-play.png)")
        else:
            logger.warning("video file is not loaded!")


    def onStopBtnPress(self):
        if self.player.isLoaded:
            logger.debug("video stoped")
            self.player.stop()
            self.btnStart.setStyleSheet(
                    "background-image: url(:/icons/assets/images/icons/cil-media-play.png)")
        else:
            logger.warning("video file is not loaded!")
