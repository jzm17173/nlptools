# -*- coding:utf-8 -*-
u"""文件、目录操作

[Python 判断文件/目录是否存在](http://www.runoob.com/w3cnote/python-check-whether-a-file-exists.html)
"""

import os
import json
import shutil
from pathlib import Path


def read_file(file, encoding="utf-8"):
    u"""读 txt 文件"""
    if Path(file).is_file():
        with open(file, mode="r", encoding=encoding) as f:
            return f.read()
    else:
        return None


def write_file(file, text, encoding="utf-8"):
    u"""写 txt 文件

    utf-8 写 csv 文件，excel 打开中文乱码，encoding 改用 utf_8_sig
    """
    with open(file, mode="w", encoding=encoding) as f:
        f.write(text)


def file_tail(file, tail="_"):
    u"""给定文件的末尾添加字符"""
    file_splited = file.split("/")
    name = file_splited[-1]
    name_splited = name.split(".")

    if len(name_splited) == 1:
        name += tail
    else:
        name_splited[-2] += tail
        name = '.'.join(name_splited)

    file_splited[-1] = name
    return "/".join(file_splited)


def read_json(file, encoding="utf-8"):
    u"""读 json 文件"""
    if Path(file).is_file():
        with open(file, mode="r", encoding=encoding) as f:
            return json.load(f)
    else:
        return None


def write_json(file, obj, encoding="utf-8"):
    u"""写 json 文件"""
    with open(file, mode="w", encoding=encoding) as f:
        json.dump(obj, f)


def concat_file(dest, src):
    u"""合并文件"""
    if isinstance(src, str) and Path(src).is_dir():
        src = ["{}/{}".format(src, item) for item in os.listdir(src)]

    text = ""
    for file in src:
        result = read_file(file)
        if result is not None:
            text += "{}\n".format(result)

    write_file(dest, text)


def mkdir(path):
    u"""创建目录"""
    if not Path(path).is_dir():
        os.mkdir(path)


def rmdir(path):
    u"""删除目录

    os.rmdir 删除空目录
    """
    if Path(path).is_dir():
        shutil.rmtree(path)


def rmfile(file):
    u"""删除文件"""
    if Path(file).is_file():
        os.remove(file)


def file_uniq(file, tail="_uniq"):
    u"""去重

    set 会改变排序
    """
    data = read_file(file).split("\n")

    uniq_data = []
    repeated_data = []
    for item in data:
        if item not in uniq_data:
            uniq_data.append(item)
        else:
            repeated_data.append(item)

    write_file(file_tail(file, tail), "\n".join(uniq_data))
    return repeated_data
