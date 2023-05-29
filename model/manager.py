import datetime
import os
from PIL import Image, ImageQt
import cv2
import numpy as np
import torch
from queue import Queue
from torchvision import transforms
from PySide6.QtCore import QTimer, Signal, QDir
from PySide6.QtGui import QImage

from views.components.myChart import MyChartWidget
from model.face_cut.face_cut import FaceCut
from util.logger import logger
from util.settings import Settings


class Manager:
    settings:Settings = None

    img_que = Queue(maxsize=100)
    min_prob = 0.3
    pre_result = "None"
    
    modelTimer: QTimer = None
    modelActive = False
    modelManager = None

    # 帧读取的间隔
    duration = 4
    durationCnt = 0

    fc: FaceCut = FaceCut()

    outputFn = None

    chart: MyChartWidget = None

    # timer: QTimer = None
    # timerRunning: False


    def __init__(self, settings):
        self.settings = settings
        self.min_prob = self.settings.get('min_accepted_probability', float)
        self.duration = self.settings.get('output_duration', int)

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
        self.min_prob = self.settings.get("min_accepted_probability", float)

        # 表情捕获文件夹
        self.captures_path = os.path.join(QDir.currentPath(),  "captures")
        # 视频录制文件夹
        self.videos_path = os.path.join(QDir.currentPath(),  "videos")

        if (not os.path.exists(self.captures_path)):
            os.mkdir(self.captures_path)

        if (not os.path.exists(self.videos_path)):
            os.mkdir(self.videos_path)


        # self.timer = QTimer()
        # self.timer.timeout.connect(self.activate_network)

    def setOutputFn(self, fn):
        self.outputFn = fn

    def setChartWidget(self, chart):
        self.chart = chart

    def softmax(self, tensor):
        array = tensor.cpu().numpy()
        exp_a = np.exp(array)
        sum_exp_a = np.sum(exp_a)
        result = exp_a / sum_exp_a
        return result
    
    
    # 加载3分类模型
    def load_model(self):
        model_path = "model/test/model.pth"
        device = torch.device('cpu')
        if self.settings.get('use_gpu', bool):
            if torch.cuda.is_available():
                device = torch.device('cuda:0')
            else:
                logger.warning('CUDA gpu is not available, switch to cpu')
                device = torch.device('cpu')
        logger.debug(f'model is running on {device}')
        self.swin_trans = torch.load(model_path, map_location=device)

    def addImage(self, img):
        self.img_que.put(img)


    def onFrameRead(self, image):
        if self.durationCnt == 0 and image.any:
            self.addImage(image)

        self.durationCnt += 1
        if self.durationCnt == self.duration:
            self.durationCnt = 0


    


    # 多线程激活网络
    def activate_network(self):
        if self.img_que.empty() or not self.modelActive:
            #logger.debug("empty")
            return
        #logger.debug(str(self.img_que.qsize()))
        #logger.debug("ok")
        
        img = self.img_que.get()  # 顺序第一张

        rects = self.fc.face_cut(img)


        if rects != ():
            for _, (x, y, w, h) in enumerate(rects):
                try:
                    img_patch = img[y - h // 4:y + h + h // 4,
                                x - w // 4:x + w + w // 4, :]
                    img_patch = cv2.resize(img_patch, (128, 128))
                # except:
                #     img_patch = img[y:y + h, x:x + w, :]
                #     img_patch = cv2.resize(img_patch, (128, 128))

                    height, width, channel = img_patch.shape
                    qImg = QImage(img_patch.data, height, width,
                                    QImage.Format.Format_RGB888).rgbSwapped()
                    
                    img = ImageQt.fromqimage(qImg)
                    img = self.transform_test(img)

                    if torch.cuda.is_available():
                        img = img.cuda()  # 转成cuda数据类型
                    img = torch.reshape(img, (1, 3, 224, 224))

                    output = self.swin_trans(img)
                    # print(output)
                    with torch.no_grad():
                        result = self.softmax(output[0])
                        #logger.debug(result)
                        if self.chart:
                            self.chart.update_series(result)
                        # self.global_result = [random.random(), random.random(), random.random()]
                        # print(self.global_result)
                        result_probability = np.max(result)
                        # print("result_probability:{}".format(result_probability))
                        if result_probability > self.min_prob:
                            # 输出结果
                            result_item = result.argmax(0)
                            result_txt = self.test_dir[result_item]

                            # 表情发生变化
                            if result_txt != self.pre_result:
                                result_change_txt = self.pre_result + "=>" + result_txt
                                self.pre_result = result_txt

                                #path1 = os.path.join(self.frames_path, image_dirs[0])
                                #path2 = os.path.join(self.captures_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg')
                                #shutil.copyfile(path1, path2) # 将捕获到表情的帧移动到captures文件夹

                                
                                # self.add_new_result(path2, self.get_date(), result_change_txt)

                                def get_date(mode = 0):
                                    if mode == 0:
                                        return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    else:
                                        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                                
                                date = get_date()
                                file = os.path.join(self.captures_path, get_date(1) + '.jpg')
                                cv2.imwrite(file, img_patch)
                                self.outputFn(file, date, result_change_txt)

                except:
                    pass
