# -*- coding: utf-8 -*-
# Created by restran on 2017/11/7
from __future__ import unicode_literals, absolute_import


def fixed_length_split(s, width):
    """
    固定长度分割字符串
    :param s:
    :param width:
    :return:
    """
    # 使用正则的方法
    # import re
    # split = re.findall(r'.{%s}' % width, string)
    return [s[x: x + width] for x in range(0, len(s), width)]


def line_break(s, length=76):
    """
    将字符串分割成一行一行
    :param s:
    :param length:
    :return:
    """
    x = '\n'.join(s[pos:pos + length] for pos in range(0, len(s), length))
    return x


def is_empty(s):
    if s == '' or s is None or not isinstance(s, str):
        return True
    else:
        return False


def any_empty(*params):
    for s in params:
        if is_empty(s):
            return True
    else:
        return False
