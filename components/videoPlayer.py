from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QSlider, QWidget,QApplication
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, QThread, Signal
import cv2
import time
import numpy as np
from assets.assets_loader import Assets
from components.myQWidget import MyQWidget
from util.logger import logger
from util.settings import settings
from util.share import ObjectManager


class VideoPlayerWidget(QWidget):

    window: QMainWindow = None
    video = None
    video_zoom: QLabel = None
    hint_text: str = 'no rescource'

    controller: None
    hasController = False

    path: str = ""

    # 播放状态
    isLoaded = False
    isPlaying = False
    isOpenedCamera: bool = False

    stopped: Signal = Signal()
    
    class PlayMode:
            ONCE = 0
            LOOP = 1
            
    playMode: PlayMode = PlayMode.ONCE
####[class Video start]###########################################################
    
    class Video:

        VIDEO_WIDTH = 640

        widget = None
        window: QMainWindow = None


        path: str = ""
        # 屏幕标签
        screen_label: QLabel = None
        # 播放视频timer
        timer: QTimer = None
        # 播放音频timer
        # audio_thread: QThread = None
        # 是否为视频文件
        isFile = True

        # 帧获取事件
        frameReadEvent = None

        flipX = False
        
        def __init__(self, widget, window, pathOrCamera, screen_label):
            """
            window: 主窗口
            pathOrCamera: 视频路径或摄像头序号
            screen_label: 作为图像载体的QLabel
            """
            self.screen_label = screen_label
            self.widget = widget
            self.window = window

            if type(pathOrCamera) is str:
                self.isFile = True
                self.path = pathOrCamera
                # self.audio_player = MediaPlayer(self.path)
            else:
                self.isFile = False

            self.flipX = settings.get('camera_flipX', bool)

            # 读取视频数据
            self.capture = cv2.VideoCapture(pathOrCamera)
            self.currentFrame = np.array([])
            self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) #获取视频的信息（宽，高，帧速率）
            self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
            self.fps = 24 if self.fps == 0 else self.fps
            self.frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)) #帧数
            self.frame_now = 0
            self.current_time = 0
            self.total_time = int(self.frame_count / self.fps)
            self.str_current_time = "00:00"

            t = time.gmtime(self.total_time)
            self.str_end_time = '{:02d}' .format(int(time.strftime("%H", t))*60 + int(time.strftime("%M", t))) + time.strftime(":%S", t)

            #else:
            #    self.capture = cv2.VideoCapture(path)

            # 初始化计时器
            self.timer = QTimer()
            self.timer.timeout.connect(self.nextFrame)  # timeout时，执行show_pic
            
            # 设置进度条最大值
            if self.widget.hasController:
                self.widget.controller.videoSlider.setMaximum(self.frame_count)


        def captureNextFrame(self):
            ret, readFrame = self.capture.read()

            if (ret == True):
                # 如果是摄像头 且 设置了水平翻转
                if not self.isFile and self.flipX:
                        cv2.flip(readFrame, 1, readFrame)

                    

                h = int(self.height * self.VIDEO_WIDTH / self.width) #调整画面大小以适应控件
                # 将当前帧复制到currentFrame
                self.currentFrame = readFrame #cv2.resize(readFrame, (VIDEO_WIDTH, h))
                self.frame_now = int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
                self.current_time = int(self.capture.get(cv2.CAP_PROP_POS_MSEC)/1000)
                t = time.gmtime(self.current_time)
                self.str_current_time = '{:02d}' .format(int(time.strftime("%H", t))*60 + int(time.strftime("%M", t))) + time.strftime(":%S", t)

                #print(self.str_current_time, " ", self.str_end_time)
                

        def convertFrame(self):
            try:
                height, width, channel = self.currentFrame.shape
                bytesPerLine = 3 * width

                qImg = QImage(self.currentFrame.data, width, height, 
                                QImage.Format.Format_RGB888).rgbSwapped()
                qImg = QPixmap.fromImage(qImg)

                return qImg
            except:
                return None
            

        def setVideoSecondPosition(self, s):
            self.capture.set(cv2.CAP_PROP_POS_MSEC, s * 1000)


        def setVideoFramePosition(self, s):
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, s)


        def showPic(self, pic: QPixmap):
            if self.screen_label:
                view = self.screen_label
                if pic:
                    k1 = pic.width() / pic.height()
                    k2 = view.width() / view.height()
                    tmp = pic
                    if k1 <= k2:
                        tmp = pic.scaledToHeight(view.height())
                    else:
                        tmp = pic.scaledToWidth(view.width())
                    view.setPixmap(tmp)
            

        # 计时器：获取下一帧并显示
        def nextFrame(self):

            try:
                self.captureNextFrame()
                tmp_frame = self.convertFrame()

                self.showPic(tmp_frame)

                if self.frame_count == self.frame_now:
                    
                    # 播放到结尾，重新开始
                    if self.widget.playMode == self.widget.PlayMode.LOOP:
                        self.setVideoSecondPosition(0)
                    elif self.widget.playMode == self.widget.PlayMode.ONCE:
                        self.widget.stopped.emit()
                        

            except TypeError:
                logger.warning('No Frame')

            # 传递给事件
            if self.frameReadEvent:
                #logger.debug(self.str_current_time)
                self.frameReadEvent(self.currentFrame.copy(), self.str_current_time)


            # 设置进度条
            if self.widget.hasController:
                self.widget.controller.lbCurrTime.setText(self.str_current_time)
                self.widget.controller.lbEndTime.setText(self.str_end_time)
                self.widget.controller.videoSlider.setValue(self.frame_now)

            # print(self.frame_now)

        def setFrameReadEvent(self, fn):
            self.frameReadEvent = fn



