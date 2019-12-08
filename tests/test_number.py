# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


class TestNumber(unittest.TestCase):
    def test_pad_num(self):
        self.assertEqual(nlptools.pad_num("3", 2), "03")
        self.assertEqual(nlptools.pad_num("11", 2), "11")
        self.assertEqual(nlptools.pad_num("3", 6), "000003")

    def test_normalize_num(self):
        self.assertEqual(nlptools.normalize_num("100,000,000"), "100000000")
        self.assertEqual(nlptools.normalize_num("100.000"), "100")
        self.assertEqual(nlptools.normalize_num("100.1000"), "100.1")
        self.assertEqual(nlptools.normalize_num("10.0%"), "10%")

    def test_grouping(self):
        nums = [3, 47, 47, 47, 46, 21, 59, 59, 10, 59, 20]

        indexes = nlptools.grouping(nums)
        self.assertEqual(
            str(indexes),
            "[0, [1, 2, 3, 4], 5, [6, 7, 8, 9], 10]")

        indexes = nlptools.grouping(nums, max_diff=0)
        self.assertEqual(
            str(indexes),
            "[0, [1, 2, 3], 4, 5, [6, 7, 8, 9], 10]")

        indexes = nlptools.grouping(nums, max_diff=0, skip=False)
        self.assertEqual(
            str(indexes),
            "[0, [1, 2, 3], 4, 5, 6, 7, 8, 9, 10]")

        nums = [0, 0, 0, 0, 43, 43, 43, 44, 21]
        indexes = nlptools.grouping(
            nums, max_diff=0, min_num=1, skip=False)
        self.assertEqual(
            str(indexes),
            "[0, 1, 2, 3, [4, 5, 6], 7, 8]")

        nums = [10, 4, 10, 4, 10, 4, 43, 44, 21]
        indexes = nlptools.grouping(
            nums, max_diff=0, min_num=1)
        self.assertEqual(
            str(indexes),
            "[[0, 1, 2, 3, 4], 5, 6, 7, 8]")


if __name__ == '__main__':
    unittest.main()
