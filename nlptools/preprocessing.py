# -*- encoding=utf-8 -*-
u"""不采用基础词典+用户扩展词典的方式，完全用户传入，调用包的时候不用总是等待"""

import os

from .utils import load_data
from .utils import load_syn_dict
from .utils import clean_text
from .utils import clean_word
from .analyzer import FreqDist
from .zh import zh2hans


_MAPS = {
    "zh-hans": zh2hans
}


def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


def _load_fullhalf_dict(file):
    u"""加载全角词典"""
    fullhalf_dict = load_syn_dict(file)
    fullhalf_dict.append([" ", "　"])  # 全角空格
    return fullhalf_dict


_dict_path = _get_module_path("dict")
_fullhalf_dict = _load_fullhalf_dict("%s/fullhalf.txt" % _dict_path)


def full2half(text):
    u"""全角(full-width)转半角(half-width)"""
    return clean_text(text, _fullhalf_dict)


u"""
def full2half(text):
    new_text = []

    for char in text:
        code = ord(char)
        if code == 12288:  # 全角空格
            code = 32
        elif code >= 65281 and code <= 65374:
            code -= 65248
        new_text.append(chr(code))

    return "".join(new_text)
"""


def zhconvert(string, to_encoding="zh-hans"):
    u"""繁简转换"""
    final = []

    for char in string:
        final.append(_MAPS[to_encoding].get(char, char))

    return "".join(final)


def syn_cleaning(text, syn_dict, mode="text"):
    u"""同义词统一"""
    if mode == "text":
        return clean_text(text, syn_dict)
    else:
        return clean_word(text, syn_dict)


def class_cleaning(word, class_dict):
    u"""类别统一

    比如：“600570”、“600571”替换为“股票”；“感冒”、“咳嗽”替换为“疾病”
    """
    return clean_word(word, class_dict, mode="set")


def load_rule_pick_dict(file):
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
    u"""加载多词匹配"""
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
    u"""
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
    if rule_dict is None:
        return tokens

    return _rule_some_cleaning(tokens, rule_dict)


def rule_extend_cleaning(tokens, rule_dict):
    if rule_dict is None:
        return tokens

    return _rule_some_cleaning(tokens, rule_dict, mode="one")
