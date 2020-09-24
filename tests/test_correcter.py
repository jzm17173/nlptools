# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


_TYPOS_RAW_FILE = _get_module_path("files/typos_raw.txt")
_TYPOS_RAW_DICT = nlptools.load_syn_dict(_TYPOS_RAW_FILE)


class TestCorrecter(unittest.TestCase):
    def test_typos_cleaning(self):
        self.assertEqual(
            nlptools.typos_cleaning("可然冰是什么", _TYPOS_RAW_DICT), "可燃冰是什么")

    def test_stock_cleaning(self):
        self.assertEqual(nlptools.stock_cleaning("6oo57o"), "600570")


if __name__ == '__main__':
    unittest.main()
