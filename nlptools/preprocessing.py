# -*- encoding=utf-8 -*-
u"""不采用基础词典+用户扩展词典的方式，完全用户传入，调用包的时候不用总是等待"""

import re

from .utils import load_data
from .utils import clean_text
from .utils import clean_word
from .analyzer import FreqDist
from .lang import zh2hans
from .lang import half2width
from .validator import only_letters_and_numbers


_MAPS = {
    "zh-hans": zh2hans
}

_PARENTHESES_RS = "\([\w\W]+?\)"

"""
import os

def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))
"""


def full2half(text):
    u"""全角(full-width)转半角(half-width)

    Parameters
    ----------
    text : str
        待转换的文本

    Returns
    -------
    str

    """
    return clean_text(text, half2width)


def zhconvert(string, to_encoding="zh-hans"):
    u"""繁简转换

    Parameters
    ----------
    string : str
        待转换的文本

    to_encoding : {"zh-hans"}, optional, default="zh-hans"
        转换类型

    Returns
    -------
    str

    """
    final = []

    for char in string:
        final.append(_MAPS[to_encoding].get(char, char))

    return "".join(final)


def syn_cleaning(text, syn_dict, mode="text"):
    u"""同义词统一

    Parameters
    ----------
    text : str
        待转换的文本

    syn_dict : [[str]]
        同义词词典

    mode : {"text", "word"}, optional, default="text"
        转换类型

    Returns
    -------
    str

    """
    if mode == "text":
        return clean_text(text, syn_dict)
    else:
        return clean_word(text, syn_dict)


def class_cleaning(word, class_dict):
    u"""类别统一

    比如：“600570”、“600571”替换为“股票”；“感冒”、“咳嗽”替换为“疾病”

    Parameters
    ----------
    word : str
        待转换的词

    class_dict : {str: set}
        类的词典

    Returns
    -------
    str

    """
    return clean_word(word, class_dict, mode="set")


def load_rule_pick_dict(file):
    u"""加载pick词典

    Parameters
    ----------
    file : str
        配置文件路径

    Returns
    -------
    dict

        {
            'index': {
                '卖出': [0],
                '到账': [0],
                '签约': [1],
                '否定': [1],
                '成功': [1],
                '银行卡': [2],
                '解绑': [2]
            },
            'data': [
                [
                    ['卖出', '到账'],
                    ['弘钱包', '弘运宝', '金额', '时间', '份额', '确认', '否定']
                ],
                [
                    ['签约', '否定', '成功'],
                    []
                ],
                [
                    ['银行卡', '解绑'],
                    ['否定']
                ]
            ]
        }

    """
    lines = load_data(file)

    if not lines:
        return None

    rule_dict = {
        "index": {},
        "data": []
    }

    for i in range(len(lines)):
        line = lines[i]

        if line.find("|") == -1:
            words = line.split()
            words_ = []
        else:
            line_splited = line.split("|")
            words = line_splited[0].split()
            words_ = line_splited[1].split()

        for word in words:
            if word not in rule_dict["index"]:
                rule_dict["index"][word] = []
            rule_dict["index"][word].append(i)

        rule_dict["data"].append([words, words_])

    return rule_dict


def load_rule_dict(file):
    u"""加载规则词典

    Parameters
    ----------
    file : str
        配置文件路径

    Returns
    -------
    dict

        {
            'index': {
                '余额宝': [0, 1],
                '升级': [0],
                '明细': [1]
            },
            'index_notin': {},
            'data': [
                [
                    ['余额宝', '升级'],
                    ['余额宝', '升级', '余额宝', '升级', '余额宝', '升级',
                        '余额宝', '升级'],
                    []
                ],
                [
                    ['余额宝', '明细'],
                    ['余额宝', '明细', '余额宝', '明细', '余额宝', '明细',
                        '余额宝', '明细'],
                    []
                ]
            ]
        }

    """
    lines = load_data(file)

    if not lines:
        return None

    rule_dict = {
        "index": {},
        "index_notin": {},
        "data": []
    }

    for i in range(len(lines)):
        line = lines[i]

        line_splited = line.split("|")
        rule = line_splited[0].split("^")
        words_del = rule[0].split()

        if len(rule) == 1:
            words_notin = []
        else:
            words_notin = rule[1].split()

        words_add = line_splited[1].split()

        for word in words_del:
            if word not in rule_dict["index"]:
                rule_dict["index"][word] = []
            rule_dict["index"][word].append(i)

        for word in words_notin:
            if word not in rule_dict["index_notin"]:
                rule_dict["index_notin"][word] = []
            rule_dict["index_notin"][word].append(i)

        rule_dict["data"].append([words_del, words_add, words_notin])

    return rule_dict


