# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import nlptools


def sample_get():
    url = "http://www.bing.com/"

    data = {
        "q": "什么是销户"
    }

    result = nlptools.get(url, data, timeout=3)

    print(result)


def sample_post():
    url = "http://www.nanakon.com/category/get"

    data = {
        "user_id": 1
    }

    result = nlptools.post(url, data, timeout=3)

    print(result)


sample_get()
sample_post()
