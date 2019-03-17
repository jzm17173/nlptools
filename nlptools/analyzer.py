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

_rule_types = [
    "greater_than_or_equal",
    "greater_than",
    "less_than_or_equal",
    "less_than",
    "equal"
]


class FreqDist(Counter):
    u"""词频分布"""

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
        rule_type = _rule_types[0]
        rule_value = 1

        if rule.find("[") != -1:
            rule_value = rule.split("[")[1].split("]")[0]
            if rule_value.isdigit():
                rule_value = int(rule_value)

        for item in _rule_types:
            if rule.find(item) != -1:
                rule_type = item
                break

        return [
            item
            for item in self.most_common()
            if _rule_dict[rule_type](item[1], rule_value)]


def diff(dest, src, case_sensitive=False):
    u"""源文件在目标文件中有的和没有的

    Args:
        dest: 目标文件
        src: 源文件
        case_sensitive: 是否区分大小写
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

    if not case_sensitive:
        src_data = [item.lower() for item in src_data]
        dest_data = [item.lower() for item in dest_data]

    dest_data = set(dest_data)

    contains_data = []
    notcontains_data = []
    for item in src_data:
        if item in dest_data:
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

    context

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
    """
    if context == "":
        return True

    rules = [item.split("&") for item in context.split("|")]

    for item in rules:
        if _every(sentence, item):
            return True

    return False


def search(sentences, contexts, max_size=None):
    u"""搜索"""
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

    write_file("search{}.txt".format(generate_name()), "\n".join(text))
