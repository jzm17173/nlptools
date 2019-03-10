# -*- coding:utf-8 -*-
u"""文件、目录操作"""

import os
import json
import shutil
from pathlib import Path


def read_file(file, encoding="utf-8"):
    u"""读文本文件"""
    if Path(file).is_file():
        with open(file, mode="r", encoding=encoding) as f:
            return f.read()
    else:
        return None


def write_file(file, text, encoding="utf-8"):
    u"""写文本文件

    utf-8 写 csv 文件，excel 打开中文乱码，encoding 改用 utf_8_sig
    """
    with open(file, mode="w", encoding=encoding) as f:
        f.write(text)


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


def file_tail(file, tail="_"):
    u"""文件名的末尾添加字符"""
    index = file.rfind(".")
    return "{}{}{}".format(file[:index], tail, file[index:])


def file_uniq(file, tail="_uniq"):
    u"""去重

    set 会改变排序
    """
    data = read_file(file).split("\n")

    unique_data = []
    repeated_data = []

    for item in data:
        if item not in unique_data:
            unique_data.append(item)
        else:
            repeated_data.append(item)

    write_file(file_tail(file, tail), "\n".join(unique_data))
    return repeated_data


def concat_file(dest, src):
    u"""合并文件"""
    if isinstance(src, str) and Path(src).is_dir():
        src = ["{}/{}".format(src, item) for item in os.listdir(src)]

    texts = []
    for file in src:
        text = read_file(file)
        if text is not None:
            texts.append(text)

    write_file(dest, "\n".join(texts))
