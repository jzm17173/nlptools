# -*- coding:utf-8 -*-

import time
import datetime


def now():
    u"""当前时间"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def timestamp():
    u"""时间戳"""
    return str(int(time.time() * 1000))


def datetime2string(dt):
    u"""
    datetime.datetime(2015, 1, 1, 20, 23, 20)
    to "2015-01-01 20:23:20"
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string2datetime(value):
    u"""
    "2015-01-01 20:23:20"
    to datetime.datetime(2015, 1, 1, 20, 23, 20)
    """
    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def datetime_add(value, days=0, hours=0, minutes=0):
    u"""
    datetime_add('2016-10-01 10:10:10', 10)
    to datetime.datetime(2016, 10, 11, 10, 10, 10)
    """
    dt = string2datetime(value)
    return dt + datetime.timedelta(days=days, hours=hours, minutes=minutes)
