from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog
from PySide6.QtCore import QDir, Signal
from .myChart import MyChartWidget
from .eegChartGroup import EEGChartGroup
from .captureArea import CaptureAreaWidget
from src.components import VideoPlayerWidget, MyQWidget
from src.util.settings import settings
from src.util.logger import logger
from src.util.share import ObjectManager
from src.model.manager import ModelManager
import os


class SubVideoButtonsWidget(MyQWidget):
    window: QMainWindow = None

    svBtnFile: QPushButton = None
    svBtnActive: QPushButton = None
    svBtnUpload: QPushButton = None
    svBtnClear: QPushButton = None

    videoWidget: VideoPlayerWidget = None
    charts: MyChartWidget = None
    eegChartGroup: EEGChartGroup = None
    captureArea: CaptureAreaWidget = None

    # model manager
    modelManager: ModelManager = None

    upload = Signal()
    clear = Signal()

    def __init__(self, videoWidget, manager):
        self.window = ObjectManager.get("window")
        self.window.loginned.connect(self.onLoginned)
        self.window.logouted.connect(self.onLogouted)

        self.videoWidget = videoWidget
        self.modelManager = manager

        super().__init__(name="sub_video_buttons")

    def initComponents(self):
        self.svBtnFile.clicked.connect(self.toggleFile)
        self.svBtnActive.clicked.connect(self.toggleActive)
        self.svBtnUpload.clicked.connect(self.doUpload)
        self.svBtnClear.clicked.connect(self.doClear)

    def connectChartsWidget(self, charts):
        self.charts = charts

    def connectCaptureAreaWidget(self, capture):
        self.captureArea = capture

    def connectEEGChartGroup(self, eegChartGroup):
        self.eegChartGroup = eegChartGroup
        self.modelManager.setEEGChartGroup(self.eegChartGroup)

    def toggleFile(self):
        # logger.debug('toggle file-----------------------')

        if not self.videoWidget.isLoaded:
            # 默认打开存放录制视频的文件夹
            last_path = settings.get('last_dir_path')
            if not last_path:
                last_path = "videos"

            logger.debug("last_path: " + last_path)
            current_path = QDir.currentPath() if not last_path else last_path

            # 选择视频
            title = '选择视频文件'
            filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
            file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
            if file_path:
                # 存储上次打开的文件夹路径
                path = os.path.dirname(file_path)
                # print(path)
                settings.setItem('last_dir_path', path)
                settings.save()

                self.videoWidget.load(file_path)

            # 选择mat文件
            current_path = os.path.join(settings.get("eeg_folder"), "output", "cleaned_raw")
            title = '选择脑电数据文件'
            filt = "NPY文件(*.npy);"
            file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
            if file_path:
                # TODO 启动图表
                self.eegChartGroup.setNpyDataSource(file_path)

            # 播放视频
            self.charts.cleanDatas()
            self.captureArea.cleanAll()
            self.eegChartGroup.cleanAll()
            self.videoWidget.play()

        else:
            self.videoWidget.stop()

        self.svBtnFile.setText(
            "关闭本地文件" if self.videoWidget.isLoaded else "打开本地文件")

    def toggleActive(self):
        if not self.modelManager.modelActive:
            self.modelManager.modelActive = True
        else:
            self.modelManager.modelActive = False

        self.svBtnActive.setText(
            "停止模型" if self.modelManager.modelActive else "启动模型")

    def doUpload(self):
        # 判断是否登录
        if not settings.get("token"):
            return
        # 发送信号
        self.upload.emit()

    def doClear(self):
        self.clear.emit()

    def onLoginned(self):
        self.svBtnUpload.setDisabled(False)

    def onLogouted(self):
        self.svBtnUpload.setDisabled(True)


