# -*- coding:utf-8 -*-

import datetime


_DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"

_tstart = None
_tend = None


def now(format=_DEFAULT_FORMAT):
    u"""当前时间"""
    dt = datetime.datetime.now()
    return dt.strftime(format)


u"""
def now(format=_DEFAULT_FORMAT):
    return time.strftime(format, time.localtime())
"""


def timestamp():
    u"""当前时间戳"""
    dt = datetime.datetime.now()
    return int(dt.timestamp() * 1000)


u"""
def timestamp():
    return int(time.time() * 1000)
"""


def datetime2string(dt, format=_DEFAULT_FORMAT):
    u"""
    datetime.datetime(2015, 1, 1, 20, 23, 20)
    to "2015-01-01 20:23:20"
    """
    return dt.strftime(format)


def string2datetime(value, format=_DEFAULT_FORMAT):
    u"""
    "2015-01-01 20:23:20"
    to datetime.datetime(2015, 1, 1, 20, 23, 20)
    """
    return datetime.datetime.strptime(value, format)


def datetime_add(value, format=_DEFAULT_FORMAT, days=0, hours=0, minutes=0):
    u"""
    datetime_add('2016-10-01 10:10:10', 10)
    to datetime.datetime(2016, 10, 11, 10, 10, 10)
    """
    dt = string2datetime(value, format)
    return dt + datetime.timedelta(days=days, hours=hours, minutes=minutes)


def start_time():
    global _tstart
    _tstart = timestamp()


def get_delta():
    global _tend
    _tend = timestamp()
    return "%.2fms" % (_tend - _tstart)
