import os
from PIL import ImageQt
import cv2
import numpy as np
import torch
from queue import Queue
from torchvision import transforms
from PySide6.QtCore import QTimer, QDir
from PySide6.QtGui import QImage

from src.model.face_cut.face_cut import FaceCut
from src.util.logger import logger
from src.util.settings import settings
from src.util.share import ObjectManager


class ModelManager:
    img_que = Queue(maxsize=100)
    min_prob = 0.3
    pre_result = "None"
    pre_result_i = -1

    modelTimer: QTimer = None
    modelActive = False
    modelManager = None

    # 帧读取的间隔
    duration = 4
    durationCnt = 0

    fc: FaceCut = FaceCut()

    outputFn = None
    chart = None
    eegChartGroup = None

    def __init__(self):
        self.min_prob = settings.get('min_accepted_probability', float)
        self.duration = settings.get('output_duration', int)

        self.transform_test = transforms.Compose(
            [
                transforms.Resize([224, 224]),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])

        self.test_dir = {0: "negative", 1: "neutral", 2: "positive"}

        # 创建模型对象
        self.swin_trans = torch.nn.Module
        # 加载模型
        self.load_model()
        # 
        self.min_prob = settings.get("min_accepted_probability", float)

        # 表情捕获文件夹
        self.captures_path = os.path.join(QDir.currentPath(), "captures")
        # 视频录制文件夹
        self.videos_path = os.path.join(QDir.currentPath(), "videos")

        if not os.path.exists(self.captures_path):
            os.mkdir(self.captures_path)

        if not os.path.exists(self.videos_path):
            os.mkdir(self.videos_path)

    def setOutputFn(self, fn):
        self.outputFn = fn

    def setChartWidget(self, chart):
        self.chart = chart

    def setEEGChartGroup(self, chartgroup):
        self.eegChartGroup = chartgroup

    def softmax(self, tensor):
        array = tensor.cpu().numpy()
        exp_a = np.exp(array)
        sum_exp_a = np.sum(exp_a)
        result = exp_a / sum_exp_a
        return result

    # 加载3分类模型
    def load_model(self):
        model_path = settings.get("model_path")
        device = torch.device('cpu')
        if settings.get('use_gpu', bool):
            if torch.cuda.is_available():
                device = torch.device('cuda:0')
            else:
                logger.warning('CUDA gpu is not available, switch to cpu')
                device = torch.device('cpu')

        self.swin_trans = ObjectManager.get("swin_trans")
        if not self.swin_trans:
            self.swin_trans = torch.load(model_path, map_location=device)
            ObjectManager.set("swin_trans", self.swin_trans)
            logger.debug(f'model is running on {device}')

    def addImage(self, img, time):
        self.img_que.put((img, time))

    def onFrameRead(self, image, time):
        if not self.modelActive:
            return

        if self.durationCnt == 0 and image.any:
            self.addImage(image, time)

        self.durationCnt += 1
        if self.durationCnt == self.duration:
            self.durationCnt = 0

    # 多线程激活网络
    def activate_network(self):
        if not self.modelActive:
            return

        if self.img_que.empty():
            return

        img, time = self.img_que.get()  # 顺序第一张
        rects = self.fc.face_cut(img)

        if type(rects) is None or len(rects) == 0:
            # 输出数据
            if self.chart:
                self.chart.repeatLast()
            if self.eegChartGroup:
                self.eegChartGroup.updateData()
            return

        for _, (x, y, w, h) in enumerate(rects):
            try:
                img_patch = img[y - h // 4:y + h + h // 4,
                            x - w // 4:x + w + w // 4, :]
                img_patch = cv2.resize(img_patch, (128, 128))
            except Exception as e:
                try:
                    img_patch = img[y:y + h, x:x + w, :]
                    img_patch = cv2.resize(img_patch, (128, 128))
                except Exception as e:
                    logger.warn(str(e).split("\n")[0])
                    if self.chart:
                        self.chart.repeatLast()
                    if self.eegChartGroup:
                        self.eegChartGroup.updateData()
                    break

            height, width, channel = img_patch.shape
            qImg = QImage(img_patch.data, height, width,
                          QImage.Format.Format_RGB888).rgbSwapped()

            img = ImageQt.fromqimage(qImg)
            img = self.transform_test(img)

            if torch.cuda.is_available():
                img = img.cuda()  # 转成cuda数据类型
            img = torch.reshape(img, (1, 3, 224, 224))

            output = self.swin_trans(img)

            with torch.no_grad():
                result = self.softmax(output[0])
                # 输出数据
                result_probability = np.max(result)
                if result_probability <= self.min_prob:
                    if self.chart:
                        self.chart.repeatLast()
                    if self.eegChartGroup:
                        self.eegChartGroup.updateData()
                    break

                if self.chart:
                    self.chart.updateSeries(result)
                if self.eegChartGroup:
                    self.eegChartGroup.updateData()

                # 输出结果
                result_item = result.argmax(0)
                result_txt = self.test_dir[result_item]

                # 表情发生变化
                if result_txt == self.pre_result:
                    break
                result_change_txt = self.pre_result + "=>" + result_txt
                self.pre_result = result_txt

                if self.outputFn:
                    date = time
                    file = os.path.join(self.captures_path, str.replace(time, ':', '') + '.jpg')
                    cv2.imwrite(file, img_patch)
                    self.outputFn(file, date, result_change_txt, self.pre_result_i, result_item)

                self.pre_result_i = result_item
