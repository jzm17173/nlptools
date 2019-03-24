# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")


from nlptools import read_file
from nlptools import full2half
from nlptools import start_time
from nlptools import get_delta


def full2half2(text):
    new_text = []

    for char in text:
        code = ord(char)
        if code == 12288:  # 全角空格
            code = 32
        elif code >= 65281 and code <= 65374:
            code -= 65248
        new_text.append(chr(code))

    return "".join(new_text)


def test_full2half():
    text = read_file("files/2000.txt")
    text2 = text * 10
    text3 = text * 100

    print("{} full2half 2000".format("-" * 30))
    start_time()
    full2half(text)
    print(get_delta())

    print("{} full2half 2w".format("-" * 30))
    start_time()
    full2half(text2)
    print(get_delta())

    print("{} full2half 20w".format("-" * 30))
    start_time()
    full2half(text3)
    print(get_delta())


def test_full2half2():
    text = read_file("files/2000.txt")
    text2 = text * 10
    text3 = text * 100

    print("{} full2half2 2000".format("-" * 30))
    start_time()
    full2half2(text)
    print(get_delta())

    print("{} full2half2 2w".format("-" * 30))
    start_time()
    full2half2(text2)
    print(get_delta())

    print("{} full2half2 20w".format("-" * 30))
    start_time()
    full2half2(text3)
    print(get_delta())


test_full2half()
test_full2half2()

u"""
------------------------------ full2half 2000
1.00ms
------------------------------ full2half 2w
0.00ms
------------------------------ full2half 20w
4.00ms
------------------------------ full2half2 2000
1.00ms
------------------------------ full2half2 2w
9.00ms
------------------------------ full2half2 20w
93.00ms
"""
