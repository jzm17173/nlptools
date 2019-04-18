# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import pad_num
from nlptools import normalize_num
from nlptools import grouping


class TestNumber(unittest.TestCase):
    def test_pad_num(self):
        self.assertEqual(pad_num("3", 2), "03")
        self.assertEqual(pad_num("11", 2), "11")
        self.assertEqual(pad_num("3", 6), "000003")

    def test_normalize_num(self):
        self.assertEqual(normalize_num("100,000,000"), "100000000")
        self.assertEqual(normalize_num("100.000"), "100")
        self.assertEqual(normalize_num("100.1000"), "100.1")

    def test_grouping(self):
        nums = [3, 47, 47, 47, 46, 21, 59, 59, 10, 59, 20]

        self.assertEqual(
            str(grouping(nums)),
            "[0, [1, 2, 3, 4], 5, [6, 7, 8, 9], 10]")
        self.assertEqual(
            str(grouping(nums, max_diff=0)),
            "[0, 1, 2, 3, 4, 5, [6, 7, 8, 9], 10]")
        self.assertEqual(
            str(grouping(nums, max_diff=0, skip=False)),
            "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
