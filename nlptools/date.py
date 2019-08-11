# -*- coding:utf-8 -*-

import datetime


_DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"

_tstart = None
_tend = None


def now(format=_DEFAULT_FORMAT):
    u"""当前时间

    Parameters
    ----------
    format : str, optional, default=_DEFAULT_FORMAT

    Returns
    -------
    str

    """
    dt = datetime.datetime.now()
    return dt.strftime(format)


u"""
def now(format=_DEFAULT_FORMAT):
    return time.strftime(format, time.localtime())
"""


def timestamp():
    u"""当前时间戳

    Returns
    -------
    int

    """
    dt = datetime.datetime.now()
    return int(dt.timestamp() * 1000)


u"""
def timestamp():
    return int(time.time() * 1000)
"""


def datetime2string(dt, format=_DEFAULT_FORMAT):
    u"""datetime.datetime 转 str

    Parameters
    ----------
    dt : datetime.datetime
    format : str, optional, default=_DEFAULT_FORMAT

    Returns
    -------
    str

    """
    return dt.strftime(format)


def string2datetime(value, format=_DEFAULT_FORMAT):
    u"""str 转 datetime.datetime

    Parameters
    ----------
    value : str
    format : str, optional, default=_DEFAULT_FORMAT

    Returns
    -------
    datetime.datetime

    """
    return datetime.datetime.strptime(value, format)


def datetime_add(value, format=_DEFAULT_FORMAT, days=0, hours=0, minutes=0):
    u"""datetime 增加时间

    Parameters
    ----------
    value : str
    format : str, optional, default=_DEFAULT_FORMAT
    days : int, optional, default=0
    hours : int, optional, default=0
    minutes : int, optional, default=0

    Returns
    -------
    datetime.datetime

    """
    dt = string2datetime(value, format)
    return dt + datetime.timedelta(days=days, hours=hours, minutes=minutes)


def start_time():
    u"""设置开始时间"""
    global _tstart
    _tstart = timestamp()


def get_delta():
    u"""计算结束时间和开始时间的差值

    Returns
    -------
    str

    """
    global _tend
    _tend = timestamp()
    return "%.2fms" % (_tend - _tstart)
