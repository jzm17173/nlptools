# -*- encoding=utf-8 -*-
u"""纠错"""

import re

from .utils import clean_text


_re_wrong_stock = re.compile("^[\do]{6}$")


def typos_cleaning(text, typos_dict):
    u"""错别字修复

    Parameters
    ----------
    text : str
        文本

    typos_dict : [[str]]
        错别字字典

    Returns
    -------
    str

    """
    return clean_text(text, typos_dict)


def stock_cleaning(word):
    u"""股票代码修复

    Parameters
    ----------
    word : str
        待修复的词

    Returns
    -------
    str

    """
    if _re_wrong_stock.match(word):
        word = word.replace("o", "0")

    return word
