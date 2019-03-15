# -*- coding:utf-8 -*-

import json as json2
import socket
from urllib import request
from urllib import parse


def _decode(result):
    try:
        return result.decode("utf-8")
    except Exception as e:
        print(e)

    try:
        return result.decode("gbk")
    except Exception as e:
        print(e)
        return None


def serialize(data):
    return parse.urlencode(list(data.items()))


def get(
        url,
        data=None,
        headers={},
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    u"""get 请求"""
    if data is not None:
        search = serialize(data)
        url = "{}?{}".format(url, search)

    req = request.Request(url, data=None, headers=headers)

    try:
        with request.urlopen(req, timeout=timeout) as f:
            result = f.read()
    except Exception as e:
        print(e)
        return None

    return _decode(result)


def post(
        url,
        data=None,
        json=None,
        headers={},
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    u"""post 请求

    application/x-www-form-urlencoded;charset=utf-8

    Referer
    User-Agent
    Content-Type
    """
    content_type = None

    if data is not None:
        body = serialize(data)
    elif json is not None:
        body = json2.dumps(data)
        content_type = "application/json"
    else:
        body = ""

    if content_type and "Content-Type" not in headers:
        headers["Content-Type"] = content_type

    req = request.Request(url, data=body.encode("utf-8"), headers=headers)

    try:
        with request.urlopen(req, timeout=timeout) as f:
            result = f.read()
    except Exception as e:
        print(e)
        return None

    return _decode(result)


def fetch(
        url,
        data=None,
        json=None,
        headers={},
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
        method="GET",
        data_type=None):
    u"""请求"""
    if method == "GET":
        result = get(
            url,
            data=data,
            headers=headers,
            timeout=timeout)
    else:
        result = post(
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout)

    if data_type == "json":
        if result is not None:
            return json2.loads(result)

    return result
