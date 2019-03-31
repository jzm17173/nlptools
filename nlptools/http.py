# -*- coding:utf-8 -*-

import json as json2
import socket
from urllib import request
from urllib import parse


def _decode(result):
    u"""解码

    Parameters
    ----------
    result : bytes

    Returns
    -------
    {str, None}

    """
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
    u"""序列化提交的数据

    Parameters
    ----------
    data : dict

    Returns
    -------
    str

    """
    return parse.urlencode(list(data.items()))


def get(
        url,
        data=None,
        headers={},
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    u"""get 请求

    Parameters
    ----------
    url : str
        请求地址
    data : dict, optional, default=None
        请求提交数据
    headers : dict, optional, default={}
        请求头部
    timeout : int, optional, default=socket._GLOBAL_DEFAULT_TIMEOUT
        请求超时

    Returns
    -------
    {str, None}

    """
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

    Parameters
    ----------
    url : str
        请求地址
    data : dict, optional, default=None
        请求提交数据
    json : dict, optional, default=None
        请求提交数据，数据以json形式提交
    headers : dict, optional, default={}
        请求头部
    timeout : int, optional, default=socket._GLOBAL_DEFAULT_TIMEOUT
        请求超时

    Returns
    -------
    {str, None}

    Notes
    -----
    Referer
    User-Agent
    Content-Type
        application/x-www-form-urlencoded;charset=utf-8

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
    u"""http 请求

    Parameters
    ----------
    url : str
        请求地址
    data : dict, optional, default=None
        请求提交数据
    json : dict, optional, default=None
        请求提交数据，数据以json形式提交
    headers : dict, optional, default={}
        请求头部
    timeout : int, optional, default=socket._GLOBAL_DEFAULT_TIMEOUT
        请求超时
    method : {"GET", "POST"}, optional, default="GET"
        请求方法
    data_type : {"json", None}, optional, default=None
        请求数据的类型

    Returns
    -------
    {str, None}

    """
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
