# -*- coding = utf-8 -*-
# @File : bad_seg_clean.py
# @Software : PyCharm
import mne
from mne.preprocessing import find_eog_events, find_ecg_events


def bad_seg_clean(raw,thresh):
    raw_copy = raw.copy()
    eog_events = find_eog_events(raw_copy, ch_name=raw.info['ch_names'][0], thresh=thresh)
    eog_onsets = eog_events[:, 0] / raw.info['sfreq'] - 0.25
    eog_durations = [0.5] * len(eog_events)
    descriptions = ['BAD_'] * len(eog_events)
    return raw
