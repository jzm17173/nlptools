# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import bytelen


class TestString(unittest.TestCase):
    def test_bytelen(self):
        self.assertEqual(bytelen("北京欢迎您!"), 11)
        self.assertEqual(bytelen("assertEqual"), 11)
