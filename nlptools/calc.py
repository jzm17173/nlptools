# -*- coding:utf-8 -*-
u"""计算"""

from decimal import Decimal


def num_add(num1, num2):
    return str(Decimal(str(num1)) + Decimal(str(num2)))


def num_sub(num1, num2):
    return str(Decimal(str(num1)) - Decimal(str(num2)))


def num_multi(num1, num2):
    return str(Decimal(str(num1)) * Decimal(str(num2)))


def num_div(num1, num2):
    return str(Decimal(str(num1)) / Decimal(str(num2)))
