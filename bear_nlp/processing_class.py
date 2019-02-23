# -*- encoding=utf-8 -*-
u"""类别"""

from .utility import _get_module_path
from .utility import load_syn_dict
from .utility import clean_word


dict_path = _get_module_path("dict")
class_file = "{}/class.txt".format(dict_path)
class_dict = load_syn_dict(class_file, mode="set")


def class_cleaning(word, extra_dict={}):
    all_dict = {}
    all_dict.update(class_dict)
    all_dict.update(extra_dict)
    return clean_word(word, all_dict, mode="set")
