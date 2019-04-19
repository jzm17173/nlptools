# -*- coding:utf-8 -*-

import math


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

    """
    value = _remove_num_comma(value)
    value = _remove_num_tail_zero(value)
    return value


def grouping(nums, min_len=3, min_num=None, max_diff=2, skip=True):
    u"""分组
    Parameters
    ----------
    nums : list
        值列表
    min_len : int, optional, default=3
        分组最小长度
    min_num : int, optional, default=None
        最小的值
    max_diff : int, optional, default=2
        最大允许的差值
    skip : bool, optional, default=True
        是否可以跳过1个差值不符合的
    Returns
    -------
    list
    """
    new_nums = []
    grouped_nums = []

    for i in range(len(nums)):
        if i not in grouped_nums:
            temp = []
            num1 = nums[i]

            right_nums = nums[i:]
            right_nums_len = len(right_nums)
            right_nums_penult_i = right_nums_len - 2

            for j in range(right_nums_len):
                num2 = right_nums[j]
                diff1 = math.fabs(num1 - num2)

                if j < right_nums_penult_i:
                    diff2 = math.fabs(num1 - right_nums[j + 1])
                else:
                    diff2 = 999

                if (min_num is None or num1 > min_num) and (diff1 <= max_diff or (skip and diff2 <= max_diff)):
                    temp.append(i + j)
                else:
                    break

            if len(temp) > min_len:
                grouped_nums.extend(temp)
                new_nums.append(temp)
            else:
                new_nums.append(i)

    return new_nums, grouped_nums
