# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import full2half


class TestFullHalf(unittest.TestCase):
    def test_full2half(self):
        self.assertEqual(full2half("　"), " ")
