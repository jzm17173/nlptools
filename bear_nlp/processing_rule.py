# -*- encoding=utf-8 -*-
u"""规则"""

from .utility_file import read_file
from .utility import _get_module_path
from .analysis_freq_dist import FreqDist


def load_rule_pick_dict(file):
    text = read_file(file)
    if text is None:
        return None

    rule_dict = {
        "index": {},
        "data": []
    }

    lines = text.split("\n")
    lines = [line for line in lines if line.strip() != ""]

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
    text = read_file(file)
    if text is None:
        return None

    rule_dict = {
        "index": {},
        "index_notin": {},
        "data": []
    }

    lines = text.split("\n")
    lines = [line for line in lines if line.strip() != ""]

    for i in range(len(lines)):
        line = lines[i]
        line_splited = line.split("|")
        rule = line_splited[0].split("^")
        words_remove = rule[0].split()
        if len(rule) == 1:
            words_notin = []
        else:
            words_notin = rule[1].split()
        words_add = line_splited[1].split()

        for word in words_remove:
            if word not in rule_dict["index"]:
                rule_dict["index"][word] = []
            rule_dict["index"][word].append(i)

        for word in words_notin:
            if word not in rule_dict["index_notin"]:
                rule_dict["index_notin"][word] = []
            rule_dict["index_notin"][word].append(i)

        rule_dict["data"].append([words_remove, words_add, words_notin])

    return rule_dict


def rule_every_cleaning(tokens, rule_dict):
    if rule_dict is None:
        return tokens

    indexes = []
    tokens_unique = list(set(tokens))
    for j in range(len(tokens_unique)):
        indexes.extend(rule_dict["index"].get(tokens_unique[j], []))

    if len(indexes) > 0:
        index_matched = []
        index_dist = FreqDist(indexes)

        len_sorted = index_dist.filter("equal[%d]" % len(tokens_unique))

        if len(len_sorted) > 0:
            index_sorted = sorted(len_sorted, key=lambda x: x[0])

            for index in index_sorted:
                words = rule_dict["data"][index[0]]
                if len(words[0]) == index[1]:
                    index_matched.append(index)

            for index in index_matched[:1]:
                words = rule_dict["data"][index[0]]
                tokens = words[1][:]  # 如果 line 和 words[1] 指向相同引用，line 变 words[1] 也会变

    return tokens


def _rule_some_cleaning(tokens, rule_dict, mode="all", count=0):
    u"""
    mode:
        all 标准化的匹配的依次替换
        one 扩展词的匹配的替换第1个
            词频高的，顺序的，还要命中的，前 2 个条件不代表命中

    词典：
    1.其它规则没有这条规则的词
    2.其它规则有这条规则的词

    规则左边没有其它规则右边的词，或者有但词没有变化

    无依赖在前
    """
    indexes = []
    indexes_notin = []
    tokens_unique = list(set(tokens))
    for j in range(len(tokens_unique)):
        indexes.extend(rule_dict["index"].get(tokens_unique[j], []))
        indexes_notin.extend(rule_dict["index_notin"].get(tokens_unique[j], []))

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
        tokens = _rule_some_cleaning(tokens, rule_dict, mode="all", count=count)

    return tokens


def rule_pick_cleaning(tokens, rule_dict):
    u"""
    依次处理，词典要注意顺序，需要词多优先匹配的就排在前面
    """
    if rule_dict is None:
        return tokens

    indexes = []
    tokens_unique = list(set(tokens))
    for j in range(len(tokens_unique)):
        indexes.extend(rule_dict["index"].get(tokens_unique[j], []))

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
