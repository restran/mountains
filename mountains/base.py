# -*- coding: utf-8 -*-
# Created by restran on 2017/8/29
from __future__ import unicode_literals, absolute_import

import os
import sys
import types

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = True if getattr(sys, 'pypy_version_info', None) else False

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes
    long_type = int
    from io import BytesIO
    from urllib.parse import urlencode, quote, \
        quote_plus, urlparse, urlunparse
    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    long_type = long
    from cStringIO import StringIO as BytesIO
    from urllib import urlencode, quote, quote_plus
    from urlparse import urlparse, urlunparse

# 当前项目所在路径
__base_path = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'PY2', 'PY3', 'PYPY', 'urlencode', 'quote', 'quote_plus',
    'urlparse', 'urlunparse',
    'string_types', 'integer_types', 'class_types', 'text_type',
    'binary_type', 'long_type', 'BytesIO', '__base_path'
]
