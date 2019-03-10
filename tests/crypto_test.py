# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import unittest

import nlptools


class TestCrypto(unittest.TestCase):
    def test_aescrypto(self):
        key = b"1234567890111111"
        iv = b"1234567890222222"
        text = "how are you"
        obj = nlptools.AESCrypto(key, iv)
        ciphertext = obj.encrypt(text)
        plaintext = obj.decrypt(ciphertext)
        self.assertEqual(text, plaintext)
