from PySide6.QtWidgets import QMainWindow, QWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtCore import QTimer
import os
import cv2
import time
import numpy as np
from assets.assets_loader import Assets


class VideoPlayerWidget(QWidget):

####[class Video start]###########################################################
    
    class Video:
        VIDEO_WIDTH = 640
        window: QMainWindow = None
        # 屏幕标签
        screen_label: QLabel = None
        # 播放用timer
        timer: QTimer = None  
        # 播放状态
        isPlaying: bool = False

        
        def __init__(self, window, path, screen_label):
            self.screen_label = screen_label
            self.window = window

            # 读取视频数据
            self.capture = cv2.VideoCapture(path)
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

            # 初始化计时器
            self.timer = QTimer(self.window)
            self.timer.timeout.connect(self.nextFrame)  # timeout时，执行show_pic



        def captureNextFrame(self):
            ret, readFrame = self.capture.read()
            if (ret == True):
                h = int(self.height * self.VIDEO_WIDTH / self.width) #调整画面大小以适应控件
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

                if pic:
                    view = self.screen_label

                    k1 = pic.width() / pic.height()
                    k2 = view.width() / view.height()
                    tmp = None
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

                # 显示时间
                # self.__ui.label_curTime.setText(self.video.str_current_time)
                # self.__ui.label_endTime.setText(self.video.str_end_time)
                # self.__ui.horizontalSlider.setValue(self.video.frame_now)

                if (self.frame_count == self.frame_now):
                    # 播放到结尾，停止播放
                    self.setVideoSecondPosition(0)
                    # 重置计数器
                    # self.output_counter = 0
                    # self.on_pushButton_start_pressed()
            except TypeError:
                print('No Frame')
                # self.timer_player.stop()

########[class Video end]######################################################################

    window: QMainWindow
    video: Video
    video_zoom: QLabel

    def __init__(self, window):
        super().__init__()
        self.window = window

        Assets.loadUi('video_player', self)
        # Assets.loadQss('video_player', self)

        self.initComponents()


    def initComponents(self):
        self.video_zoom = self.ui.video_zoom


    def load(self, path):
        self.video = self.Video(self.window, path, self.video_zoom)
        self.play()



    def play(self):
        self.video.timer.start(int(1000 / self.video.fps))


    def stop(self):
        pass


    def pause(self):
        pass


    def clear(self):
        pass


    def setProgress(self, value):
        pass


    def getProgress(self, value):
        pass



