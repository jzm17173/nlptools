# -*- coding:utf-8 -*-

import json
import socket
from urllib import request
from urllib import parse


DEFAULT_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT
u"""timeout

help(request.urlopen)
    urlopen(url, data=None, timeout=<object object at 0x10acce160>,
        *, cafile=None, capath=None, cadefault=False, context=None)

import socket
socket._GLOBAL_DEFAULT_TIMEOUT
    <object object at 0x10acce160>

https://segmentfault.com/q/1010000004935548
"""
DEFAULT_POST_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=utf-8"


def get(
        url,
        data=None,
        timeout=DEFAULT_TIMEOUT,
        user_agent=None,
        referer=None):
    u"""get 请求"""
    if data is not None:
        url += "?%s" % parse.urlencode(list(data.items()))

    req = request.Request(url)

    if user_agent:
        req.add_header("User-Agent", user_agent)

    if referer:
        req.add_header("Referer", referer)

    try:
        with request.urlopen(req, data=None, timeout=timeout) as f:
            result = f.read()
    except Exception as e:
        print(e)
        return None

    try:
        return result.decode("utf-8")
    except Exception as e:
        print(e)

    try:
        return result.decode("gbk")
    except Exception as e:
        print(e)
        return None


def post(
        url,
        data=None,
        req_type=None,
        timeout=DEFAULT_TIMEOUT,
        content_type=DEFAULT_POST_CONTENT_TYPE,
        user_agent=None,
        referer=None):
    u"""post 请求"""
    req = request.Request(url)

    req.add_header("Content-Type", content_type)

    if user_agent:
        req.add_header("User-Agent", user_agent)

    if referer:
        req.add_header("Referer", referer)

    if data is None:
        data_str = ""
    elif req_type == "json":
        data_str = json.dumps(data)
    else:
        data_str = parse.urlencode(list(data.items()))

    try:
        with request.urlopen(
                req, data=data_str.encode("utf-8"), timeout=timeout) as f:
            result = f.read()
    except Exception as e:
        print(e)
        return None

    try:
        return result.decode("utf-8")
    except Exception as e:
        print(e)

    try:
        return result.decode("gbk")
    except Exception as e:
        print(e)
        return None


def fetch(
        url,
        data=None,
        method="GET",
        req_type=None,
        res_type=None,
        timeout=DEFAULT_TIMEOUT,
        content_type=DEFAULT_POST_CONTENT_TYPE,
        user_agent=None,
        referer=None):
    u"""请求"""
    if method == "GET":
        result = get(
            url,
            data=data,
            timeout=timeout,
            user_agent=user_agent,
            referer=referer)
    else:
        result = post(
            url,
            data=data,
            req_type=req_type,
            timeout=timeout,
            content_type=content_type,
            user_agent=user_agent,
            referer=referer)

    if res_type == "json":
        if result is not None:
            return json.loads(result)

    return result
