# -*- coding:utf-8 -*-

import os
from pathlib import Path


def read_file(file, encoding="utf-8"):
    if os.path.exists(file):
        with open(file, mode="r", encoding=encoding) as f:
            return f.read()
    else:
        return None


def write_file(file, text, encoding="utf-8"):
    with open(file, mode="w", encoding=encoding) as f:
        f.write(text)


def mkdir(path):
    if not Path(path).is_dir():
        os.mkdir(path)


def load_syn_dict(file):
    lines = read_file(file).split('\n')
    syn_dict = [line.split() for line in lines if line.strip() != ""]

    return syn_dict


def load_fullwidth_dict(file):
    fullwidth_dict = load_syn_dict(file)
    fullwidth_dict.append([" ", "　"])  # 全角空格
    return fullwidth_dict


fullwidth_dict = load_fullwidth_dict("fullwidth/fullwidth.txt")


def clean_text(text, word_dict):
    for item in word_dict:
        new = item[0]
        for old in item[1:]:
            text = text.replace(old, new)

    return text


def concat_file(dest, src, lower=False, halfwidth=False):
    if isinstance(src, str):
        src = ["{}/{}".format(src, item) for item in os.listdir(src)]

    text = ""
    for file in src:
        text += read_file(file) + "\n"

    if lower:
        text = text.lower()

    if halfwidth:
        text = clean_text(text, fullwidth_dict)

    write_file(dest, text)


def make_class(file):
    data = read_file(file).split("\n")
    data = [item.split() for item in data if item.strip() != ""]
    words = []
    for item in data:
        words.extend(item)

    if len(data) != len(words):
        write_file("{}_.txt".format(file.split(".")[0]), "\n".join(words))
    write_file("{}_class.txt".format(file.split(".")[0]), " ".join(words))


def clean_empty(file):
    data = read_file(file).split("\n")
    data = [item.strip() for item in data if item.strip() != ""]
    write_file(file, "\n".join(data))


