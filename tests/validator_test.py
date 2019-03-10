# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

from nlptools import is_int
from nlptools import is_float
from nlptools import is_email
from nlptools import verify
from nlptools import verify_page


class TestValidator(unittest.TestCase):
    def test_is_int(self):
        self.assertTrue(is_int("1"))
        self.assertTrue(is_int("-1"))
        self.assertFalse(is_int("-"))
        self.assertFalse(is_int("1.1"))
        self.assertFalse(is_int("-1.1"))
        self.assertFalse(is_int("abc"))

    def test_is_float(self):
        self.assertTrue(is_float("1"))
        self.assertTrue(is_float("1.1"))
        self.assertTrue(is_float("-1.1"))
        self.assertFalse(is_float(".0"))
        self.assertFalse(is_float("abc"))

    def test_is_email(self):
        self.assertTrue(is_email("123456@qq.com"))
        self.assertFalse(is_email("123456qq.com"))

    def test_verify(self):
        self.assertTrue(verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": ""
            }
        ]), "{}不能为空".format("nickname"))

        self.assertTrue(verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": ""
            }
        ], {
            "required": "{}是必须的",
        }), "{}是必须的".format("nickname"))

        self.assertEqual(verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": "abc"
            }
        ]), None)

        self.assertEqual(verify([
            {
                "name": "email",
                "rule": "valid_email",
                "value": "123456@qq.com"
            }
        ]), None)

        self.assertEqual(verify([
            {
                "name": "email",
                "rule": "valid_email",
                "value": "123456qq.com"
            }
        ]), "{}格式错误".format("email"))

    def test_verify_page(self):
        self.assertEqual(verify_page(-1, 100), "{}不能小于等于{}".format("page", 0))
