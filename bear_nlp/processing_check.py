# -*- encoding=utf-8 -*-
u"""纠错"""

import re

from .utility import _get_module_path
from .utility import load_syn_dict
from .utility import clean_text


dict_path = _get_module_path("dict")
check_raw_file = "{}/check_raw.txt".format(dict_path)
check_raw_dict = load_syn_dict(check_raw_file)

pattern = {
    "stock_check": re.compile("[\do]{6}")
}


def check_cleaning(text, extra_dict=[]):
    u"""纠错"""
    return clean_text(text, check_raw_dict + extra_dict)


def check_stock_cleaning(word):
    u"""股票代码纠错"""
    if pattern["stock_check"].match(word):
        word = word.replace("o", "0")

    return word
