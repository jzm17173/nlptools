# -*- coding:utf-8 -*-
u"""文件、目录操作"""

import os
import math
import json
import shutil
from pathlib import Path


def read_file(file, encoding="utf-8"):
    u"""读文本文件

    Parameters
    ----------
    file : str
        文件路径
    encoding : {"utf-8", ...}, optional, default="utf-8"
        文件编码

    Returns
    -------
    {str, None}

    """
    if Path(file).is_file():
        with open(file, mode="r", encoding=encoding) as f:
            return f.read()
    else:
        return None


def write_file(file, text, encoding="utf-8"):
    u"""写文本文件

    Parameters
    ----------
    file : str
        文件路径
    text : {str, list}
        写入文本
    encoding : {"utf-8", ...}, optional, default="utf-8"
        文件编码

    Notes
    -----
    utf-8 写 csv 文件，excel 打开中文乱码，encoding 改用 utf_8_sig

    """
    if isinstance(text, list):
        text = "\n".join(text)

    with open(file, mode="w", encoding=encoding) as f:
        f.write(text)


def read_json(file, encoding="utf-8"):
    u"""读 json 文件

    Parameters
    ----------
    file : str
        文件路径
    encoding : {"utf-8", ...}, optional, default="utf-8"
        文件编码

    Returns
    -------
    {str, None}

    """
    if Path(file).is_file():
        with open(file, mode="r", encoding=encoding) as f:
            return json.load(f)
    else:
        return None


def write_json(file, obj, encoding="utf-8"):
    u"""写 json 文件

    Parameters
    ----------
    file : str
        文件路径
    obj : json
        json数据
    encoding : {"utf-8", ...}, optional, default="utf-8"
        文件编码

    """
    with open(file, mode="w", encoding=encoding) as f:
        json.dump(obj, f)


def mkdir(path):
    u"""创建目录

    Parameters
    ----------
    path : str
        目录路径

    """
    if not Path(path).is_dir():
        os.mkdir(path)


def rmdir(path):
    u"""删除目录

    Parameters
    ----------
    path : str
        目录路径

    Notes
    -----
    os.rmdir 删除空目录

    """
    if Path(path).is_dir():
        shutil.rmtree(path)


def rmfile(file):
    u"""删除文件

    Parameters
    ----------
    file : str
        文件路径

    """
    if Path(file).is_file():
        os.remove(file)


def file_tail(file, tail="_"):
    u"""文件名的末尾添加字符

    Parameters
    ----------
    file : str
        文件路径
    tail : str, optional, default="_"
        文件名末尾要添加的字符

    Returns
    -------
        str

    """
    index = file.rfind(".")
    return "{}{}{}".format(file[:index], tail, file[index:])


def file_uniq(file, tail="_uniq"):
    u"""去重

    Parameters
    ----------
    file : str
        文件路径
    tail : str, optional, default="_uniq"
        文件名末尾要添加的字符

    Returns
    -------
        list
        重复的数据

    Notes
    -----
    set 会改变排序

    """
    data = read_file(file).split("\n")

    unique_data = []
    added_data = set()
    repeated_data = set()

    for item in data:
        if item not in added_data:
            unique_data.append(item)
            added_data.add(item)
        else:
            repeated_data.add(item)

    write_file(file_tail(file, tail), "\n".join(unique_data))
    return repeated_data


def scan(root):
    u"""找到目录下所有文件

    Parameters
    ----------
    root : str
        目录

    Returns
    -------
    list

    """
    files = []
    names = os.listdir(root)
    for name in names:
        sub_path = "{}/{}".format(root, name)
        if os.path.isdir(sub_path):
            files.extend(scan(sub_path))
        elif os.path.isfile(sub_path):
            files.append(sub_path)
    return files


def concat_file(dest, src):
    u"""合并文件

    Parameters
    ----------
    dest : str
        生成文件的路径
    src : {str, list}
        需要合并的文件列表或者父目录

    """
    if isinstance(src, str) and Path(src).is_dir():
        src = ["{}/{}".format(src, item) for item in os.listdir(src)]

    texts = []
    for file in src:
        text = read_file(file)
        if text is not None:
            texts.append(text)

    write_file(dest, "\n".join(texts))


def split_file(dest, src, num):
    u"""拆分文件

    Parameters
    ----------
    dest : str
        存放拆分后文件的目录
    src : str
        待拆分的文件
    num : int
        个数

    """
    text = read_file(src)
    lines = text.split("\n")
    l = math.ceil(len(lines) / num)
    mkdir(dest)
    for i in range(num):
        write_file(
            "{}/{}_{}.txt".format(dest, num, i+1),
            "\n".join(lines[i*l:i*l+l]))
