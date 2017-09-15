# -*- coding: utf-8 -*-
# Created by restran on 2017/9/15
from __future__ import unicode_literals, absolute_import

import time
from functools import wraps


# 装饰器的本质，是把函数作为参数传给装饰器函数
# 装饰器实际上是闭包
def log(func):
    """
    打印函数运行日志的装饰器
    :param func:
    :return:
    """

    # wraps 这个装饰器会将 func 的 doc 和 __name__ 复制过来
    # 否则在 wrapper 中调用 func.__name__ 输出的就是 wrapper
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('before call %s' % func.__name__)
        ret = func(*args, **kwargs)
        print('after call %s' % func.__name__)
        return ret

    return wrapper


def log_with_message(message):
    """
    打印函数运行日志的装饰器，可以再给装饰器传参数
    :param message:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('decorator log_with_message is running, %s' % message)
            ret = func(*args, **kwargs)
            return ret

        return wrapper

    return decorator


def time_elapsed(func):
    """
    记录函数运行耗时的生成器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = time.time() * 1000
        ret = func(*args, **kwargs)
        now_ts = time.time() * 1000
        elapsed = now_ts - timestamp
        print('%s costs time: %.2fms' % (func.__name__, elapsed))
        return ret

    return wrapper