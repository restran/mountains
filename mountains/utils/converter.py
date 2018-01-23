# -*- coding: utf-8 -*-
# created by restran on 2018/01/22
from __future__ import unicode_literals, absolute_import


def str2int(number_str, default_value=None):
    if number_str is None or number_str == '':
        return default_value
    try:
        return int(number_str)
    except Exception as e:
        return default_value
