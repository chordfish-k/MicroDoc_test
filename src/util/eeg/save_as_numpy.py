# -*- coding = utf-8 -*-
# @File : save_as_numpy.py
# @Software : PyCharm
import os

import numpy as np

from src.util.share import ObjectManager


def save_as_numpy(raw,path):
    raw = raw.resample(24)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = raw.get_data(reject_by_annotation='omit')
    # normalized_data = 2 * ((data - np.min(data)) / (np.max(data) - np.min(data))) - 1
    # np.save(path, normalized_data)
    np.save(path, data)
    analyseThread = ObjectManager.get("analyseThread")
    analyseThread.sendLog.emit(f"Output npy file to: {path}")

# if __name__ == "__main__":
#     path = os.path.curdir +  "/cleaned_raw/20220118_zjyy_dxmei_01_musicRspSeg1_BL.cleaned_raw"
#     data = np.load(path)
#     print(data[:3])
#     print(data.shape)
#     print(min(data[0]), max(data[0]))