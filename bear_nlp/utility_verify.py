# -*- coding:utf-8 -*-

import re


def is_int(value):
    u"""是否整型

    str.isdigit() 是否只由数字组成，“-”、“.”也不包括
    """
    pattern = re.compile("^\-?\d+$")
    return pattern.match(value)


def is_float(value):
    u"""是否浮点型"""
    pattern = re.compile("^(\-?\d+)(\.\d+)?$")
    return pattern.match(value)


def is_email(value):
    u"""是否邮件"""
    pattern = re.compile(
        "^([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+@([A-Z0-9]+[_|\_|\.]?)*[A-Z0-9]+\.[A-Z]{2,3}$",
        re.I)
    return pattern.match(value)


def _get_rule_value(rule):
    return rule.split("[")[1].split("]")[0]


def verify(options):
    u"""验证

    [validate.js](http://rickharrison.github.io/validate.js/)
    """
    for p in options:
        rule = p.get("rule")
        name = p.get("name")
        value = p.get("value")

        if rule == "required":
            if value == "":
                return "{}不能为空".format(name)

        if rule == "valid_email":
            if is_email(value) is None:
                return "{}格式错误".format(name)

        if rule.find("min_length") != -1:
            min_length = int(_get_rule_value(rule))
            if len(value) < min_length:
                return "{}长度不能小于{}".format(name, min_length)

        if rule.find("max_length") != -1:
            max_length = int(_get_rule_value(rule))
            if len(value) > max_length:
                return "{}长度不能大于{}".format(name, max_length)

        if rule.find("exact_length") != -1:
            exact_length = int(_get_rule_value(rule))
            if len(value) != exact_length:
                return "{}长度不是{}".format(name, exact_length)

        if rule.find("matches") != -1:
            matches_value = _get_rule_value(rule)
            if value != matches_value:
                return "{}不一致".format(name)

        if rule == "numeric":
            if is_float(value) is None:
                return "{}不是数值".format(name)

        if rule == "integer":
            if is_int(value) is None:
                return "{}不是整数".format(name)

        if rule.find("greater_than_or_equal") != -1:
            min_length = float(_get_rule_value(rule))
            if float(value) < min_length:
                return "{}不能小于{}".format(name, min_length)

        if rule.find("greater_than") != -1:
            min_length = float(_get_rule_value(rule))
            if float(value) <= min_length:
                return "{}不能小于等于{}".format(name, min_length)

        if rule.find("less_than_or_equal") != -1:
            max_length = float(_get_rule_value(rule))
            if float(value) > max_length:
                return "{}不能大于{}".format(name, max_length)

        if rule.find("less_than") != -1:
            max_length = float(_get_rule_value(rule))
            if float(value) >= max_length:
                return "{}不能大于等于{}".format(name, max_length)

    return None


def verify_page(page, row, extend=None):
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

    return verify(rules)
