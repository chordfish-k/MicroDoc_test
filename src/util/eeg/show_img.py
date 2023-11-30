# -*- coding = utf-8 -*-
# @File : show_img.py
# @Software : PyCharm
import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ..settings import settings


def show_img(raw, scaling, name="default"):
    path = os.path.join(settings.get("eeg_folder"), f"output/EEG/{name}.jpg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw.plot(duration=50, scalings={'eeg': scaling})
    # plt.show()
    plt.savefig(path)
