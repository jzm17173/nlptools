# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

from nlptools.crypto import AESCrypto


AES_SECRET_KEY = "6030369686470256".encode("utf-8")  # 16位
AES_IV = "8174135459704062".encode("utf-8")  # 16位
URL = "http://47.96.19.183/api_sanjiaoshou/public/HundsunProd/Hundsun.php"


class TestCrypto(unittest.TestCase):
    def test_aescrypto(self):
        obj = AESCrypto(AES_SECRET_KEY, AES_IV)
        ciphertext = obj.encrypt(URL)
        plaintext = obj.decrypt(ciphertext)
        self.assertEqual(URL, plaintext)


if __name__ == '__main__':
    unittest.main()
