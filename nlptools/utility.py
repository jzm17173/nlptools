# -*- coding:utf-8 -*-

import os
import time

from .utility_file import read_file


tstart = None
tend = None

def start_time():
    global tstart
    tstart = time.time()


def get_delta():
    global tend
    tend = time.time()
    return "%.2fms" % 1000 * (tstart - tend)


def _get_module_path(path):
    u""""utility.py 的路径

    代码放在当前文件才能取到当前文件的路径

    example:
        os.getcwd()                "/Users/nanakon/Github/Bear/python/test/"
        os.path.dirname(__file__)  "../hs_nlp"
        os.path.join               "/Users/nanakon/Github/Bear/python/
                                        test/../hs_nlp"
        os.path.normpath           "/Users/nanakon/Github/Bear/python/
                                        hs_nlp"
    """
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


def load_dict(file, mode="list"):
    u"""加载词典

    Args:
        file: 文件
        mode: 类型

    Returns:
        mode为list
        ["啊", "呀"]

        mode为set
        {"啊", "呀"}
    """
    text = read_file(file)
    if text is None:
        if mode == "set":
            return set()
        else:
            return []

    words = text.split("\n")

    words = [
        word.strip()
        for word in words
        if word.strip() != ""]

    if mode == "set":
        words = set(words)

    return words


def load_syn_dict(file, mode="list"):
    u"""加载替换词典


    Args:
        file: 文件
        list: 类型

    Returns:
        mode为list
        [["登录", "登陆", "登入"]]

        mode为set
        {"登录": {"登陆", "登入"}}
    """
    text = read_file(file)
    if text is None:
        if mode == "set":
            return {}
        else:
            return []

    lines = text.split("\n")
    if mode == "set":
        syn_dict = {}
        for line in lines:
            if line.strip() != "":
                line_splited = line.split()
                word = line_splited[0]
                if word not in syn_dict:
                    syn_dict[word] = set()
                syn_dict[word] = syn_dict[word] | set(line_splited[1:])  # 有key重复的情况
    else:
        syn_dict = [
            line.split()
            for line in lines
            if line.strip() != ""]

    return syn_dict


def clean_text(text, word_dict):
    u"""替换文档里的词"""
    for item in word_dict:
        new = item[0]
        for old in item[1:]:
            text = text.replace(old, new)

    return text


def clean_word(word, word_dict, mode="list"):
    u"""替换词

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
