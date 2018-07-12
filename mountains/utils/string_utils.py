# -*- coding: utf-8 -*-
# Created by restran on 2017/11/7
from __future__ import unicode_literals, absolute_import
from ..encoding import force_bytes


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


def bytes_2_printable_strings(data):
    data = force_bytes(data)
    result = ['', '']
    for c in data:
        if PY2:
            c = ord(c)

        if 32 <= c <= 126 or c in (9, 10, 13):
            if c == 9:
                c = 32
            elif c == 13:
                c = 10

            # 去掉连续的空格
            if c == 32 and result[-1] == ' ':
                continue
            # 去掉连续的换行
            elif c == 10 and result[-1] == '\n':
                continue

            result.append(chr(c))

    return ''.join(result)