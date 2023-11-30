# -*- coding = utf-8 -*-
# @File : main.py
# @Software : PyCharm

import os
from PySide6.QtCore import QThread, Signal
from matplotlib import pyplot as plt

from .bad_seg_clean import bad_seg_clean
from .clean_EEG import clean_EEG
from .load_data import load_data
from .make_epochs import make_epochs
from .save_as_numpy import save_as_numpy
from .show_img import show_img
from ..settings import settings
from ..share import ObjectManager

# if __name__ == '__main__':
#     # BL 静息状态 RM 轻松的音乐 PM 喜欢的音乐
#     # 一般BL数据neutral较多 PM数据positive较多
#     data_path = "珠江医院_音乐治疗数据/HC/20220118_dxmei/20220118_zjyy_dxmei_01_musicRspSeg1_BL.mat"
#     save_path = "cleaned_raw/20220118_zjyy_dxmei_01_musicRspSeg1_BL.cleaned_raw"
#     raw = load_data(data_path)
#     cleaned_raw = clean_EEG(raw)
#
#     show_img(raw, 100, "orign")
#     show_img(cleaned_raw, 100, "cleaned")
#
#     save_as_numpy(raw, save_path)


class AnalyseThread(QThread):
    matPath = ""
    sendLog = Signal(str)

    def __int__(self):
        super(AnalyseThread, self).__init__()

    def setMatPath(self, matPath:str):
        self.matPath = matPath

    def run(self):
        data_path = self.matPath
        save_path = os.path.join(settings.get("eeg_folder"),
                                 f"output/cleaned_raw/{os.path.basename(self.matPath)}.npy")
        self.analyse(data_path, save_path)

    def analyse(self, data_path, save_path):
        self.sendLog.emit(f"Loading...")
        raw = load_data(data_path)

        self.sendLog.emit(f"Begin EEG cleaning...")
        cleaned_raw = clean_EEG(raw)
        self.sendLog.emit(f"Finish EEG cleaning...")

        show_img(raw, 100, "orign")
        show_img(cleaned_raw, 100, "cleaned")

        save_path = save_path.replace("\\", "/")
        save_as_numpy(raw, save_path)


        # PSD
        orign_raw = load_data(data_path)
        raw = orign_raw.copy()

        self.sendLog.emit(f"Making epochs...")
        epochs = make_epochs(raw)

        # raw = bad_seg_clean(raw, thresh=70)
        orign_raw.compute_psd(fmin=0, fmax=130).plot()
        save_path = os.path.join(settings.get("eeg_folder"), "output/PSD/psd.png").replace("\\", "/")
        plt.savefig(save_path,
                    facecolor=(242 / 255, 242 / 255, 242 / 255))
        self.sendLog.emit(f"Output {save_path}")

        epochs.compute_psd().plot_topomap(normalize=True)
        save_path = os.path.join(settings.get("eeg_folder"), "output/PSD/psd_topomap.png").replace("\\", "/")
        plt.savefig(save_path,
                    facecolor=(242 / 255, 242 / 255, 242 / 255))
        self.sendLog.emit(f"Output {save_path}")
        self.sendLog.emit(f"Done.")


def eegAnalyse(matPath:str, logFunc=None):
    analyseThread = AnalyseThread()
    analyseThread.setMatPath(matPath)
    analyseThread.sendLog.connect(logFunc)
    analyseThread.start()
    ObjectManager.set("analyseThread", analyseThread)

