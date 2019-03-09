# -*- coding:utf-8 -*-
u"""文件比较"""

import copy

from .utility import _get_module_path
from .utility_file import read_file
from .utility_file import write_file
from .utility_file import file_tail


dict_path = _get_module_path("dict")


def contains(dest, src, dest_in_dict=False, case_sensitive=False, result_file=None):
    u"""源文件有的并且目标文件也有的数据

    Args:
        dest: 目标文件
        src: 源文件
        dest_in_dict: 目标文件是否在 dict 目录，默认 False
        case_sensitive: 是否区分大小写，默认 False
        result_file: 结果保存文件
    """
    if not isinstance(dest, list):
        dest_ = [dest]
    else:
        dest_ = copy.deepcopy(dest)

    if dest_in_dict:
        for i in range(len(dest_)):
            dest_[i] = "{}/{}".format(dict_path, dest_[i])

    dest_data = []
    for item in dest_:
        dest_data.extend(read_file(item).split("\n"))

    src_data = read_file(src).split("\n")

    src_data = [item.strip() for item in src_data if item.strip() != ""]
    dest_data = [item.strip() for item in dest_data if item.strip() != ""]

    if not case_sensitive:
        src_data = [item.lower() for item in src_data]
        dest_data = [item.lower() for item in dest_data]

    dest_data = set(dest_data)
    result = [item for item in src_data if item in dest_data]

    if result_file is None:
        result_file = file_tail(src, tail="_contains")

    write_file(result_file, "\n".join(result))


def not_contains(dest, src, dest_in_dict=False, case_sensitive=False, result_file=None):
    u"""源文件有的并且目标文件没有的数据

    Args:
        dest: 目标文件
        src: 源文件
        dest_in_dict: 目标文件是否在 dict 目录，默认 False
        case_sensitive: 是否区分大小写，默认 False
        result_file: 结果保存文件
    """
    if not isinstance(dest, list):
        dest_ = [dest]
    else:
        dest_ = copy.deepcopy(dest)

    if dest_in_dict:
        for i in range(len(dest_)):
            dest_[i] = "{}/{}".format(dict_path, dest_[i])

    dest_data = []
    for item in dest_:
        dest_data.extend(read_file(item).split("\n"))

    src_data = read_file(src).split("\n")

    src_data = [item.strip() for item in src_data if item.strip() != ""]
    dest_data = [item.strip() for item in dest_data if item.strip() != ""]

    if not case_sensitive:
        src_data = [item.lower() for item in src_data]
        dest_data = [item.lower() for item in dest_data]

    dest_data = set(dest_data)
    result = [item for item in src_data if item not in dest_data]

    if result_file is None:
        result_file = file_tail(src, tail="_not_contains")

    write_file(result_file, "\n".join(result))
