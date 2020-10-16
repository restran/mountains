# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import
import re
from ..base import text_type, string_types
import string
from base64 import b64decode, b32decode

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
        return value.decode(encoding)
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


def is_base64(s, is_printable=True):
    if len(s) % 4 != 0:
        return False

    b64rex = re.compile('^[A-Za-z0-9+/]+[=]{0,2}$', re.MULTILINE)
    if not b64rex.match(s):
        return False

    if is_printable:
        try:
            a = b64decode(s.encode()).decode()
            for c in a:
                if c not in string.printable:
                    return False
        except:
            return False
    return True


def is_base32(s, is_printable=True):
    if len(s) % 8 != 0:
        return False

    rex = re.compile('^[A-Z2-7]+[=]{0,7}$', re.MULTILINE)
    if not rex.match(s):
        return False

    if is_printable:
        try:
            a = b32decode(s.encode()).decode()
            for c in a:
                if c not in string.printable:
                    return False
        except:
            return False
    return True


def main():
    pass


if __name__ == '__main__':
    main()
