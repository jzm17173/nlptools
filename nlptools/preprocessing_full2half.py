# -*- encoding=utf-8 -*-
u"""全角转半角

全角 full-width
半角 half-width
"""

from .utility import _get_module_path
from .utility import load_syn_dict
from .utility import clean_text


def load_fullwidth_dict(file):
    u"""全角词典"""
    fullwidth_dict = load_syn_dict(file)
    fullwidth_dict.append([" ", "　"])  # 全角空格
    return fullwidth_dict


dict_path = _get_module_path("dict")
fullwidth_file = '%s/fullwidth.txt' % dict_path
fullwidth_dict = load_fullwidth_dict(fullwidth_file)


def full2half(text):
    return clean_text(text, fullwidth_dict)


def _full2half(text):
    text_ = ""
    for char in text:
        code = ord(char)
        if code == 12288:  # 全角空格
            code = 32
        elif code >= 65281 and code <= 65374:
            code -= 65248
        text_ += chr(code)
    return text_
