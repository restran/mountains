# -*- coding: utf-8 -*-
# Created by restran on 2017/10/13
from __future__ import unicode_literals, absolute_import

import logging

from .. import json

try:
    from django.http import HttpResponse
except:
    class HttpResponse(object):
        def __init__(*args, **kwargs):
            raise Exception('django is not installed')

logger = logging.getLogger(__name__)


def http_response_json(dict_data):
    """
    返回json数据
    :param dict_data:
    :return:
    """

    return HttpResponse(json.dumps(dict_data),
                        content_type="application/json; charset=utf-8")


class APIStatusCode(object):
    SUCCESS = 200  # 成功
    FAIL = 400  # 客户端的错误, 例如请求信息不正确
    ERROR = 500  # 服务端的错误, 例如出现异常
    LOGIN_REQUIRED = 401  # 需要登录才能访问


class APIHandler(object):
    @classmethod
    def return_json(cls, code, data, msg):
        try:
            return http_response_json({
                'code': code, 'data': data, 'msg': msg})
        except Exception as e:
            logger.error(e)
            return http_response_json({
                'code': APIStatusCode.ERROR, 'data': None,
                'msg': msg})

    @classmethod
    def success(cls, data=None, msg='', code=APIStatusCode.SUCCESS):
        return cls.return_json(code, data, msg)

    @classmethod
    def fail(cls, data=None, msg='', code=APIStatusCode.FAIL):
        return cls.return_json(code, data, msg)

    @classmethod
    def login_required(cls, data=None, msg='', code=APIStatusCode.LOGIN_REQUIRED):
        return cls.return_json(code, data, msg)

    @classmethod
    def error(cls, data=None, msg='', code=APIStatusCode.ERROR):
        return cls.return_json(code, data, msg)
