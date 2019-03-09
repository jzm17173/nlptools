# -*- encoding=utf-8 -*-
u"""同义词"""

from .utility import _get_module_path
from .utility import load_syn_dict
from .utility import clean_text
from .utility import clean_word


dict_path = _get_module_path("dict")
syn_raw_file = "{}/syn_raw.txt".format(dict_path)
syn_tokens_file = "{}/syn_tokens.txt".format(dict_path)
syn_raw_dict = load_syn_dict(syn_raw_file)  # 用在分词前
syn_tokens_dict = load_syn_dict(syn_tokens_file)  # 用在分词后


def syn_cleaning(text, clean_type="text", extra_dict=[]):
    if clean_type == "text":
        return clean_text(text, syn_raw_dict + extra_dict)
    else:
        return clean_word(text, syn_tokens_dict + extra_dict)
