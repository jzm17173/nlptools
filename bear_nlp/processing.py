# -*- encoding=utf-8 -*-
u"""数据预处理"""

import re

# from flashtext import KeywordProcessor

from .utility_file import read_file
from .utility import _get_module_path
from .utility import clean_text
from .utility import load_dict
from .processing_seg import seg
from .processing_trad2simp import trad2simp
from .processing_full2half import full2half
from .processing_check import check_cleaning
from .processing_check import check_stock_cleaning
from .processing_syn import syn_cleaning
from .processing_class import class_cleaning
from .processing_rule import rule_some_cleaning
from .processing_rule import rule_every_cleaning
from .processing_rule import rule_pick_cleaning
from .processing_rule import rule_extend_cleaning


def load_stopwords_raw(file):
    u"""加载停用词词典，分词前"""
    stopwords = read_file(file).split("\n")

    stopwords = [
        ["#", word.strip()]  # 不能为 ""
        for word in stopwords
        if word.strip() != ""]

    return stopwords


dict_path = _get_module_path("dict")

stopwords_file = "{}/stopwords.txt".format(dict_path)
stopwords_raw_file = "{}/stopwords_raw.txt".format(dict_path)
stopwords_time_file = "{}/stopwords_time.txt".format(dict_path)

stopwords = load_dict(stopwords_file, mode="set")  # 停用词词典
stopwords_time = load_dict(stopwords_time_file, mode="set")  # 时间停用词词典，用在分词后
stopwords_raw = load_stopwords_raw(stopwords_raw_file)  # 停用词词典，分词前


pattern = {
    "number": re.compile('^[好哪那第]?[0-9\.%一二三四五六七八九几两十百千万亿w]+[多]?[个张支]?$'),
    "time": re.compile('^[好]?[一二三四五六七八九十百几两]+[天号月年点]?$')
}


"""
核对代码和聚类的比较
"""


def text_cleaning(text):
    u"""数据处理"""
    text_joined = "\n".join(text)

    # 大写转小写
    text_joined = text_joined.lower()

    # 全角转半角
    text_joined = full2half(text_joined)

    # 繁体字转简体字
    text_joined = trad2simp(text_joined)

    # 纠错
    text_joined = check_cleaning(text_joined)

    # 同义词
    text_joined = syn_cleaning(text_joined)

    # 去停用词
    u"""
    &nbsp;      &nbsp ;
    /:share     / : share
    加了分词词典，还是拆开了
    """
    text_joined = clean_text(text_joined, stopwords_raw)

    # 分词
    text_splited = text_joined.split("\n")
    text_cutted = []
    for line in text_splited:
        # 排除一行上只有 # 符号的情况
        if len(line) > line.count("#"):
            line = line.replace("#", "")

        words = seg(line)

        # 分词会分出 " "
        words = [word for word in words if word.strip() != ""]

        text_cutted.append(words)

    new_text = []
    for i in range(len(text_cutted)):
        line = text_cutted[i]
        for j in range(len(line)):
            # 股票代码纠错
            line[j] = check_stock_cleaning(line[j])

            # 同义词
            line[j] = syn_cleaning(line[j], clean_type="word")

            # 类别
            line[j] = class_cleaning(line[j])

        # 移除停用词
        line_stopwords_removed = [
            word
            for word in line
            if word not in stopwords]
        # 全是停用词的情况
        if len(line_stopwords_removed) > 0:
            line = line_stopwords_removed
        else:
            line = ["这句全是停用词"]

        # 股票
        line_stock_tail_removed = [
            word
            for word in line
            if word not in ["股票", "股份", "股"]]
        if len(line_stock_tail_removed) == 0:
            line = ["股票"]
        elif len(set(line_stock_tail_removed)) == 1 and line_stock_tail_removed[0] in ["美股", "港股", "新三板"]:
            line = line_stock_tail_removed

        # 移除数字
        line_number_removed = [
            word
            for word in line
            if pattern["number"].match(word) is None]
        # 全是数字的情况
        if len(line_number_removed) > 0:
            line = line_number_removed
        else:
            line = ['这句全是数字']

        # 移除时间
        line_time_removed = [
            word
            for word in line
            if pattern["time"].match(word) is None and
            word not in stopwords_time]
        # 全是时间的情况
        if len(line_time_removed) > 0:
            line = line_time_removed
        else:
            line = ['这句全是时间']

        # 长文本
        # 计算词个数而不是文本长度，英文一个词很长
        if len(line) > 50:
            line = ['这句是长文本']

        # 多词匹配
        line = rule_some_cleaning(line)

        # 所有词匹配
        line = rule_every_cleaning(line)

        # 选取词
        line = rule_pick_cleaning(line)

        # 扩展词
        line = rule_extend_cleaning(line)

        new_text.append(line)

    return new_text
