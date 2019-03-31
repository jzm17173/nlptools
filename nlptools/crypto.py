# -*- coding:utf-8 -*-

import base64

from Crypto.Cipher import AES


_DEFAULT_PADDING = "\0"


def _pad(text, block_size, padding=_DEFAULT_PADDING):
    u"""填充

    Parameters
    ----------
    text : str
        待填充的文本
    block_size : int
        填充的最小单位
    padding : str, optional, default="\0"
        填充的文本

    Returns
    -------
    str

    """
    return "{}{}".format(text, (block_size - len(text) % block_size) * padding)


def _unpad(text, padding=_DEFAULT_PADDING):
    u"""移除填充

    Parameters
    ----------
    text : str
        待移除填充的文本
    padding : str, optional, default="\0"
        填充的文本

    Returns
    -------
    str

    """
    return text.rstrip(padding)


class AESCrypto(object):
    u"""AES加密解密

    Parameters
    ----------
    key : bytes
        密钥
    iv : bytes
        初始向量

    """
    def __init__(self, key, iv):
        self.key = key
        self.mode = AES.MODE_CBC  # 加密模式
        self.iv = iv

    def encrypt(self, text):
        u"""加密

        Parameters
        ----------
        text : str
            待加密的文本

        Returns
        -------
        str
            加密后的文本

        """
        text = _pad(text, len(self.key)).encode("utf-8")

        obj = AES.new(self.key, self.mode, self.iv)
        ciphertext = obj.encrypt(text)

        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt(self, text):
        u"""解密

        Parameters
        ----------
        text : str
            待解密的文本

        Returns
        -------
        {str, None}
            解密后的文本，None表示不匹配的加密文本

        """
        try:
            text = text.encode("utf-8")
            text = base64.b64decode(text)

            obj = AES.new(self.key, self.mode, self.iv)
            plaintext = obj.decrypt(text)

            return _unpad(plaintext.decode("utf-8"))
        except:
            return None
