# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import uuid
from datetime import datetime
from decimal import Decimal
from .. import text_type, PY3, force_text

# https://github.com/esnme/ultrajson
# ujson 速度比较快，但是有些参数没有，与 simplejson 和 json 不完全兼容
# 而且 ujson 似乎已经不再维护了

try:
    import simplejson as json

    simplejson_imported = True
except ImportError:
    import json

    simplejson_imported = False


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


load = json.load
dump = json.dump


def loads(content, encoding='utf-8', **kwargs):
    if PY3:
        # python3.5，json loads 必须为str类型，如果为bytes类型会报错
        # python3.7，json loads 支持str类型和bytes类型
        content = force_text(content)
    return json.loads(s=content, encoding=encoding, **kwargs)


def dumps(dict_data, ensure_ascii=True, indent=None,
          sort_keys=False, encoding='utf-8', **kwargs):
    """
    返回json数据
    :param encoding:
    :param ensure_ascii:
    :param sort_keys:
    :param indent:
    :param dict_data:
    :return:
    """
    if simplejson_imported:
        return json.dumps(dict_data, default=json_default,
                          ensure_ascii=ensure_ascii, indent=indent,
                          sort_keys=sort_keys, encoding=encoding, **kwargs)
    else:
        return json.dumps(dict_data, default=json_default,
                          ensure_ascii=ensure_ascii, indent=indent,
                          sort_keys=sort_keys, **kwargs)
