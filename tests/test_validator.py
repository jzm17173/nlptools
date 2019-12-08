# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

import nlptools


class TestValidator(unittest.TestCase):
    def test_is_int(self):
        self.assertTrue(nlptools.is_int("1"))
        self.assertTrue(nlptools.is_int("-1"))
        self.assertFalse(nlptools.is_int("-"))
        self.assertFalse(nlptools.is_int("1.1"))
        self.assertFalse(nlptools.is_int("-1.1"))
        self.assertFalse(nlptools.is_int("abc"))

    def test_is_float(self):
        self.assertTrue(nlptools.is_float("1"))
        self.assertTrue(nlptools.is_float("1.1"))
        self.assertTrue(nlptools.is_float("-1.1"))
        self.assertFalse(nlptools.is_float(".0"))
        self.assertFalse(nlptools.is_float("abc"))

    def test_is_email(self):
        self.assertTrue(nlptools.is_email("123456@qq.com"))
        self.assertFalse(nlptools.is_email("123456qq.com"))

    def test_verify(self):
        self.assertTrue(nlptools.verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": ""
            }
        ]), "{}不能为空".format("nickname"))

        self.assertTrue(nlptools.verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": ""
            }
        ], {
            "required": "{}是必须的",
        }), "{}是必须的".format("nickname"))

        self.assertEqual(nlptools.verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": "abc"
            }
        ]), None)

        self.assertEqual(nlptools.verify([
            {
                "name": "email",
                "rule": "valid_email",
                "value": "123456@qq.com"
            }
        ]), None)

        self.assertEqual(nlptools.verify([
            {
                "name": "email",
                "rule": "valid_email",
                "value": "123456qq.com"
            }
        ]), "{}格式错误".format("email"))

    def test_verify_page(self):
        self.assertEqual(nlptools.verify_page(-1, 100), "{}不能小于等于{}".format("page", 0))


if __name__ == '__main__':
    unittest.main()
