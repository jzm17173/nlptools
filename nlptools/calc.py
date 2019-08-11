# -*- coding:utf-8 -*-
u"""计算"""

from decimal import Decimal

from .number import normalize_num


def num_add(num1, num2):
    u"""相加

    Parameters
    ----------
    num1 : {int, float, str}
        数值1

    num2 : {int, float, str}
        数值2

    Returns
    -------
    str

    """
    return str(Decimal(str(num1)) + Decimal(str(num2)))


def num_sub(num1, num2):
    u"""相减

    Parameters
    ----------
    num1 : {int, float, str}
        数值1

    num2 : {int, float, str}
        数值2

    Returns
    -------
    str

    """
    return str(Decimal(str(num1)) - Decimal(str(num2)))


def num_multi(num1, num2):
    u"""相乘

    Parameters
    ----------
    num1 : {int, float, str}
        数值1

    num2 : {int, float, str}
        数值2

    Returns
    -------
    str

    """
    return normalize_num(str(Decimal(str(num1)) * Decimal(str(num2))))


def num_div(num1, num2):
    u"""相除

    Parameters
    ----------
    num1 : {int, float, str}
        数值1

    num2 : {int, float, str}
        数值2

    Returns
    -------
    str

    """
    return str(Decimal(str(num1)) / Decimal(str(num2)))
