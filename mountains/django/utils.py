# -*- coding: utf-8 -*-
# created by restran on 2018/04/06
from __future__ import unicode_literals, absolute_import


def get_client_ip(request):
    """
    获取客户端的IP
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        ip = x_real_ip
    elif x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
