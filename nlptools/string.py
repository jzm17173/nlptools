# -*- coding:utf-8 -*-

import re


def bytelen(target, fix=2):
    u"""字符串长度，其中双字节字符的长度可以指定

    Parameters
    ----------
    target : str
        字符串
    fix : int, optional, default=2
        双字节字符的长度

    Returns
    -------
    int

    Notes
    -----
    [^\x00-\xff] 双字节字符，ASCII编码不在0-255的字符

    """
    return len(re.sub("[^\x00-\xff]", "-" * fix, target))
