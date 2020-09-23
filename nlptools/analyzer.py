# -*- coding:utf-8 -*-

from pathlib import Path
from collections import Counter

from .fs import read_file
from .fs import write_file
from .fs import file_tail
from .utils import load_data
from .utils import generate_name


_rule_dict = {
    "greater_than_or_equal": lambda x, y: x >= y,
    "greater_than": lambda x, y: x > y,
    "less_than_or_equal": lambda x, y: x <= y,
    "less_than": lambda x, y: x < y,
    "equal": lambda x, y: x == y
}

_RULE_TYPES = [
    "greater_than_or_equal",
    "greater_than",
    "less_than_or_equal",
    "less_than",
    "equal"
]


class FreqDist(Counter):
    u"""词频分布

    Parameters
    ----------
    samples : list
        待统计词频的词列表

    Attributes
    ----------
    _N : {None, int}

    """
    def __init__(self, samples):
        Counter.__init__(self, samples)

        self._N = None

    def N(self):
        if self._N is None:
            self._N = sum(self.values())

        return self._N

    def B(self):
        return len(self)

    def freq(self, sample):
        n = self.N()
        if n == 0:
            return 0
        return self[sample] / n

    def hapaxes(self):
        return [item for item in self if self[item] == 1]

    def filter(self, rule="greater_than_or_equal[1]"):
        rule_type = _RULE_TYPES[0]
        rule_value = 1

        if rule.find("[") != -1:
            rule_value = rule.split("[")[1].split("]")[0]
            if rule_value.isdigit():
                rule_value = int(rule_value)

        for item in _RULE_TYPES:
            if rule.find(item) != -1:
                rule_type = item
                break

        return [
            item
            for item in self.most_common()
            if _rule_dict[rule_type](item[1], rule_value)]


def diff(dest, src, case_sensitive=False):
    u"""源文件在目标文件中有的和没有的

    Parameters
    ----------
    dest : {str, list}
        目标文件

    src : str
        源文件

    case_sensitive : {True, False}, optional, default=False
        是否区分大小写

    """
    if not isinstance(dest, list):
        dest = [dest]

    if len([item for item in dest if Path(item).is_file()]) != len(dest):
        raise Exception("有目标文件不存在")

    if not Path(src).is_file():
        raise Exception("源文件不存在")

    dest_data = []
    for item in dest:
        dest_data.extend(read_file(item).split("\n"))

    src_data = read_file(src).split("\n")

    src_data = [item.strip() for item in src_data if item.strip() != ""]
    dest_data = [item.strip() for item in dest_data if item.strip() != ""]
    dest_data_lowercase = [item.lower() for item in dest_data]
    dest_data_set = set(dest_data_lowercase) if not case_sensitive else set(dest_data)

    contains_data = []
    notcontains_data = []
    for item in src_data:
        if not case_sensitive:
            item = item.lower()

        if item in dest_data_set:
            contains_data.append(item)
        else:
            notcontains_data.append(item)

    write_file(
        file_tail(src, tail="_contains"), "\n".join(contains_data))
    write_file(
        file_tail(src, tail="_notcontains"), "\n".join(notcontains_data))


def _every(sentence, rules):
    u"""全匹配"""
    result = True

    for rule in rules:
        word = rule.strip("^BE")
        size = len(word)

        index = sentence.find(word)
        rword = sentence[-size:]

        if rule[0] == "^":
            if rule[1] == "B":
                if index == 0:
                    return False
            elif rule[1] == "E":
                if rword == word:
                    return False
            else:
                if index != -1:
                    return False
        else:
            if rule[0] == "B":
                if index != 0:
                    return False
            elif rule[0] == "E":
                if rword != word:
                    return False
            else:
                if index == -1:
                    return False

    return result


def context_exists(sentence, context):
    u"""上下文判断

    Parameters
    ----------
    sentence : str
        句子

    context : str
        上下文

        "召开方式&^只能选择|表决方式&^只能选择|相结合&^只能选择"

        | 或
        & 并
        ^ 非
        B 开头
        E 结尾

        第一层都是|
        第二层都是&

        解析过程：
        [
            "召开方式&^只能选择",
            "表决方式&^只能选择",
            "相结合&^只能选择"
        ]

        [
            ["召开方式", "^只能选择"],
            ["表决方式", "^只能选择"],
            ["相结合", "^只能选择"]
        ]

    Returns
    -------
    bool

    """
    if context == "":
        return True

    rules = [item.split("&") for item in context.split("|")]

    for item in rules:
        if _every(sentence, item):
            return True

    return False


def search(sentences, contexts, max_size=None, result_file=None):
    u"""搜索

    Parameters
    ----------
    sentences : {str, list}
        句子列表或者文件

    contexts : {str, list}
        上下文列表或者文件

    max_size : {int, None}, optional, default=None
        最多问题数

    result_file : {str, None}, optional, default=None
        结果文件路径

    """
    if isinstance(sentences, str):
        sentences = load_data(sentences)

    if isinstance(contexts, str):
        contexts = load_data(contexts)

    text = []

    for context in contexts:
        text.append("\n\n{}\n{}\n\n".format("-" * 30, context))
        questions = []
        for sentence in sentences:
            if context_exists(sentence, context):
                if max_size is None or len(questions) < max_size:
                    questions.append("    {}".format(sentence))
                else:
                    break
        text.extend(questions)

    if result_file is None:
        result_file = "{}_search.txt".format(generate_name())

    write_file(result_file, "\n".join(text))


def discovery_new_words(file, old_words, max_size=None, result_path=None):
    u"""发现新词

    Parameters
    ----------
    file : str
        文件路径

    old_words : set
        常用词，已在字典里的词

    max_size : {int, None}, optional, default=None
        最多问题数

    result_path : {str, None}, optional, default=None
        结果文件目录

    """
    sentences = load_data(file)

    words = []
    for item in sentences:
        words.extend(item.split())

    dist = FreqDist(words)
    name = generate_name()

    notcontains1_text = []
    notcontainsn_text = []
    contains_text = []

    notcontains1_contexts = []
    notcontainsn_contexts = []

    for word, count in dist.most_common():
        line = "{} {}".format(word, count)

        if word not in old_words:
            if len(word) == 1:
                notcontains1_text.append(line)
                notcontains1_contexts.append(word)
            else:
                notcontainsn_text.append(line)
                notcontainsn_contexts.append(word)
        else:
            contains_text.append(line)

    if result_path is None:
        result_path = ""
    else:
        result_path = "{}/".format(result_path)

    write_file(
        "{}{}_newwords_notcontains1.txt".format(result_path, name),
        "\n".join(notcontains1_text))
    write_file(
        "{}{}_newwords_notcontainsn.txt".format(result_path, name),
        "\n".join(notcontainsn_text))
    write_file(
        "{}{}_newwords_contains.txt".format(result_path, name),
        "\n".join(contains_text))

    search(
        sentences,
        notcontains1_contexts,
        max_size=max_size,
        result_file="{}{}_search_notcontains1.txt".format(result_path, name))
    search(
        sentences,
        notcontainsn_contexts,
        max_size=max_size,
        result_file="{}{}_search_notcontainsn.txt".format(result_path, name))
