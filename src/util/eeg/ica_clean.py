# -*- coding = utf-8 -*-
# @File : ica_clean.py
# @Software : PyCharm
import os
import matplotlib

from src.util.settings import settings

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mne.preprocessing import ICA

from ..share import ObjectManager


def ica_clean(raw):

    # ICA分析
    ica = ICA(max_iter='auto', n_components=30)
    raw_for_ica = raw.copy()
    ica.fit(raw_for_ica, reject_by_annotation=False)
    n_components = ica.n_components

    analyseThread = ObjectManager.get("analyseThread")
    analyseThread.sendLog.emit(str(raw_for_ica.info))

    ica.plot_components(nrows=6, ncols=5, show=False)
    savePath = os.path.join(settings.get("eeg_folder"), "output/ICA/plot_components1.jpg").replace("\\", "/")
    plt.savefig(savePath)
    analyseThread.sendLog.emit(f"Output : {savePath}")

    for i in range(n_components):
        ica.plot_properties(raw, picks=[i], show=False)
        savePath = os.path.join(settings.get("eeg_folder"), f"output/ICA/ICA_{i}.jpg").replace("\\", "/")
        plt.savefig(savePath)
        analyseThread.sendLog.emit(f"Output : {savePath}")


    # 自动排除伪迹成分
    ecg_indices, ecg_scores = ica.find_bads_ecg(raw_for_ica, ch_name=raw_for_ica.info['ch_names'][0]
                                                , reject_by_annotation=False)
    eog_indices, eog_scores = ica.find_bads_eog(raw_for_ica, ch_name=raw_for_ica.info['ch_names'][0]
                                                , reject_by_annotation=False)
    mus_indices, mus_scores = ica.find_bads_muscle(raw_for_ica)
    artifacts_indices = ecg_indices + eog_indices + mus_indices
    ica.exclude = artifacts_indices
    cleaned_raw = ica.apply(raw_for_ica)

    return cleaned_raw
