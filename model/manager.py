import os
from PIL import Image, ImageQt
import cv2
import numpy as np
import torch
from torchvision import transforms
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage

from model.face_cut.face_cut import FaceCut
from util.logger import logger


class Manager:
    img_pool = []
    min_prob = 0.3
    pre_result = "None"

    
    modelTimer: QTimer = None
    modelActive = False
    modelManager = None

    fc: FaceCut = FaceCut()


    def __init__(self, settings):
        self.settings = settings

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
        self.min_prob = float(self.settings.get("min_accepted_probability"))

        # 表情捕获文件夹
        self.captures_path = "./captures/"
        # 视频录制文件夹
        self.videos_path = "./videos/"

        if (not os.path.exists(self.captures_path)):
            os.mkdir(self.captures_path)

        if (not os.path.exists(self.videos_path)):
            os.mkdir(self.videos_path)

    def softmax(self, tensor):
            array = tensor.cpu().numpy()
            exp_a = np.exp(array)
            sum_exp_a = np.sum(exp_a)
            result = exp_a / sum_exp_a
            return result
    
    
    # 加载3分类模型
    def load_model(self):
        model_path = "model/test/model.pth"
        if self.settings.get('use_gpu'):
            if torch.cuda.is_available():
                logger.warning('No CUDA gpu is available, switch to cpu')
                self.swin_trans = torch.load(model_path, map_location=torch.device('cuda'))
            else:
                self.swin_trans = torch.load(model_path, map_location=torch.device('cpu'))
        else:
            self.swin_trans = torch.load(model_path, map_location=torch.device('cpu'))

        if torch.cuda.is_available():
            self.swin_trans = self.swin_trans.cuda()


    def addImage(self, img):
        self.img_pool.append(img)


    def onFrameRead(self, image):
        rects = self.fc.face_cut(image)
        
        if rects != ():
            img_patch = []
            for i, (x, y, w, h) in enumerate(rects):

                try:
                    img_patch = image[y - h // 4:y + h + h // 4,
                                x - w // 4:x + w + w // 4, :]
                    img_patch = cv2.resize(img_patch, (128, 128))
                except:
                    img_patch = image[y:y + h, x:x + w, :]

                    img_patch = cv2.resize(img_patch, (128, 128))

            height, width, channel = img_patch.shape
            qImg = QImage(img_patch.data, height, width,
                            QImage.Format.Format_RGB888).rgbSwapped()
            qImg = ImageQt.fromqimage(qImg)
            
            self.addImage(qImg)


    # 多线程激活网络
    def activate_network(self):
        if self.img_pool == []:
            return
        
        img = self.img_pool[0]  # 顺序第一张
        self.img_pool = self.img_pool[1:]

        if (not img):
            return

        img = self.transform_test(img)

        if torch.cuda.is_available():
            img = img.cuda()  # 转成cuda数据类型
        img = torch.reshape(img, (1, 3, 224, 224))

        output = self.swin_trans(img)
        # print(output)
        with torch.no_grad():
            result = self.softmax(output[0])
            logger.debug(result)
            self.global_result = result
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
