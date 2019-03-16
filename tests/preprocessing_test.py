# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import load_syn_dict
from nlptools import class_cleaning
from nlptools import full2half


class_dict = load_syn_dict("dict/class.txt", mode="set")


class TestPreprocessing(unittest.TestCase):
    def test_class_cleaning(self):
        self.assertEqual(class_cleaning("纳威司达", class_dict), "美股")
        self.assertEqual(class_cleaning("平安银行", class_dict), "银行")

    def test_full2half(self):
        self.assertEqual(full2half("　"), " ")
