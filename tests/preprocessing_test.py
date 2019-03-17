# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import load_syn_dict
from nlptools import class_cleaning
from nlptools import full2half
from nlptools import load_rule_dict
from nlptools import load_rule_pick_dict
from nlptools import rule_every_cleaning
from nlptools import rule_some_cleaning
from nlptools import rule_pick_cleaning
from nlptools import rule_extend_cleaning

class_dict = load_syn_dict("dict/class.txt", mode="set")

every_dict = load_rule_dict("dict/every.txt")
some_dict = load_rule_dict("dict/some.txt")
extend_dict = load_rule_dict("dict/extend.txt")
pick_dict = load_rule_pick_dict("dict/pick.txt")


class TestPreprocessing(unittest.TestCase):
    def test_class_cleaning(self):
        self.assertEqual(class_cleaning("纳威司达", class_dict), "美股")
        self.assertEqual(class_cleaning("平安银行", class_dict), "银行")

    def test_full2half(self):
        self.assertEqual(full2half("　"), " ")

    def test_rule_every_cleaning(self):
        print(rule_every_cleaning(["拿出"], every_dict))
        self.assertEqual(
            "".join(rule_every_cleaning(["拿出"], every_dict)),
            "卖出")

    def test_rule_some_cleaning(self):
        print(rule_some_cleaning(["银行", "卡"], some_dict))
        self.assertEqual(
            "".join(rule_some_cleaning(["银行", "卡"], some_dict)),
            "银行卡")

    def test_rule_extend_cleaning(self):
        print(rule_extend_cleaning(["余额宝", "升级"], extend_dict))
        self.assertEqual(
            "".join(rule_extend_cleaning(["余额宝", "升级"], extend_dict)),
            "余额宝升级余额宝升级余额宝升级余额宝升级")

    def test_rule_pick_cleaning(self):
        # set无序了
        print(rule_pick_cleaning(["卖出", "到账", "我"], pick_dict))
        self.assertTrue(
            len(rule_pick_cleaning(["卖出", "到账", "我"], pick_dict)) == 2)
