# -*- coding:utf-8 -*-

import re


_INT_RE = re.compile("^\-?\d+$")
_FLOAT_RE = re.compile("^(\-?\d+)(\.\d+)?$")
_EMAIL_RE = re.compile(
    "^([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+@([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+\.[A-Z]{2,3}$",
    re.I)
_LETTER_NUMBER_RE = re.compile("^[\dA-Z]+$", re.I)

_DEFAULT_MESSAGE_FORMAT = {
    "required": "{}不能为空",
    "valid_email": "{}格式错误",
    "min_length": "{}长度不能小于{}",
    "max_length": "{}长度不能大于{}",
    "exact_length": "{}长度不是{}",
    "matches": "{}不一致",
    "numeric": "{}不是数值",
    "integer": "{}不是整数",
    "greater_than_or_equal": "{}不能小于{}",
    "greater_than": "{}不能小于等于{}",
    "less_than_or_equal": "{}不能大于{}",
    "less_than": "{}不能大于等于{}"
}


def is_int(value):
    u"""是否整型

    Parameters
    ----------
    value : str
        字符串

    Returns
    -------
    bool

    Notes
    -----
    str.isdigit() 是否只由数字组成，“-”、“.”也不包括

    """
    if _INT_RE.match(str(value)):
        return True
    else:
        return False


def is_float(value):
    u"""是否浮点型

    Parameters
    ----------
    value : str
        字符串

    Returns
    -------
    bool

    """
    if _FLOAT_RE.match(str(value)):
        return True
    else:
        return False


def is_email(value):
    u"""是否邮件

    Parameters
    ----------
    value : str
        字符串

    Returns
    -------
    bool

    """
    if _EMAIL_RE.match(str(value)):
        return True
    else:
        return False


def only_letters_and_numbers(value):
    u"""是否只包含字母、数字

    Parameters
    ----------
    value : str
        字符串

    Returns
    -------
    bool

    """
    if _LETTER_NUMBER_RE.match(value):
        return True
    else:
        return False


def check(rules, message_format={}):
    u"""验证

    Parameters
    ----------
    rules : [{str: str}]
        规则列表

        name : str
            字段名
        rule : {"required",
                "valid_email",
                "min_length[x]",
                "max_length[x]",
                "exact_length[x]",
                "matches[x]",
                "numeric",
                "integer",
                "greater_than_or_equal[x]",
                "greater_than[x]",
                "less_than_or_equal[x]",
                "less_than[x]"}
            字段规则，x 为比较的值
        value : str
            字段值

    message_format : dict, optional, default={}
        错误信息格式

        默认的错误信息格式
            {
                "required": "{}不能为空",
                "valid_email": "{}格式错误",
                "min_length": "{}长度不能小于{}",
                "max_length": "{}长度不能大于{}",
                "exact_length": "{}长度不是{}",
                "matches": "{}不一致",
                "numeric": "{}不是数值",
                "integer": "{}不是整数",
                "greater_than_or_equal": "{}不能小于{}",
                "greater_than": "{}不能小于等于{}",
                "less_than_or_equal": "{}不能大于{}",
                "less_than": "{}不能大于等于{}"
            }

    Returns
    -------
    {str, None}
        返回错误信息或 None

    """
    for item in rules:
        rule = item.get("rule")
        name = item.get("name")
        value = item.get("value")

        rule_name = rule.split("[")[0]
        if rule == rule_name:
            rule_value = None
        else:
            rule_value = rule.split("[")[1].split("]")[0]

        message_exists = False

        if rule_name == "required":
            if value == "":
                message_exists = True
        elif rule_name == "valid_email":
            if not is_email(value):
                message_exists = True
        elif rule_name == "numeric":
            if not is_float(value):
                message_exists = True
        elif rule_name == "integer":
            if not is_int(value):
                message_exists = True
        elif rule_name == "min_length":
            if len(value) < int(rule_value):
                message_exists = True
        elif rule_name == "max_length":
            if len(value) > int(rule_value):
                message_exists = True
        elif rule_name == "exact_length":
            if len(value) != int(rule_value):
                message_exists = True
        elif rule_name == "matches":
            if value != rule_value:
                message_exists = True
        elif rule_name == "greater_than_or_equal":
            if float(value) < float(rule_value):
                message_exists = True
        elif rule_name == "greater_than":
            if float(value) <= float(rule_value):
                message_exists = True
        elif rule_name == "less_than_or_equal":
            if float(value) > float(rule_value):
                message_exists = True
        elif rule_name == "less_than":
            if float(value) >= float(rule_value):
                message_exists = True

        if message_exists:
            if rule_name in message_format:
                msg_format = message_format[rule_name]
            else:
                msg_format = _DEFAULT_MESSAGE_FORMAT[rule_name]

            if msg_format.count("{}") == 2:
                return msg_format.format(name, rule_value)
            else:
                return msg_format.format(name)

    return None


def check_page(page, row, extend=None, message_format={}):
    u"""验证分页

    Parameters
    ----------
    page : int
        页码

    row : int
        每页数据数

    extend : [{str: str}]
        扩展规则

        name : str
            字段名
        rule : {"required",
                "valid_email",
                "min_length[x]",
                "max_length[x]",
                "exact_length[x]",
                "matches[x]",
                "numeric",
                "integer",
                "greater_than_or_equal[x]",
                "greater_than[x]",
                "less_than_or_equal[x]",
                "less_than[x]"}
            字段规则，x 为比较的值
        value : str
            字段值

    message_format : dict, optional, default={}
        错误信息格式

        默认的错误信息格式
            {
                "required": "{}不能为空",
                "valid_email": "{}格式错误",
                "min_length": "{}长度不能小于{}",
                "max_length": "{}长度不能大于{}",
                "exact_length": "{}长度不是{}",
                "matches": "{}不一致",
                "numeric": "{}不是数值",
                "integer": "{}不是整数",
                "greater_than_or_equal": "{}不能小于{}",
                "greater_than": "{}不能小于等于{}",
                "less_than_or_equal": "{}不能大于{}",
                "less_than": "{}不能大于等于{}"

    Returns
    -------
    {str, None}
        返回错误信息或 None

    """
    rules = [
        {
            "name": "page",
            "rule": "numeric",
            "value": page
        },
        {
            "name": "row",
            "rule": "numeric",
            "value": row
        },
        {
            "name": "page",
            "rule": "greater_than[0]",
            "value": page
        },
        {
            "name": "row",
            "rule": "greater_than[0]",
            "value": row
        }
    ]

    if extend is not None:
        rules += extend

    return check(rules, message_format)
