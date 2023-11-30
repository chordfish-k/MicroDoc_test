# -*- coding = utf-8 -*-
# @File : clean_EEG.py
# @Software : PyCharm
from .bad_seg_clean import bad_seg_clean
from .ica_clean import ica_clean


def clean_EEG(raw):
    cleaned_raw = raw.copy()
    cleaned_raw = bad_seg_clean(cleaned_raw, thresh=70)
    cleaned_raw = ica_clean(cleaned_raw)
    return cleaned_raw
