from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt, QTimer
from src.api.report import postReportAPI
from .components import CaptureAreaWidget, MyChartWidget, SubVideoButtonsWidget
from src.components import StackPage, VideoControllerWidget, VideoPlayerWidget
from src.util.logger import logger
from src.model.manager import ModelManager
from src.util.share import ObjectManager


class AnalysePageWidget(StackPage):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: VideoPlayerWidget = None
    videoControllerWidget: VideoControllerWidget = None
    subVideoButtons: SubVideoButtonsWidget = None
    captureAreaWidget: CaptureAreaWidget = None

    modelTimer1 = None

    def __init__(self):
        
        self.window = ObjectManager.get("window")

        self.modelManager = ModelManager()
        self.modelManager.setOutputFn(self.showResult)

        self.modelTimer1 = QTimer()
        self.modelTimer1.timeout.connect(self.onModelTimer)
        self.modelTimer1.start(1)

        super().__init__()


    def initComponents(self):
        """
        self
            |_splitter(hor)
                |_leftSplitter(ver)
                |   |_videoBoxWidget
                |   |   |_videoPlayerWidget
                |   |_chartWidget
                |_rightBoxWidget
                    |_subVideoButtonWidget
                    |_captureAreaWiget
        """      
        # splitter(hor)
        self.splitter = QSplitter(self)
        self.splitter.setObjectName(u'mainContent')
        self.splitter.setOrientation(Qt.Orientation.Horizontal)

        # leftSplitter(ver)
        leftSplitter = QSplitter(self.splitter)
        leftSplitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(leftSplitter)
        # videoBoxWidget
        videoBoxWidget = QWidget(leftSplitter)
        videoBox = QVBoxLayout(videoBoxWidget)
        videoBox.setContentsMargins(0, 0, 0, 0)
        # videoBoxWidget
        self.videoPlayerWidget = VideoPlayerWidget()
        self.videoPlayerWidget.setHintText("未加载视频")
        self.videoPlayerWidget.setFrameReadEvent(self.modelManager.onFrameRead)
        
        # chartWidget
        self.chartWidget = MyChartWidget()
        self.modelManager.setChartWidget(self.chartWidget)
        self.chartWidget.output.connect(self.uploadData)

        leftSplitter.addWidget(self.videoPlayerWidget)
        leftSplitter.addWidget(self.chartWidget)
        # print(leftSplitter.children())

        leftSplitter.setStretchFactor(0, 1)
        leftSplitter.setStretchFactor(1, 2)
        leftSplitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # rightBoxWidget
        rightBoxWidget = QWidget(self.splitter)
        rightBox = QVBoxLayout(rightBoxWidget)
        rightBox.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(rightBoxWidget)
        # subVideoButtonWidget
        self.subVideoButtons = SubVideoButtonsWidget(self.videoPlayerWidget, self.modelManager)
        self.subVideoButtons.connectChartsWidget(self.chartWidget)
        self.subVideoButtons.upload.connect(self.uploadData)
        self.subVideoButtons.clear.connect(self.clearData)
        rightBox.addWidget(self.subVideoButtons)
        # captureAreaWiget
        self.captureAreaWidget = CaptureAreaWidget()
        rightBox.addWidget(self.captureAreaWidget)
        self.subVideoButtons.connectCaptureAreaWidget(self.captureAreaWidget)

        
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        

    def onModelTimer(self):
        self.modelManager.activate_network()


    def showResult(self, img_path:str, time:str, state:str, old:int, new:int):
        # logger.debug("output: "+img_path)
        # logger.debug(time + state)
        self.captureAreaWidget.addCaptureItem(img_path, time, state, old, new)# scrollAreaLayout.addWidget(item)

        # print(len(self.captureAreaWidget.children()))

    def uploadData(self):
        li = self.chartWidget.getData()
        tb = self.captureAreaWidget.getData()
    
        data = {
            'datas': li,
            'captures': tb
        }
        # print(data)
        res = postReportAPI(data)
        # print(res)


    def clearData(self):
        self.chartWidget.clean_datas()
        self.captureAreaWidget.cleanAll()