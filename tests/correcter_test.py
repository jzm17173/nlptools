# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import load_syn_dict
from nlptools import typos_cleaning
from nlptools import stock_cleaning


typos_raw_file = "dict/typos_raw.txt"
typos_raw_dict = load_syn_dict(typos_raw_file)


class TestCorrecter(unittest.TestCase):
    def test_typos_cleaning(self):
        self.assertEqual(
            typos_cleaning("可然冰是什么", typos_raw_dict), "可燃冰是什么")

    def test_stock_cleaning(self):
        self.assertEqual(stock_cleaning("6oo57o"), "600570")
