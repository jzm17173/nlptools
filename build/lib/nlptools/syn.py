# -*- encoding=utf-8 -*-
u"""同义词"""

from .utils import clean_text
from .utils import clean_word


def syn_cleaning(text, syn_dict, mode="text"):
    if mode == "text":
        return clean_text(text, syn_dict)
    else:
        return clean_word(text, syn_dict)
