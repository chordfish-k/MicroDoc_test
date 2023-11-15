from PySide6.QtWidgets import QMainWindow, QLabel, QCheckBox, QPushButton, QFileDialog, QSizePolicy
from PySide6.QtCore import QDir
import os
import cv2
import datetime
from components import VideoControllerWidget, VideoPlayerWidget, MyQWidget
from util.settings import settings
from util.logger import logger


class SubToolsWidget(MyQWidget):
    window: QMainWindow = None

    stBtnStartRecord: QPushButton = None
    stBtnChooseSubVideo: QPushButton = None
    stCbCamera: QCheckBox = None
    stCbNao: QCheckBox = None
    stLbCurrFile: QLabel = None

    videoWidget: VideoPlayerWidget = None
    subVideoWidget: VideoPlayerWidget = None
    videoBar: VideoControllerWidget = None

    isRecording: bool = False
    videoOut: cv2.VideoWriter = None


    def __init__(self, window, videoWidget, subVideoWidget, videoBar):
        self.window = window
        self.videoWidget = videoWidget
        self.subVideoWidget = subVideoWidget
        self.videoBar = videoBar

        super().__init__(name="sub_tools")


    def initComponents(self):
        self.stBtnChooseSubVideo.clicked.connect(self.toggleFile)
        self.stCbCamera.clicked.connect(self.toggleCamera)
        self.stBtnStartRecord.clicked.connect(self.toggleRecord)
        self.subVideoWidget.setFrameReadEvent(self.captureFrame)
        self.videoWidget.stopped.connect(self.toggleFile)

        self.stLbCurrFile.setWordWrap(True)
        

    def toggleCamera(self):
        logger.debug('toggle camera')
        self.subVideoWidget.toggleCamera()

    def toggleRecord(self):
        if self.isRecording:
            self.stopRecord()
            self.stBtnStartRecord.setText("开始录制")
        else:
            self.startRecord()
            self.stBtnStartRecord.setText("停止录制")


    def openVideoFile(self):
        last_path = settings.get('last_dir_path')
        logger.debug("last_path: " + last_path)
        current_path = QDir.currentPath() if not last_path else last_path
        title = '选择视频文件'
        filt = "视频文件(*.wmv *avi *.mp4 *.mov);;所有文件(*.*)"
        file_path, filt = QFileDialog.getOpenFileName(self, title, current_path, filt)
        file_name = os.path.split(file_path)[-1]
        
        if file_path:
            # 存储上次打开的文件夹路径
            path = os.path.dirname(file_path)
            settings.setItem('last_dir_path', path)
            settings.save()
            logger.debug("this_path: " + file_path)
            return file_path, file_name
        else:
            return None, None


    def toggleFile(self):
        logger.debug('toggle file')

        if not self.videoWidget.isLoaded:
            path, name = self.openVideoFile()
            if path:
                self.videoWidget.load(path)
                #self.videoWidget.setPlayMode(
                # videoPlayer.VideoPlayerWidget.PlayMode.LOOP)
                self.stLbCurrFile.setText(f"当前文件：{name}")

        else:
            self.videoBar.onStopBtnPress()
            self.stLbCurrFile.setText("当前文件：无")

        self.stBtnChooseSubVideo.setText(
            "关闭本地文件" if self.videoWidget.isLoaded else "打开本地文件")


    ## 开始录制
    def startRecord(self):
        self.isRecording = True

        if not self.subVideoWidget.isOpenedCamera:
            return

        # 新建一个视频文件
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        video_path = os.path.join('videos', str(time_str) + '.avi')
        # print(video_path)

        self.videoOut = cv2.VideoWriter(video_path, self.fourcc, settings.get("capture_video_fps", float), (640, 480))

    ## 停止录制
    def stopRecord(self):
        self.isRecording = False

        if not self.subVideoWidget.isOpenedCamera:
            return
            # 释放画面缓存
        self.videoOut.release()
        self.videoOut = None

        # 重置计数器
        # self.output_counter = 0


    def captureFrame(self, _, __):
        # 将画面写入文件
        if not self.subVideoWidget.isOpenedCamera:
            return
        if self.isRecording and self.videoOut:
                ret, readFrame = self.subVideoWidget.video.capture.read()
                self.videoOut.write(readFrame)