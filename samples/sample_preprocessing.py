# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import nlptools


_SYN_RAW_FILE = "files/syn_raw.txt"
_SYN_TOKENS_FILE = "files/syn_tokens.txt"
_SYN_RAW_DICT = nlptools.load_syn_dict(_SYN_RAW_FILE)
_SYN_TOKENS_DICT = nlptools.load_syn_dict(_SYN_TOKENS_FILE)


def sample_syn_cleaning():
    text1 = nlptools.syn_cleaning("我绑定不上手机", _SYN_RAW_DICT)
    text2 = nlptools.syn_cleaning("扣费", _SYN_TOKENS_DICT, mode="word")
    print(text1)
    print(text2)


sample_syn_cleaning()
