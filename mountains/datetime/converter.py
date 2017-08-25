# -*- coding: utf-8 -*-
# Created by restran on 2016/11/1
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import time

"""
date string, datetime, time and timestamp converter
"""


def str2datetime(date_str, format='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.strptime(date_str, format)
    except:
        return None


def str2time(date_str, format='%Y-%m-%d %H:%M:%S'):
    try:
        return time.strptime(date_str, format)
    except:
        return None


def str2timestamp(date_str, format='%Y-%m-%d %H:%M:%S'):
    try:
        return int(time.mktime(time.strptime(date_str, format)))
    except:
        return None


def datetime2str(dt, format='%Y-%m-%d %H:%M:%S'):
    try:
        return dt.strftime(format)
    except:
        return None


def datetime2time(dt):
    try:
        return dt.timetuple()
    except:
        return None


def datetime2timestamp(dt):
    try:
        return int(time.mktime(dt.timetuple()))
    except:
        return None


def time2str(time_tuple, format='%Y-%m-%d %H:%M:%S'):
    try:
        return time.strftime(format, time_tuple)
    except:
        return None


def time2datetime(time_tuple):
    try:
        return datetime(*time_tuple[0:6])
    except:
        return None


def time2timestamp(time_tuple):
    try:
        return int(time.mktime(time_tuple))
    except:
        return None


def timestamp2datetime(ts):
    try:
        return datetime.fromtimestamp(ts)
    except:
        return None


def timestamp2time(ts):
    try:
        return time.localtime(ts)
    except:
        return None


def timestamp2str(ts, format='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.fromtimestamp(ts).strftime(format)
    except:
        return None
