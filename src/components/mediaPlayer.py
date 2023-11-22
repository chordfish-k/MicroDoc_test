from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *
from PySide6.QtCore import *
from src.components.myQWidget import MyQWidget


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class MediaPlayer(MyQWidget):
    audio_output: QAudioOutput = None
    player: QMediaPlayer = None
    wgt_video: QVideoWidget = None

    # 播放状态
    isLoaded = False
    isPlaying = False
    isOpenedCamera: bool = False

    # 是否按下滑动条
    sld_video_pressed = None

    path = None

    loaded = Signal(int)
    stopped = Signal()
    positionChanged = Signal(int)

    def __init__(self):
        super().__init__()

    def initComponents(self):
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.wgt_video = QVideoWidget(self)
        self.player.setVideoOutput(self.wgt_video)
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self.changePosition)

        ly = QHBoxLayout()
        ly.setContentsMargins(0, 0, 0, 0)
        ly.addWidget(self.wgt_video)
        self.setLayout(ly)

        def status_changed(state):
            if state == QMediaPlayer.MediaStatus.LoadedMedia:
                self.loaded.emit(self.player.duration())
                print(self.player.subtitleTracks())
                if tracks := self.player.subtitleTracks():
                    for index, track in enumerate(tracks):
                        print(f'Track ({index}):')
                        for key in track.keys():
                            print(f'  {track.metaDataKeyToString(key)} = '
                                  f'{track.stringValue(key)}')
                    self.player.setActiveSubtitleTrack(0)
                    print("Active:", 0)
                else:
                    print('No subtitle tracks')
            if state == QMediaPlayer.MediaStatus.EndOfMedia:
                # self.stopped.emit()
                self.pause()

        self.player.mediaStatusChanged.connect(status_changed)

    def moveSlider(self, positionVal):
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((positionVal / 100) * self.player.duration())
            self.player.setPosition(video_position)

    def pressSlider(self):
        self.sld_video_pressed = True

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changePosition(self, position):
        self.positionChanged.emit(position)

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()

    def getDuration(self):
        return self.player.duration()

    ########## 重载 #############
    def load(self, path):
        if self.isLoaded:
            self.stop()

        self.path = path
        url = QUrl.fromLocalFile(path.encode("utf-8"))
        self.player.setSource(url)
        self.isPlaying = False
        self.isLoaded = True

    def play(self):
        if self.isLoaded:
            self.isPlaying = True
            self.player.play()

    def stop(self):
        if self.isLoaded:
            self.isLoaded = False
            self.isPlaying = False
            if self.player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
                self.player.stop()

    def pause(self):
        if self.isLoaded and self.isPlaying:
            self.isPlaying = False
            self.player.pause()

    def setProgress(self, value):
        self.player.setPosition(value)
