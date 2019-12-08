# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import nlptools


syn_raw_file = "files/syn_raw.txt"
syn_tokens_file = "files/syn_tokens.txt"
syn_raw_dict = nlptools.load_syn_dict(syn_raw_file)
syn_tokens_dict = nlptools.load_syn_dict(syn_tokens_file)


def sample_syn_cleaning():
    text1 = nlptools.syn_cleaning("我绑定不上手机", syn_raw_dict)
    text2 = nlptools.syn_cleaning("扣费", syn_tokens_dict, mode="word")
    print(text1)
    print(text2)


sample_syn_cleaning()
