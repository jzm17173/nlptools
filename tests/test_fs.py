# -*- coding: utf-8 -*-

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))

import nlptools


def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


class TestCalc(unittest.TestCase):
    def test_mkdir(self):
        nlptools.mkdir("a")
        nlptools.mkdir("a/b")

        self.assertTrue(Path("a").is_dir())
        self.assertTrue(Path("a/b").is_dir())

        nlptools.rmdir("a/b")
        nlptools.rmdir("a")

    def test_scan(self):
        FILE_NUM = 6
        TEST_NUM = 8
        files = nlptools.scan(_get_module_path('../tests'))
        self.assertEqual(len([file for file in files if "test_" in file and file.endswith(".py")]), TEST_NUM)
        self.assertEqual(len([file for file in files if ".txt" in file]), FILE_NUM)


if __name__ == '__main__':
    unittest.main()
