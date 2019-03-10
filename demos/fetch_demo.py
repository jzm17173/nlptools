# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import nlptools


def demo_get():
    url = "http://www.bing.com/"

    data = {
        "q": "什么是销户"
    }

    result = nlptools.get(url, data, timeout=3)

    print(result)


def demo_post():
    url = "http://www.nanakon.com/category/get"

    data = {
        "user_id": 1
    }

    result = nlptools.post(url, data, timeout=3)

    print(result)


demo_get()
demo_post()
