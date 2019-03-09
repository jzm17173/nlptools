# -*- coding: utf-8 -*-

import unittest

from bear_utils import is_int
from bear_utils import is_float
from bear_utils import is_email
from bear_utils import verify


class TestValidator(unittest.TestCase):
    def test_is_int(self):
        self.assertTrue(is_int("1"))
        self.assertTrue(is_int("-1"))
        self.assertEqual(is_int("-"), None)
        self.assertEqual(is_int("1.1"), None)
        self.assertEqual(is_int("-1.1"), None)
        self.assertEqual(is_int("abc"), None)

    def test_is_float(self):
        self.assertTrue(is_float("1"))
        self.assertTrue(is_float("1.1"))
        self.assertTrue(is_float("-1.1"))
        self.assertEqual(is_float(".0"), None)
        self.assertEqual(is_float("abc"), None)

    def test_is_email(self):
        self.assertTrue(is_email("123456@qq.com"))

    def test_verify(self):
        self.assertTrue(verify([
            {
                "name": "nickname",
                "rule": "required",
                "value": ""
            }
        ]), "{}不能为空".format("nickname"))

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