config = {
    # 类别
    "class": {
        "base": [
            "class/time.txt",
            "class/finance/bank.txt"
        ],
        # 天弘基金
        "thfund": [
            "class/thfund/fund1.txt",
            "class/thfund/fund2.txt",
            "class/thfund/fund3.txt",
            "class/thfund/fund4.txt",
            "class/thfund/fund5.txt",
            "class/thfund/fund6.txt"
        ],
        # 晓鲸
        "smartwhale": [
            "class/ent/music.txt",
            "class/ent/poetry.txt",
            "class/ent/book.txt",
            "class/ent/film.txt",
            "class/ent/game.txt"
        ]
    },
    # 合并
    "concat": {
        # 类别
        "class.txt": {
            "base": [
                "class/time_class.txt",
                "class/finance/bank_class.txt"
            ],
            "thfund": [
                "class/thfund/fund1_class.txt",
                "class/thfund/fund2_class.txt",
                "class/thfund/fund3_class.txt",
                "class/thfund/fund4_class.txt",
                "class/thfund/fund5_class.txt",
                "class/thfund/fund6_class.txt"
            ],
            "smartwhale": [
                "class/ent/music_class.txt",
                "class/ent/poetry_class.txt",
                "class/ent/book_class.txt",
                "class/ent/film_class.txt",
                "class/ent/game_class.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 停用词(分词前)
        "stopwords_raw.txt": {
            "base": [
                "stopwords/stopwords_raw.txt"
            ],
            "thfund": [
                "stopwords/stopwords_raw.txt"
            ],
            "smartwhale": [
                "stopwords/stopwords_raw.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 停用词
        "stopwords.txt": {
            "base": [
                "stopwords/chinese.txt",
                "stopwords/english.txt",
                "stopwords/letter.txt",
                "stopwords/number.txt",
                "stopwords/punctuation.txt",
                "stopwords/special_character.txt",
                "stopwords/good.txt",
                "stopwords/bad.txt",
                "stopwords/other.txt",
                "custom/custom2stopwords.txt"
            ],
            "thfund": [
                "stopwords/chinese.txt",
                "stopwords/english.txt",
                "stopwords/letter.txt",
                "stopwords/number.txt",
                "stopwords/punctuation.txt",
                "stopwords/special_character.txt",
                "stopwords/good.txt",
                "stopwords/bad.txt",
                "stopwords/other.txt",
                "custom/custom2stopwords.txt"
            ],
            "smartwhale": [
                "stopwords/chinese.txt",
                "stopwords/english.txt",
                "stopwords/letter.txt",
                "stopwords/number.txt",
                "stopwords/punctuation.txt",
                "stopwords/special_character.txt",
                "stopwords/good.txt",
                "stopwords/bad.txt",
                "stopwords/other.txt",
                "custom/custom2stopwords.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 停用词-时间
        "stopwords_time.txt": {
            "base": [
                "stopwords/time.txt"
            ],
            "thfund": [
                "stopwords/time.txt"
            ],
            "smartwhale": [
                "stopwords/time.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 规则-全部匹配
        "rule_every.txt": {
            "base": [
            ],
            "thfund": [
                "rule/thfund/every.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 规则-部分匹配
        "rule_some.txt": {
            "base": [
            ],
            "thfund": [
                "rule/thfund/some.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 规则-挑选
        "rule_pick.txt": {
            "base": [
            ],
            "thfund": [
                "rule/thfund/pick.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 规则—扩展
        "rule_extend.txt": {
            "base": [
            ],
            "thfund": [
                "rule/thfund/extend.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 纠错
        "check_raw.txt": {
            "base": [
                "check/raw_common.txt",
                "check/raw_finance.txt"
            ],
            "thfund": [
                "check/thfund/raw.txt"
            ],
            "smartwhale": [
                "check/smartwhale/raw.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 全角
        "fullwidth.txt": {
            "base": [
                "fullwidth/fullwidth.txt"
            ],
            "lower": True,
            "halfwidth": False
        },
        # 同义词-分词前
        "syn_raw.txt": {
            "base": [
                "syn/raw.txt",
                "syn/raw_tail.txt",
                "syn/raw_split.txt"
            ],
            "thfund": [
                "syn/thfund/raw.txt",
                "syn/thfund/syn2custom_primary.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 同义词-分词后
        "syn_tokens.txt": {
            "base": [
                "syn/tokens.txt",
                "syn/tokens_custom2syn.txt"
            ],
            "thfund": [
                "syn/thfund/tokens.txt",
                "syn/thfund/tokens_custom2syn.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 自定义词典
        "custom.txt": {
            "base": [
                "class/finance/fund_code.txt",
                "class/finance/fund_name.txt",
                "class/finance/us_stock_name.txt",
                "class/finance/hk_stock_name.txt",
                "class/finance/new_three_board_name.txt",
                "class/finance/stock_code.txt",
                "class/finance/stock_name.txt",
                "class/finance/stock_short_name.txt",
                "class/finance/stock_code_other.txt",
                "class/finance/stock_name_other.txt",

                "custom/finance/block_area.txt",
                "custom/finance/block_concept.txt",
                "custom/finance/block_index.txt",
                "custom/finance/product.txt",
                "custom/finance/other.txt",

                "custom/common.txt",

                "custom/custom2stopwords.txt",
                "custom/custom2syn.txt",

                "class/time.txt",
                "class/finance/bank.txt"
            ],
            "smartwhale": [
                "custom/smartwhale/smartwhale.txt",
                "class/ent/music.txt",
                "class/ent/poetry.txt",
                "class/ent/book.txt",
                "class/ent/film.txt",
                "class/ent/game.txt"
            ],
            "thfund": [
                "custom/thfund/syn2custom_primary.txt",
                "custom/thfund/custom2syn.txt",
                "custom/thfund/thfund.txt",
                "class/thfund/fund1_.txt",
                "class/thfund/fund2_.txt",
                "class/thfund/fund3_.txt",
                "class/thfund/fund4_.txt",
                "class/thfund/fund5_.txt",
                "class/thfund/fund6_.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 股票
        "stock.txt": {
            "base": [
                "class/finance/us_stock_name.txt",
                "class/finance/hk_stock_name.txt",
                "class/finance/new_three_board_name.txt",
                "class/finance/stock_code.txt",
                "class/finance/stock_name.txt",
                "class/finance/stock_short_name.txt",
                "class/finance/stock_code_other.txt",
                "class/finance/stock_name_other.txt"
            ],
            "thfund": [
                "class/finance/us_stock_name.txt",
                "class/finance/hk_stock_name.txt",
                "class/finance/new_three_board_name.txt",
                "class/finance/stock_code.txt",
                "class/finance/stock_name.txt",
                "class/finance/stock_short_name.txt",
                "class/finance/stock_code_other.txt",
                "class/finance/stock_name_other.txt"
            ],
            "smartwhale": [
                "class/finance/us_stock_name.txt",
                "class/finance/hk_stock_name.txt",
                "class/finance/new_three_board_name.txt",
                "class/finance/stock_code.txt",
                "class/finance/stock_name.txt",
                "class/finance/stock_short_name.txt",
                "class/finance/stock_code_other.txt",
                "class/finance/stock_name_other.txt"
            ],
            "lower": True,
            "halfwidth": True
        },
        # 内置词典
        "builtin.txt": {
            "base": [
                "builtin/jieba.txt"
            ],
            "lower": False,
            "halfwidth": False
        },
    }
}


def _build(root_dir="../nlptools/dict", product=None):
    class_files = []
    if product is None:
        class_files.extend(config["class"]["base"])
    elif product in config["class"]:
        class_files.extend(config["class"][product])

    for file in class_files:
        make_class(file)

    for key in config["concat"]:
        dest = "{}/{}".format(root_dir, key)
        item = config["concat"][key]

        src = []
        if product is None and "base" in item:
            src.extend(item["base"])
        elif product in item:
            src.extend(item[product])

        lower = item["lower"]
        halfwidth = item["halfwidth"]

        if len(src) != 0:
            concat_file(dest, src, lower=lower, halfwidth=halfwidth)

    names = os.listdir("{}/".format(root_dir))
    for name in names:
        if name not in ["src", ".DS_Store"]:
            clean_empty("{}/{}".format(root_dir, name))


dirs = [
    "../base",
    "../base/dict",
    "../thfund",
    "../thfund/dict",
    "../smartwhale",
    "../smartwhale/dict"
]

for item in dirs:
    mkdir(item)

# _build()
_build(root_dir="../base/dict")
_build(root_dir="../thfund/dict", product="thfund")
_build(root_dir="../smartwhale/dict", product="smartwhale")
