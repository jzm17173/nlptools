# -*- coding:utf-8 -*-


def pad_num(num, digits):
    u"""补0

    Parameters
    ----------
    num : str
        数值

    digits : int
        位数

    Returns
    -------
    str
        补0后的数值

    """
    neg = "-" if num[0] == "-" else ""

    if neg == "-":
        num = num[1:]

    while(len(num) < digits):
        num = "0{}".format(num)

    return "{}{}".format(neg, num)


def _remove_num_tail_zero(value):
    u"""移除小数末尾的0

    Parameters
    ----------
    value : str
        数值

    Returns
    -------
    str
        移除末尾多余0后的数值

    """
    if "." in value:
        max_i = 0
        for i in range(len(value)):
            if value[i] != "0" and i > max_i:
                max_i = i
        end = max_i + 1 if value[max_i] != "." else max_i
        return value[:end]
    else:
        return value


def _remove_num_comma(value):
    u"""移除逗号

    Parameters
    ----------
    value : str
        数值

    Returns
    -------
    str
        移除逗号后的数值

    """
    return value.replace(",", "")


def normalize_num(value):
    u"""标准化数字

    Parameters
    ----------
    value : str
        数值

    Returns
    -------
    str
        标准化后的数值

    """
    value = _remove_num_comma(value)
    value = _remove_num_tail_zero(value)
    return value
