# -*- coding = utf-8 -*-
# @File : make_epochs.py
# @Software : PyCharm
import mne


def make_epochs(raw):
    # 定义时间段的长度和重叠（根据需求进行调整）
    duration = 10.0  # 时间段的长度（单位：秒）
    overlap = 0.0  # 重叠部分的比例

    # 获取原始数据的采样频率
    sfreq = raw.info['sfreq']
    # 计算时间段的采样点数和重叠的采样点数
    n_samples = int(duration * sfreq)
    n_overlap = int(n_samples * overlap)

    # 创建虚拟事件，基于时间段的分割
    events = mne.make_fixed_length_events(raw, duration=duration, overlap=n_overlap)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=duration, baseline=None, preload=True)

    return epochs