def rule_every_cleaning(tokens, rule_dict):
    u"""every

    Parameters
    ----------
    tokens : list
        分词

    rule_dict : dict
        转换词典

    Returns
    -------
    list

    """
    if rule_dict is None:
        return tokens

    indexes = []
    tokens_unique = list(set(tokens))
    for i in range(len(tokens_unique)):
        indexes.extend(rule_dict["index"].get(tokens_unique[i], []))

    if len(indexes) > 0:
        index_matched = []
        index_dist = FreqDist(indexes)

        # 按index的个数排序
        len_sorted = index_dist.filter("equal[%d]" % len(tokens_unique))

        if len(len_sorted) > 0:
            # 按index的值排序
            index_sorted = sorted(len_sorted, key=lambda x: x[0])

            for index in index_sorted:
                words = rule_dict["data"][index[0]]
                # 排除：rule是abcd，tokens是abc
                if len(words[0]) == index[1]:
                    index_matched.append(index)

            for index in index_matched[:1]:
                words = rule_dict["data"][index[0]]
                tokens = words[1][:]  # 拷贝，引用相同，一个修改导致另一个也被修改

    return tokens


def _rule_some_cleaning(tokens, rule_dict, mode="all", count=0):
    indexes = []
    indexes_notin = []
    tokens_unique = list(set(tokens))
    for i in range(len(tokens_unique)):
        indexes.extend(
            rule_dict["index"].get(tokens_unique[i], []))
        indexes_notin.extend(
            rule_dict["index_notin"].get(tokens_unique[i], []))

    indexes = [index for index in indexes if index not in indexes_notin]

    index_matched = []
    if len(indexes) > 0:
        index_dist = FreqDist(indexes)

        len_sorted = index_dist.most_common()

        if mode == "all":
            index_sorted = sorted(len_sorted, key=lambda x: x[0])
        else:
            index_sorted = sorted(
                len_sorted,
                key=lambda x: -(x[1] - 0.001 * x[0]))

        for index in index_sorted:
            words = rule_dict["data"][index[0]]
            # 包括^的至少要有两个词
            if index[1] > 1 or (index[1] == 1 and len(words[2]) != 0):
                if len(words[0]) == index[1]:
                    index_matched.append(index)

        for index in index_matched[:1]:
            words = rule_dict["data"][index[0]]
            for word in words[0]:
                tokens.remove(word)
            tokens.extend(words[1])

    count += 1

    # 再执行一次才能知道有没有新的匹配
    # 不能加 “银行 卡 | 银行 卡 绑定” 会始终匹配
    if mode == "all" and len(index_matched) > 0 and count < 3:
        tokens = _rule_some_cleaning(
            tokens, rule_dict, mode="all", count=count)

    return tokens


def rule_pick_cleaning(tokens, rule_dict):
    u"""pick

    Parameters
    ----------
    tokens : list
        分词

    rule_dict : dict
        转换词典

    Returns
    -------
    list

    Notes
    -----
    依次处理，词典要注意顺序，需要词多优先匹配的排在前面

    """
    if rule_dict is None:
        return tokens

    indexes = []
    tokens_unique = list(set(tokens))
    for i in range(len(tokens_unique)):
        indexes.extend(rule_dict["index"].get(tokens_unique[i], []))

    index_matched = []
    if len(indexes) > 0:
        index_dist = FreqDist(indexes)

        len_sorted = index_dist.filter("greater_than[1]")

        if len(len_sorted) > 0:
            index_sorted = sorted(
                len_sorted,
                key=lambda x: x[0])

            for index in index_sorted:
                words = rule_dict["data"][index[0]]
                if len(words[0]) == index[1]:
                    index_matched.append(index)

            for index in index_matched[:1]:
                words = rule_dict["data"][index[0]]
                tokens = list(set([
                    word for word in tokens if word in words[0] + words[1]]))

    return tokens


def rule_some_cleaning(tokens, rule_dict):
    u"""some

    Parameters
    ----------
    tokens : list
        分词

    rule_dict : dict
        转换词典

    Returns
    -------
    list

    """
    if rule_dict is None:
        return tokens

    return _rule_some_cleaning(tokens, rule_dict)


def rule_extend_cleaning(tokens, rule_dict):
    u"""extend

    Parameters
    ----------
    tokens : list
        分词

    rule_dict : dict
        转换词典

    Returns
    -------
    list

    """
    if rule_dict is None:
        return tokens

    return _rule_some_cleaning(tokens, rule_dict, mode="one")


def remove_space(text):
    u"""移除空格

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    
    """
    return text.replace(" ", "")


def remove_unnecessary_space(text):
    u"""移除非必须的空格

    Parameters
    ----------
    text : str

    Returns
    -------
    str

    """
    text = text.strip()
    text = re.sub("\s{2,}", " ", text)
    splited_text = text.split(" ")
    l = len(splited_text)
    last_i = l - 1
    for i in range(l):
        current_text = splited_text[i]
        if i < last_i:
            next_text = splited_text[i+1]
            if only_letters_and_numbers("{}{}".format(current_text[-1], next_text[0])):
                splited_text[i] = "{} ".format(current_text)
    return "".join(splited_text)


def remove_parentheses(text):
    u"""移除圆括号

    Parameters
    ----------
    text : {str, list}

    Returns
    -------
    {str, list}

    """
    if isinstance(text, list):
        return [re.sub(_PARENTHESES_RS, "", item) for item in text]
    else:
        return re.sub(_PARENTHESES_RS, "", text)
