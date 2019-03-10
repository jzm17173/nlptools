# -*- coding:utf-8 -*-

import base64

from Crypto.Cipher import AES


_DEFAULT_PADDING = "\0"


def _pad(text, block_size, padding=_DEFAULT_PADDING):
    return "{}{}".format(text, (block_size - len(text) % block_size) * padding)


def _unpad(text, padding=_DEFAULT_PADDING):
    return text.rstrip(padding)


class AESCrypto(object):
    def __init__(self, key, iv):
        self.key = key  # 秘钥 bytes
        self.mode = AES.MODE_CBC  # 加密模式
        self.iv = iv  # 初始向量 bytes

    def encrypt(self, text):
        text = _pad(text, len(self.key)).encode("utf-8")

        obj = AES.new(self.key, self.mode, self.iv)
        ciphertext = obj.encrypt(text)

        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt(self, text):
        try:
            text = text.encode("utf-8")
            text = base64.b64decode(text)

            obj = AES.new(self.key, self.mode, self.iv)
            plaintext = obj.decrypt(text)

            return _unpad(plaintext.decode("utf-8"))
        except:
            return None
