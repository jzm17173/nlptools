# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import nlptools


def sample_freq_dist():
    dist = nlptools.FreqDist("abcdeabcdabcaba")
    print(dist )  # FreqDist({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1})

    print(dist.keys())  # dict_keys(['a', 'b', 'c', 'd', 'e'])

    print(dist.items())  # dict_items([('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)])

    print(dist["a"])  # 5

    print(dist.most_common(3))  # [('a', 5), ('b', 4), ('c', 3)]
    print(dist.most_common())  # [('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)]

    print(dist.values())  # dict_values([5, 4, 3, 2, 1])

    print(dist.N())  # 15

    print(dist.B())  # 5

    print(dist.freq("a"))  # 0.3333333333333333

    print(dist.hapaxes())  # ['e']

    print(dist.filter("greater_than_or_equal[2]"))  # [('a', 5), ('b', 4), ('c', 3), ('d', 2)]
    print(dist.filter("less_than_or_equal[2]"))  # [('d', 2), ('e', 1)]
    print(dist.filter("equal[2]"))  # [('d', 2)]

    print(list(dist.keys()))
    print("".join(dist.keys()))


def sample_diff():
    nlptools.diff("files/diff1.txt", "files/diff2.txt")


def sample_search():
    nlptools.search(
        "files/search_sentences.txt",
        "files/search_contexts.txt",
        max_size=5,
        result_file="files/search_result.txt")


def sample_discovery_new_words():
    file = "files/newwords.txt"
    old_words = nlptools.load_dict("files/builtin.txt", mode="set")
    nlptools.discovery_new_words(
        file,
        old_words,
        max_size=5,
        result_path="files")


# sample_freq_dist()
# sample_diff()
# sample_search()
sample_discovery_new_words()
