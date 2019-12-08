# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


def _get_module_path(path):
    return os.path.normpath(os.path.join(os.getcwd(),
                            os.path.dirname(__file__), path))


typos_raw_file = _get_module_path("files/typos_raw.txt")
typos_raw_dict = nlptools.load_syn_dict(typos_raw_file)


class TestCorrecter(unittest.TestCase):
    def test_typos_cleaning(self):
        self.assertEqual(
            nlptools.typos_cleaning("可然冰是什么", typos_raw_dict), "可燃冰是什么")

    def test_stock_cleaning(self):
        self.assertEqual(nlptools.stock_cleaning("6oo57o"), "600570")


if __name__ == '__main__':
    unittest.main()
