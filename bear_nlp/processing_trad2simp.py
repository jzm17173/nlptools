# -*- encoding=utf-8 -*-
u"""繁体字转简体字"""

from zhtools.langconv import Converter


def trad2simp(text):
    return Converter("zh-hans").convert(text)
