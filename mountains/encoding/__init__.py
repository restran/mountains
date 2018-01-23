# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

from ..base import text_type, string_types

_UTF8_TYPES = (bytes, type(None))

_TO_UNICODE_TYPES = (text_type, type(None))


def utf8(value, encoding=None):
    """Converts a string argument to a byte string.
    """
    if isinstance(value, _UTF8_TYPES):
        return value
    if not isinstance(value, text_type):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )

    if encoding is not None:
        return value.encode(encoding)

    try:
        return value.encode('utf-8')
    except:
        return value.encode('gbk')


def to_unicode(value, encoding=None):
    """Converts a string argument to a unicode string.
    """
    if isinstance(value, text_type):
        return value
    elif isinstance(value, type(None)):
        return text_type(value)

    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )

    if encoding is not None:
        return value.decode('utf-8')
    else:
        try:
            value = value.decode('utf-8')
        except:
            try:
                value = value.decode('gbk')
            except:
                pass

        return value


def force_text(s, encoding=None):
    """
    强制转成 Unicode
    """

    return to_unicode(s, encoding)


def force_bytes(s, encoding=None):
    """
    强制转成 bytes
    """

    return utf8(s, encoding)
