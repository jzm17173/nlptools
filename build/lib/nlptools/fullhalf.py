# -*- encoding=utf-8 -*-

import os

from .utils import load_syn_dict
from .utils import clean_text


def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


def _load_fullhalf_dict(file):
    u"""加载全角词典"""
    fullhalf_dict = load_syn_dict(file)
    fullhalf_dict.append([" ", "　"])  # 全角空格
    return fullhalf_dict


_dict_path = _get_module_path("dict")
_fullhalf_dict = _load_fullhalf_dict("%s/fullhalf.txt" % _dict_path)


def full2half(text):
    u"""全角(full-width)转半角(half-width)"""
    return clean_text(text, _fullhalf_dict)


u"""
def full2half(text):
    new_text = []

    for char in text:
        code = ord(char)
        if code == 12288:  # 全角空格
            code = 32
        elif code >= 65281 and code <= 65374:
            code -= 65248
        new_text.append(chr(code))

    return "".join(new_text)
"""
