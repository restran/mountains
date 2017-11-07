# -*- coding: utf-8 -*-
# Created by restran on 2017/11/7
from __future__ import unicode_literals, absolute_import
from mountains.encoding import force_bytes
from mountains import PY2


def fixed_length_split(string, width):
    """
    固定长度分割字符串
    :param string:
    :param width:
    :return:
    """
    # 使用正则的方法
    # import re
    # split = re.findall(r'.{%s}' % width, string)
    return [string[x: x + width] for x in range(0, len(string), width)]


def bytes_2_printable_strings(data):
    data = force_bytes(data)
    result = []

    for c in data:
        if PY2:
            c = ord(c)
        if 32 <= c <= 126 or c in (10, 13):
            result.append(chr(c))

    return ''.join(result)


def main():
    data = open('D:/test.jpg', 'rb').read()
    r = bytes_2_printable_strings(data)
    print(r)


if __name__ == '__main__':
    main()
