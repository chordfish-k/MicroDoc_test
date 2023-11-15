from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from components import VideoPlayerWidget, VideoControllerWidget, MyQWidget
from .components import SubToolsWidget
from util.logger import logger


class RecordPageWidget(MyQWidget):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: VideoPlayerWidget = None
    subVideoPlayerWidget: VideoPlayerWidget = None
    videoControllerWidget: VideoControllerWidget = None
    subToolsWidget: SubToolsWidget = None

    def __init__(self, window):
        super().__init__(window=window)
        self.window = window

        
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
        # VideoContent组件
        self.videoPlayerWidget = VideoPlayerWidget(self.window)
        self.videoPlayerWidget.setHintText("请选择情绪诱发视频")
        videoBox.addWidget(self.videoPlayerWidget)
        self.videoControllerWidget = VideoControllerWidget(self.window)
        self.videoControllerWidget.attachVideoPlayer(self.videoPlayerWidget)
        self.videoControllerWidget.setShowStopBtn(False)
        videoBox.addWidget(self.videoControllerWidget)

        # MyChart
        # self.chartWidget = myChart.MyChartWidget(self)
        # leftSplitter.addWidget(self.chartWidget)

        # leftSplitter.setStretchFactor(0, 2)
        # leftSplitter.setStretchFactor(1, 3)

        rightSplitter = QSplitter(self)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        # right UP
        self.subVideoPlayerWidget = VideoPlayerWidget(self.window)
        self.subVideoPlayerWidget.setHintText("摄像头未连接")
        rightSplitter.addWidget(self.subVideoPlayerWidget)
        # right DOWN
        self.subToolsWidget = SubToolsWidget(
            self.window, self.videoPlayerWidget,
            self.subVideoPlayerWidget, self.videoControllerWidget)
        rightSplitter.addWidget(self.subToolsWidget)

        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 8)
        
        
        # 使用分离器装载
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.addWidget(videoBoxWidget)
        self.splitter.addWidget(rightSplitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
