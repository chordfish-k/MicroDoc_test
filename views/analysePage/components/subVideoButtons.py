from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog
from PySide6.QtCore import QDir, Signal
import os
from components import VideoPlayerWidget
from components.myQWidget import MyQWidget
from util.settings import settings
from util.logger import logger
from util.share import ObjectManager


class SubVideoButtonsWidget(MyQWidget):
    window: QMainWindow = None

    svBtnFile: QPushButton = None
    svBtnActive: QPushButton = None
    svBtnUpload: QPushButton = None
    svBtnClear: QPushButton = None

    videoWidget: VideoPlayerWidget = None

    # model manager
    manager = None

    upload = Signal()
    clear = Signal()


    def __init__(self, videoWidget, manager):
        self.window = ObjectManager.get("window")
        self.window.loginned.connect(self.onLoginned)
        self.window.logouted.connect(self.onLogouted)

        self.videoWidget = videoWidget
        self.manager = manager

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


    def toggleCamera(self):
        logger.debug('toggle camera')
        self.videoWidget.toggleCamera()
        self.svBtnCamera.setText(
            "关闭摄像头" if self.videoWidget.isOpenedCamera else "打开摄像头")


    def toggleFile(self):
        logger.debug('toggle file-----------------------')

        if not self.videoWidget.isLoaded:
            # 默认打开存放录制视频的文件夹
            last_path = settings.get('last_dir_path')
            if not last_path:
                last_path = "videos"

            logger.debug("last_path: " + last_path)
            current_path = QDir.currentPath() if not last_path else last_path
            title = '选择视频文件'
            filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
            file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
            if file_path:
                
                # 存储上次打开的文件夹路径
                path = os.path.dirname(file_path)
                print(path)
                settings.setItem('last_dir_path', path)
                settings.save()

                self.videoWidget.load(file_path)
                self.videoWidget.play()
                
                self.charts.clean_datas()
                self.captureArea.cleanAll()
        else:
            self.videoWidget.stop()

        self.svBtnFile.setText(
            "关闭本地文件" if self.videoWidget.isLoaded else "打开本地文件")
        

    def toggleActive(self):
        if not self.manager.modelActive:
            self.manager.modelActive = True
        else:
            self.manager.modelActive = False

        self.svBtnActive.setText(
            "停止模型" if self.manager.modelActive else "启动模型")


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