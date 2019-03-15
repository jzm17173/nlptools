# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest
from pathlib import Path

from nlptools import mkdir


class TestCalc(unittest.TestCase):
    def test_mkdir(self):
        mkdir("a")
        mkdir("a/b")

        self.assertTrue(Path("a").is_dir())
        self.assertTrue(Path("a/b").is_dir())
