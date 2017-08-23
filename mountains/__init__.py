# -*- coding: utf-8 -*-
# Created by restran on 2017/7/26
from __future__ import unicode_literals, absolute_import
import sys
import os

__author__ = "restran <grestran@gmail.com>"
__version__ = "0.2.0"

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = True if getattr(sys, 'pypy_version_info', None) else False

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

# 当前项目所在路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
