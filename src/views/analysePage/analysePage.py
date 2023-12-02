from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt, QTimer
from src.api.report import postReportAPI
from .components import CaptureAreaWidget, MyChartWidget, SubVideoButtonsWidget, EEGChartGroup
from src.components import StackPage, VideoControllerWidget, VideoPlayerWidget
from src.model.manager import ModelManager
from src.util.share import ObjectManager
from src.util.logger import logger


class AnalysePageWidget(StackPage):
    window: QMainWindow = None
    splitter: QSplitter = None

    videoPlayerWidget: VideoPlayerWidget = None
    videoControllerWidget: VideoControllerWidget = None
    subVideoButtons: SubVideoButtonsWidget = None
    captureAreaWidget: CaptureAreaWidget = None
    chartWidget: MyChartWidget = None
    eegChartGroup: EEGChartGroup = None

    modelTimer1: QTimer = None

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
        self.videoPlayerWidget = VideoPlayerWidget()
        self.videoPlayerWidget.setHintText("未加载视频")
        self.videoPlayerWidget.setFrameReadEvent(self.modelManager.onFrameRead)

        # eegChartGroup
        self.eegChartGroup = EEGChartGroup()

        # chartWidget
        self.chartWidget = MyChartWidget()
        self.modelManager.setChartWidget(self.chartWidget)
        self.chartWidget.output.connect(self.uploadData)

        # leftSplitter.addWidget(self.videoPlayerWidget)
        leftSplitter.addWidget(self.eegChartGroup)
        leftSplitter.addWidget(self.chartWidget)
        # print(leftSplitter.children())

        leftSplitter.setStretchFactor(0, 1)
        leftSplitter.setStretchFactor(1, 2)
        leftSplitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # rightSplitter(ver)
        rightSplitter = QSplitter(self.splitter)
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(rightSplitter)

        # rightBoxWidget
        rightBoxWidget = QWidget(self.splitter)
        rightBox = QVBoxLayout(rightBoxWidget)
        rightBox.setContentsMargins(0, 0, 0, 0)

        rightSplitter.addWidget(self.videoPlayerWidget)
        # self.videoPlayerWidget.setMinimumHeight(400)
        # subVideoButtonWidget
        self.subVideoButtons = SubVideoButtonsWidget(self.videoPlayerWidget, self.modelManager)
        self.subVideoButtons.connectChartsWidget(self.chartWidget)
        self.subVideoButtons.connectEEGChartGroup(self.eegChartGroup)
        self.subVideoButtons.upload.connect(self.uploadData)
        self.subVideoButtons.clear.connect(self.clearData)
        rightBox.addWidget(self.subVideoButtons)

        # captureAreaWidget
        self.captureAreaWidget = CaptureAreaWidget()
        rightBox.addWidget(self.captureAreaWidget)
        rightSplitter.addWidget(rightBoxWidget)

        rightSplitter.setStretchFactor(0, 1)
        rightSplitter.setStretchFactor(1, 5)
        rightSplitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self.subVideoButtons.connectCaptureAreaWidget(self.captureAreaWidget)
        # self.splitter.addWidget(rightSplitter)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.handle(1).setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def onModelTimer(self):
        self.modelManager.activate_network()

    def showResult(self, img_path: str, time: str, state: str, old: int, new: int):
        self.captureAreaWidget.addCaptureItem(img_path, time, state, old, new)

    def uploadData(self):
        li = self.chartWidget.getData()
        eeg = self.eegChartGroup.getData()
        tb = self.captureAreaWidget.getData()

        data = {
            'datas': li+eeg,
            'captures': tb
        }
        # print(li)
        # print(eeg)
        # print(data)

        res = postReportAPI(data)
        # print(res)
        if res['code'] == 1:
            logger.info(f"数据上传成功，报告id为{res['data']}")

    def clearData(self):
        self.chartWidget.cleanDatas()
        self.captureAreaWidget.cleanAll()
        self.eegChartGroup.cleanAll()
