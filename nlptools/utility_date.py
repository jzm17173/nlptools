# -*- coding:utf-8 -*-

import datetime


_DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"

_tstart = None
_tend = None

u"""
- time.time() 当前时间的纪元值
- time.localtime() 当前系统时区下的时间
- time.gmtime() 返回UTC时间

```
import time

now = time.time()
time.localtime(now)  # 省略参数，默认返回当前时间

time.time()
# 1551198332.8990002

time.localtime()
# time.struct_time(tm_year=2019, tm_mon=2, tm_mday=27,
    tm_hour=0, tm_min=25, tm_sec=39,
    tm_wday=2, tm_yday=58, tm_isdst=0)

time.gmtime()
time.struct_time(tm_year=2019, tm_mon=2, tm_mday=26,
    tm_hour=16, tm_min=25, tm_sec=51,
    tm_wday=1, tm_yday=57, tm_isdst=0)
```

"""


# def now(format=_DEFAULT_FORMAT):
#     u"""当前时间"""
#     return time.strftime(format, time.localtime())


def now(format=_DEFAULT_FORMAT):
    u"""当前时间"""
    dt = datetime.datetime.now()
    return dt.strftime(format)


# def timestamp():
#     u"""当前时间戳"""
#     return int(time.time() * 1000)


def timestamp():
    u"""当前时间戳"""
    dt = datetime.datetime.now()
    return int(dt.timestamp() * 1000)


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
    return "%.2fms" % (_tstart - _tend)
