# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

import nlptools


def demo_now():
    t1 = nlptools.now()
    t2 = nlptools.now(format="%Y%m%d%H%M%S")

    print(t1)  # 2019-03-10 15:28:29
    print(t2)  # 20190310152829


demo_now()
