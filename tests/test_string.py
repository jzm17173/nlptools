# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


class TestString(unittest.TestCase):
    def test_bytelen(self):
        self.assertEqual(nlptools.bytelen("北京欢迎您!"), 11)
        self.assertEqual(nlptools.bytelen("assertEqual"), 11)


if __name__ == '__main__':
    unittest.main()
