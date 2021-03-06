# -*- coding:utf-8 -*-

import uuid

from .fs import read_file
from .date import now
from .date import timestamp


def load_data(file):
    u"""加载数据

    Parameters
    ----------
    file : str
        文件路径

    Returns
    -------
    list

    """
    text = read_file(file)

    if text is None:
        return []

    lines = text.split("\n")

    return [line.strip() for line in lines if line.strip() != ""]


def load_dict(file, mode="list"):
    u"""加载词典

    Parameters
    ----------
    file : str
        文件路径

    mode : {"list", "set"}, optional, default="list"
        类型

    Returns
    -------
    {list, set}

    """
    words = load_data(file)

    if mode == "set":
        words = set(words)

    return words


def load_syn_dict(file, mode="list"):
    u"""加载替换词典

    Parameters
    ----------
    file : str
        文件路径

    mode : {"list", "set"}, optional, default="list"
        类型

    Returns
    -------
    {[[str]], {str: set}}

    """
    lines = load_data(file)

    if mode == "set":
        syn_dict = {}

        for line in lines:
            line_splited = line.split()
            word = line_splited[0]
            if word not in syn_dict:
                syn_dict[word] = set()
            syn_dict[word] = syn_dict[word] | set(line_splited[1:])  # key重复会
    else:
        syn_dict = [
            line.split()
            for line in lines]

    return syn_dict


def clean_text(text, word_dict):
    u"""替换文档里的词

    Parameters
    ----------
    text : str
        待替换的文本

    word_dict : [[str]]
        词典

    Returns
    -------
    str

    """
    for item in word_dict:
        new = item[0]
        for old in item[1:]:
            text = text.replace(old, new)

    return text


def clean_word(word, word_dict, mode="list"):
    u"""替换词

    Parameters
    ----------
    word : str
        待替换的词

    word_dict : {[[str]], {str: set}}
        词典

    mode : {"list", "set"}, optional, default="list"
        类型

    Returns
    -------
    str

    Notes
    -----
    同一个词只会匹配一次
    """
    if mode == "set":
        for item in word_dict:
            if word in word_dict[item]:
                return item
    else:
        for item in word_dict:
            if word in item:
                return item[0]

    return word


def generate_name(mode="time"):
    u"""命名

    Parameters
    ----------
    mode : {"time", "uuid", "timestamp"}, optional, default="time"
        类型

    Returns
    -------
    str

    """
    if mode == "uuid":
        return str(uuid.uuid1())
    elif mode == "timestamp":
        return str(timestamp())
    else:
        return now("%Y%m%d%H%M%S")
