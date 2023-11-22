from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import *
from src.components import VideoPlayerWidget, VideoControllerWidget, StackPage, MediaPlayer
from src.util.share import ObjectManager
from src.util.logger import logger
from .components import SubToolsWidget



class RecordPageWidget(StackPage):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: VideoPlayerWidget = None
    subVideoPlayerWidget: VideoPlayerWidget = None
    videoControllerWidget: VideoControllerWidget = None
    subToolsWidget: SubToolsWidget = None

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__()
        
        
    def initComponents(self):
        """
        [old]
        self
            |_splitter(hor)
                |_leftSplitter(ver)
                |   |_videoBoxWidget
                |   |   |_videoPlayerWidget
                |   |   |_videoControllerWidget
                |   |_chartWidget
                |_rightSplitter(ver)
                    |_subVideoPlayerWidget
                    |_subVLayoutWidget
                        |_subVideoButtonsWidget
                        |_captureAreaWidget
        [new]
        self
            |_splitter(hor)
                |_videoBoxWidget
                |   |_videoPlayerWidget
                |   |_videoControllerWidget
                |_rightSplitter
                    |_subVideoPlayerWidget
                    |_toolListWiget
        """      

        videoBoxWidget = QWidget()
        videoBox = QVBoxLayout(videoBoxWidget)
        videoBox.setContentsMargins(0, 0, 0, 0)
        videoBox.setSpacing(0)
        # VideoContent组件
        self.videoPlayerWidget = MediaPlayer()#VideoPlayerWidget()
        # self.videoPlayerWidget.setHintText("请选择情绪诱发视频")
        videoBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = VideoControllerWidget()
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        self.videoControllerWidget.setShowStopBtn(False)

        self.videoPlayerWidget.positionChanged.connect(self.positionChanged)
        self.videoPlayerWidget.loadded.connect(self.videoLoadded)
        videoBox.addWidget(self.videoControllerWidget)


        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        # right UP
        self.subVideoPlayerWidget = VideoPlayerWidget()
        self.subVideoPlayerWidget.setHintText("摄像头未连接")
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        # right DOWN
        self.subToolsWidget = SubToolsWidget(self.videoPlayerWidget,self.subVideoPlayerWidget)
        self.subToolsWidget.closeFile.connect(self.stopVideo)
        rightSplitter.addWidget(self.subToolsWidget)

        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 1)
        rightSplitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.addWidget(videoBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setOpaqueResize(False)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)


    def stopVideo(self):
        self.videoControllerWidget.onStopBtnPress()


    def positionChanged(self, position):
        self.videoControllerWidget.setSliderPosition(position)


    def videoLoadded(self, duration):
        self.videoControllerWidget.setSliderDuration(duration)
        self.videoControllerWidget.onPlayBtnPress()