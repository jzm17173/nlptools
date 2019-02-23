# -*- coding:utf-8 -*-

from .utility_file import read_file
from .utility_file import write_file
from .utility_file import file_tail
from .utility_time import timestamp


def _load_syn_dict(file):
    u"""同义词

    Returns:
        {
            "开通": ["开通", "开立", "开了", "开了个", "开户", "新开户"]
        }
    """
    lines = read_file(file).split("\n")
    lines = [
        line.split()
        for line in lines
        if line.strip() != ""]

    syn_dict = {}
    for words in lines:
        syn_dict[words[0]] = words

    return syn_dict


def _load_keywords(file):
    u"""搜索条件"""
    if isinstance(file, str):
        lines = read_file(file).split("\n")
        lines = [line.strip() for line in lines if line.strip() != ""]
    else:
        lines = file

    rules = []
    for line in lines:
        rule123 = line.split("|")
        rule12 = rule123[0].split("^")
        rule = []
        rule.append(rule12[0].split())

        if len(rule12) == 1:
            rule.append([])
        else:
            rule.append(rule12[1].split())

        if len(rule123) == 1:
            rule.append([])
        else:
            rule.append(rule123[1].split())

        rule.append(line)

        rules.append(rule)

    return rules


def _load_data(file):
    u"""数据"""
    data = read_file(file).split("\n")
    data = [item.strip() for item in data if item.strip() != ""]
    return data


def has_all(question, keywords, syn_dict):
    u"""全部存在"""
    count = 0
    for item in keywords:
        if syn_dict.get(item) is None:
            if question.find(item) != -1:
                count += 1
        else:
            for sub_item in syn_dict.get(item):
                if question.find(sub_item) != -1:
                    count += 1
                    break

    if count == len(keywords):
        return True
    else:
        return False


def has_one(question, keywords, syn_dict):
    u"""只要有一个存在"""
    if len(keywords) == 0:
        return True

    for item in keywords:
        if syn_dict.get(item) is None:
            if question.find(item) != -1:
                return True
        else:
            for sub_item in syn_dict.get(item):
                if question.find(sub_item) != -1:
                    return True

    return False


def has_zero(question, keywords, syn_dict):
    u"""全部不存在"""
    for item in keywords:
        if syn_dict.get(item) is None:
            if question.find(item) != -1:
                return False
        else:
            for sub_item in syn_dict.get(item):
                if question.find(sub_item) != -1:
                    return False

    return True


def search(data, keywords, syn_dict, result_file=None, max_size=None):
    u"""搜索

    传入数据或文件
    """
    if isinstance(data, str):
        if result_file is None:
            result_file = file_tail(data, "_result")
        data = _load_data(data)

    keywords = _load_keywords(keywords)

    if isinstance(syn_dict, str):
        syn_dict = _load_syn_dict(syn_dict)

    if result_file is None:
        result_file = "{}.txt".format(timestamp())

    result = []
    for rule in keywords:
        item = {
            "keywords": rule,
            "question": []
        }

        for question in data:
            if (has_all(question, rule[0], syn_dict) and
                    has_zero(question, rule[1], syn_dict) and
                    has_one(question, rule[2], syn_dict)):
                if max_size is None:
                    item["question"].append(question)
                elif len(item["question"]) < max_size:
                    item["question"].append(question)

        result.append(item)

    text = ""
    for item in result:
        text += "\n\n------------------------------\n\n\n关键词：{}\n\n".format(
            item["keywords"][3])

        for question in item["question"]:
            text += "{}\n".format(question)

    write_file(result_file, text)
