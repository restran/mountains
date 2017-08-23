# -*- coding: utf-8 -*-
# Created by restran on 2016/11/1
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import time

"""
date string, datetime, time and timestamp converter
"""


def str2datetime(date_str, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(date_str, format)


def str2time(date_str, format='%Y-%m-%d %H:%M:%S'):
    return time.strptime(date_str, format)


def str2timestamp(date_str, format='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(time.strptime(date_str, format)))


def datetime2str(dt, format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(format)


def datetime2time(dt):
    return dt.timetuple()


def datetime2timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def time2str(time_tuple, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time_tuple)


def time2datetime(time_tuple):
    return datetime(*time_tuple[0:6])


def time2timestamp(time_tuple):
    return int(time.mktime(time_tuple))


def timestamp2datetime(ts):
    return datetime.fromtimestamp(ts)


def timestamp2time(ts):
    return time.localtime(ts)


def timestamp2str(ts, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(ts).strftime(format)
