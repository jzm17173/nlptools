# -*- coding: utf-8 -*-

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))

import nlptools


class TestCalc(unittest.TestCase):
    def test_mkdir(self):
        nlptools.mkdir("a")
        nlptools.mkdir("a/b")

        self.assertTrue(Path("a").is_dir())
        self.assertTrue(Path("a/b").is_dir())

        nlptools.rmdir("a/b")
        nlptools.rmdir("a")


if __name__ == '__main__':
    unittest.main()
