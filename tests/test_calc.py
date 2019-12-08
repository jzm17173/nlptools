# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


class TestCalc(unittest.TestCase):
    def test_num_add(self):
        num1 = 1.001
        num2 = 1.022
        num3 = 2.023
        self.assertNotEqual(num1 + num2, num3)
        self.assertEqual(nlptools.num_add(num1, num2), str(num3))

    def test_num_sub(self):
        num1 = 1.001
        num2 = 1.022
        num3 = -0.021
        self.assertNotEqual(num1 - num2, num3)
        self.assertEqual(nlptools.num_sub(num1, num2), str(num3))

    def test_num_multi(self):
        num1 = 1.1
        num2 = 1.1
        num3 = 1.21
        self.assertNotEqual(num1 * num2, num3)
        self.assertEqual(nlptools.num_multi(num1, num2), str(num3))
        self.assertNotEqual(nlptools.num_multi("0.013", 100), "1.300")
        self.assertEqual(nlptools.num_multi("0.013", 100), "1.3")

    def test_num_div(self):
        num1 = 1.21
        num2 = 1.1
        num3 = 1.1
        self.assertNotEqual(num1 / num2, num3)
        self.assertEqual(nlptools.num_div(num1, num2), str(num3))


if __name__ == '__main__':
    unittest.main()
