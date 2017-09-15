# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import uuid
from datetime import datetime
from decimal import Decimal

from mountains.base import PY3, text_type
from mountains.encoding import force_bytes

try:
    import simplejson as json
except ImportError:
    import json


def json_default(obj):
    """
    对一些数据类型的 json 序列化，
    默认情况下 json 没有对 datetime 和 Decimal 进行序列化
    如果不指定的话，会抛异常
    :param obj:
    :return:
    """
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, uuid.UUID):
        return text_type(obj)
    else:
        try:
            return text_type(obj)
        except:
            pass

    raise TypeError("%r is not JSON serializable" % obj)


def loads(content, encoding=None):
    if PY3:
        return json.loads(s=force_bytes(content), encoding=encoding)
    else:
        return json.loads(s=content, encoding=encoding)


def dumps(dict_data, ensure_ascii=True, indent=None,
          sort_keys=False):
    """
    返回json数据
    :param ensure_ascii:
    :param sort_keys:
    :param indent:
    :param dict_data:
    :return:
    """

    return json.dumps(dict_data, default=json_default,
                      ensure_ascii=ensure_ascii, indent=indent,
                      sort_keys=sort_keys)
