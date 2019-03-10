# -*- coding:utf-8 -*-

import re


_re_int = re.compile("^\-?\d+$")
_re_float = re.compile("^(\-?\d+)(\.\d+)?$")
_re_email = re.compile(
    "^([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+@([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+\.[A-Z]{2,3}$",
    re.I)

_message_format = {
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

    str.isdigit() 是否只由数字组成，“-”、“.”也不包括
    """
    if _re_int.match(str(value)):
        return True
    else:
        return False


def is_float(value):
    u"""是否浮点型"""
    if _re_float.match(str(value)):
        return True
    else:
        return False


def is_email(value):
    u"""是否邮件"""
    if _re_email.match(str(value)):
        return True
    else:
        return False


def verify(rules, message_format={}):
    u"""验证"""
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
                msg_format = _message_format[rule_name]

            if msg_format.count("{}") == 2:
                return msg_format.format(name, rule_value)
            else:
                return msg_format.format(name)

    return None


def verify_page(page, row, extend=None, message_format={}):
    u"""验证分页"""
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

    return verify(rules, message_format)
