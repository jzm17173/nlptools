# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import nlptools


def demo_load_dict():
    data1 = nlptools.load_dict("dict/custom.txt")
    data2 = nlptools.load_dict("dict/custom.txt", mode="set")
    print(data1)
    print(data2)


def demo_load_syn_dict():
    data1 = nlptools.load_syn_dict("dict/syn_tokens.txt")
    data2 = nlptools.load_syn_dict("dict/syn_tokens.txt", mode="set")
    print(data1)
    print(data2)


def demo_clean_text():
    text = nlptools.clean_text("我的账号是,你的账户呢？", [["账号", "账户"]])
    print(text)


def demo_clean_word():
    word1 = nlptools.clean_word("账户", {"账号": {"账户"}}, mode="set")
    word2 = nlptools.clean_word("账户", [["账号", "账户"]])
    print(word1)
    print(word2)


def demo_generate_name():
    name1 = nlptools.generate_name()
    name2 = nlptools.generate_name("timestamp")
    name3 = nlptools.generate_name("uuid")

    print(name1)
    print(name2)
    print(name3)


demo_load_dict()
demo_load_syn_dict()
demo_clean_text()
demo_clean_word()
demo_generate_name()
