# -*- coding:utf-8 -*-

from .utility_file import read_file
from .utility_file import write_file
from .utility_file import file_tail
from .utility import load_dict
from .utility import _get_module_path
from .analysis_freq_dist import FreqDist
from .analysis_search import search
from .processing_seg import seg


dict_path = _get_module_path("dict")


def load_added_dict():
    dict1 = load_dict("{}/builtin.txt".format(dict_path))
    dict1 = [item for item in dict1 if len(item) > 1]
    dict2 = load_dict("{}/custom.txt".format(dict_path))
    dict3 = ["这句是长文本", "这句全是时间", "这句全是数字", "这句全是停用词", "这句全是股票"]
    dict4 = load_dict("{}/stopwords.txt".format(dict_path))
    added_dict = dict1 + dict2 + dict3 + dict4
    return set(added_dict)


added_dict = load_added_dict()


def extract_words(file):
    data = read_file(file).split("\n")
    data = [item.split() for item in data if item.strip() != ""]

    data_ = []
    for item in data:
        data_.extend(item)

    dist = FreqDist(data_)

    text1 = ""
    text2 = ""
    text3 = ""
    for item in dist.most_common():
        if item[0] in added_dict:  # 已存在
            text1 += "{} {}\n".format(item[0], item[1])
        else:
            if len(item[0]) != 1:  # 词长大于1
                text2 += "{} {}\n".format(item[0], item[1])
            else:  # 词长为1
                text3 += "{} {}\n".format(item[0], item[1])

    write_file(file_tail(file, "_1"), text1)
    write_file(file_tail(file, "_2"), text2)
    write_file(file_tail(file, "_3"), text3)


def discovery_new_words(file):
    data = read_file(file).split("\n")

    text = ""
    for item in data:
        if item.strip() != "":
            text += "{}\n".format(" ".join(seg(item)))

    tokens_file = file_tail(file, "_tokens")
    write_file(tokens_file, text)

    extract_words(tokens_file)

    data = read_file(file).split("\n")
    keywords = read_file(file_tail(tokens_file, "_2")).split("\n")
    keywords = [item.split()[0] for item in keywords if item.strip() != ""]
    syn_dict = {}

    search(
        data,
        keywords,
        syn_dict,
        file_tail(tokens_file, "_2_result"))
