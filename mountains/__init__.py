# -*- coding: utf-8 -*-
# Created by restran on 2017/7/26
from __future__ import unicode_literals, absolute_import

from .base import PY2, PY3, PYPY, string_types, integer_types, \
    class_types, text_type, binary_type, long_type, BytesIO
from .encoding import force_text, force_bytes

__author__ = "restran <grestran@gmail.com>"
__version__ = "0.5.4"

__all__ = [
    '__author__', '__version__', 'PY2', 'PY3', 'PYPY',
    'string_types', 'integer_types', 'class_types', 'text_type',
    'binary_type', 'long_type', 'BytesIO', 'force_text', 'force_bytes'
]
