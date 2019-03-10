# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import nlptools


syn_raw_file = "dict/syn_raw.txt"
syn_tokens_file = "dict/syn_tokens.txt"
syn_raw_dict = nlptools.load_syn_dict(syn_raw_file)
syn_tokens_dict = nlptools.load_syn_dict(syn_tokens_file)


def demo_syn_cleaning():
    text1 = nlptools.syn_cleaning("我绑定不上手机", syn_raw_dict)
    text2 = nlptools.syn_cleaning("扣费", syn_tokens_dict, mode="word")
    print(text1)
    print(text2)


demo_syn_cleaning()