########[class Video end]######################################################################

    # 帧获取事件
    frameReadEvent = None

    def __init__(self):
        super().__init__()
        self.window = ObjectManager.get("window")

        Assets.loadUi('video_player', self)
        Assets.loadQss('video_player', self)

        self.initComponents()


    def initComponents(self):
        pass

    def load(self, path):
        if self.isLoaded:
            self.stop()
        elif self.isOpenedCamera:
            self.closeCamera()

        self.path = path

        self.video = self.Video(self, self.window, path, self.video_zoom)
        if self.frameReadEvent:
            self.video.setFrameReadEvent(self.frameReadEvent)
        self.isPlaying = False
        self.isLoaded = True


    def play(self):
        if self.isLoaded:
            logger.debug("fps: "+ str(self.video.fps))
            self.video.timer.start(1000//self.video.fps)
            self.isPlaying = True

            # if self.video.audio_player:
            #     self.video.audio_player.set_pause(False)



    def stop(self):
        if self.isLoaded:
            self.isLoaded = False
            self.isPlaying = False
            self.video.timer.stop()
            self.video.capture.release()
            del self.video
            self.video = None
            self.clearScreen()

            # if self.video.audio_player:
            #     self.video.audio_player.close_player()


    def pause(self):
        if self.isLoaded and self.isPlaying:
            self.video.timer.stop()
            self.isPlaying = False

            # if self.video.audio_player:
            #     self.video.audio_player.set_pause(True)


    def clearScreen(self):
        self.video_zoom.setPixmap(QPixmap())
        self.setHintText()


    def setProgress(self, value):
        if self.video:
            # logger.debug("value: " + str(value))
            self.video.capture.set(cv2.CAP_PROP_POS_FRAMES, value)


    def getProgress(self, value):
        pass


    def toggleCamera(self):
        if not self.isOpenedCamera:
            self.openCamera()
        else:
            self.closeCamera()


    def openCamera(self):
        self.video = self.Video(self, self.window, 0, self.video_zoom)
        if self.frameReadEvent:
            self.video.setFrameReadEvent(self.frameReadEvent)


        self.video.timer.start()
        self.isOpenedCamera = True

        # if settings.record_when_open_camera:
        #     self.start_record()

        # self.clean_datas() #清空图表

        # 禁用子视频窗口的按钮
        # self.__ui.pushButton_open_sub.setEnabled(False)
        # self.__ui.pushButton_stop_sub.setEnabled(False)


    def closeCamera(self):
        self.video.timer.stop()
        del self.video
        self.video = None
        self.clearScreen()
        self.isOpenedCamera = False


    def setController(self, controller):
        self.controller = controller
        self.hasController = True

    
    def setFrameReadEvent(self, fn):
        """
        fn: 方法名 (frame:numpy.ndarray)
        """
        self.frameReadEvent = fn

        if self.video:
            self.video.setFrameReadEvent(self.frameReadEvent)


    def setHintText(self, text:str=None):
        if text:
            self.hintText = text
        self.video_zoom.setText(self.hintText)


    def setPlayMode(self, mode: PlayMode):
        self.playMode = mode
        
    def getCurrentTime(self):
        return self.video.current_time if self.video else 0




class VideoControllerWidget(MyQWidget):
    window: QMainWindow = None

    btnStart: QPushButton = None
    btnStop: QPushButton = None
    videoSlider: QSlider = None
    lbCurrTime: QLabel = None
    lbEndTime: QLabel = None

    player: VideoPlayerWidget = None

    showStopBtn: bool = True


    def __init__(self, window):
        self.window = window
        super().__init__(name="video_controller")


    def initComponents(self):
        self.btnStart = self.ui.btnStart
        self.btnStop = self.ui.btnStop
        self.videoSlider = self.ui.videoSlider
        self.lbCurrTime = self.ui.lbCurrTime
        self.lbEndTime = self.ui.lbEndTime
        
    
    def attachVideoPlayer(self, videoPlayer):
        self.player = videoPlayer
        videoPlayer.setController(self)
        self.btnStart.clicked.connect(self.onPlayBtnPress)
        self.btnStop.clicked.connect(self.onStopBtnPress)
        self.videoSlider.sliderPressed.connect(self.onSliderPressed)
        self.videoSlider.sliderReleased.connect(self.onSliderRelease)

    
    def onPlayBtnPress(self):
        if self.player:
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
        else:
            logger.warning("videoPlayer is not found!")


    def setShowStopBtn(self, isShow):
        self.showStopBtn = isShow
        self.btnStop.setVisible(isShow)

    def onStopBtnPress(self):
        if self.player:
            if self.player.isLoaded:
                logger.debug("video stoped")
                self.player.stop()
                self.btnStart.setStyleSheet(
                        "background-image: url(:/icons/assets/images/icons/cil-media-play.png)")
            else:
                logger.warning("video file is not loaded!")
        else:
            logger.warning("videoPlayer is not found!")


    def onSliderPressed(self):
        if self.player:
            self.player.pause()


    def onSliderRelease(self):
        if self.player:
            # logger.debug("slider move")
            self.player.setProgress(self.videoSlider.value())
            self.player.play()


    def refresh(self):
        Assets.loadQss('video_controller', self)
        super().refresh()