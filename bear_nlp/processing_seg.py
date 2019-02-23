# -*- coding:utf-8 -*-
u"""分词"""

import configparser

import jieba
import jieba.posseg as pseg

from .utility import _get_module_path
from .utility_fetch import fetch
from .utility_file import read_file
from .utility_file import write_file
from .utility_file import file_tail


root_path = _get_module_path("")
dict_path = _get_module_path("dict")
config_file = "{}/conf/config.cfg".format(root_path)
custom_file = "{}/custom.txt".format(dict_path)

cfg = configparser.ConfigParser()
cfg.read(config_file)
mode = cfg["seg"]["mode"]
url = cfg["seg"]["url"]


def load_userdict(file):
    u"""加载自定义词典"""
    if not isinstance(file, list):
        file = [file]

    if mode == "jieba":
        for item in file:
            jieba.load_userdict(item)


load_userdict(custom_file)


def jieba_seg(text):
    u"""jieba 分词

    什么是销户
    ["什么", "是", "销户"]
    """
    return list(jieba.cut(text, cut_all=False))


def jieba_posseg(text):
    u"""jieba 词性标注

    什么是销户
    [("什么", "r"), ("是", "v"), ("销户", "n")]
    """
    words = pseg.cut(text)
    return [(word, flag) for word, flag in words]


def hanlp_service(text):
    u"""hanlp 分词服务

    Returns:
        word: 词
        pos_tag: 词性code
        pos_tag_value: 词性value
        entity_type: 实体类型code，不一定返回
        entity_type_value: 实体类型value，不一定返回
    """
    data = {
        "text": text
    }

    result = fetch(
        url,
        data=data,
        method="POST",
        res_type="json")

    if result is not None:
        if result["code"] == "00":
            return result["rows"]

    return None


def hanlp_seg(text):
    u"""hanlp 分词"""
    result = hanlp_service(text)

    if result is not None:
        return [item["word"] for item in result]
    else:
        return jieba_seg(text)


def hanlp_posseg(text):
    u"""hanlp 词性标注

    jieba 词性

    hanlp 词性
    """
    result = hanlp_service(text)

    if result is not None:
        return [(item["word"], item["pos_tag"]) for item in result]
    else:
        return jieba_posseg(text)


def seg(text):
    u"""分词"""
    if mode == "jieba":
        return jieba_seg(text)
    else:
        return hanlp_seg(text)


def posseg(text):
    u"""词性标注"""
    if mode == "jieba":
        return jieba_posseg(text)
    else:
        return hanlp_posseg(text)


def file_seg(file):
    data = read_file(file).split("\n")
    text = ""
    for item in data:
        if item.strip() != "":
            print(item)
            text += "{}\n".format(seg(item.strip()))
    write_file(file_tail(file, "_seg"), text)
