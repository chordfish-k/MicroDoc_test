import cv2
import os
import numpy as np
from util.logger import logger
from PySide6.QtCore import QDir

class FaceCut:

    detector = None

    def __init__(self):
        path = QDir.currentPath()+ "/model/face_cut/haarcascade_frontalface_default.xml"
        self.detector = cv2.CascadeClassifier(path)

    def face_cut(self, image: np.ndarray, **kwargs)->np.ndarray|None:
        if self.detector == None:
            return
        
        scaleFactor = kwargs.get('scaleFactor') # 严格大于1，越小，出的框越多
        minNeighbors = kwargs.get('minNeighbors') # 越小，出的框越多
        minSize = kwargs.get('minSize')

        return self.detector.detectMultiScale(
                image,
                scaleFactor=1.1 if not scaleFactor else scaleFactor,  
                minNeighbors=2 if not minNeighbors else minNeighbors, 
                minSize=(128, 128) if not minSize else minSize,
            )