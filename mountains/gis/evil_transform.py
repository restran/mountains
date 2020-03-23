# -*- coding: utf-8 -*-
# created by restran on 2019/04/08
from __future__ import unicode_literals, absolute_import

"""
Original from https://github.com/googollee/eviltransform
地球坐标（WGS-84）
火星坐标（GCJ－2）
GCJ-02坐标用在谷歌地图，高德地图、腾讯地图等中国地图服务。
百度地图要在GCJ-02基础上再加转换
"""

import math

__all__ = ['wgs2gcj', 'gcj2wgs', 'gcj2wgs_exact',
           'distance', 'gcj2bd', 'bd2gcj', 'wgs2bd', 'bd2wgs']

earth_r = 6378137.0


def out_of_china(lat, lng):
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)


def transform(x, y):
    xy = x * y
    abs_x = math.sqrt(abs(x))
    x_pi = x * math.pi
    y_pi = y * math.pi
    d = 20.0 * math.sin(6.0 * x_pi) + 20.0 * math.sin(2.0 * x_pi)

    lat = d
    lng = d

    lat += 20.0 * math.sin(y_pi) + 40.0 * math.sin(y_pi / 3.0)
    lng += 20.0 * math.sin(x_pi) + 40.0 * math.sin(x_pi / 3.0)

    lat += 160.0 * math.sin(y_pi / 12.0) + 320 * math.sin(y_pi / 30.0)
    lng += 150.0 * math.sin(x_pi / 12.0) + 300.0 * math.sin(x_pi / 30.0)

    lat *= 2.0 / 3.0
    lng *= 2.0 / 3.0

    lat += -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * xy + 0.2 * abs_x
    lng += 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * xy + 0.1 * abs_x

    return lat, lng


def delta(lat, lng):
    ee = 0.00669342162296594323
    d_lat, d_lng = transform(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * math.pi
    magic = math.sin(rad_lat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((earth_r * (1 - ee)) / (magic * sqrt_magic) * math.pi)
    d_lng = (d_lng * 180.0) / (earth_r / sqrt_magic * math.cos(rad_lat) * math.pi)
    return d_lat, d_lng


def wgs2gcj(wgs_lat, wgs_lng):
    if out_of_china(wgs_lat, wgs_lng):
        return wgs_lat, wgs_lng
    else:
        d_lat, d_lng = delta(wgs_lat, wgs_lng)
        return wgs_lat + d_lat, wgs_lng + d_lng


def gcj2wgs(gcj_lat, gcj_lng):
    if out_of_china(gcj_lat, gcj_lng):
        return gcj_lat, gcj_lng
    else:
        d_lat, d_lng = delta(gcj_lat, gcj_lng)
        return gcj_lat - d_lat, gcj_lng - d_lng


def gcj2wgs_exact(gcj_lat, gcj_lng):
    init_delta = 0.01
    threshold = 0.000001
    d_lat = d_lng = init_delta
    m_lat = gcj_lat - d_lat
    m_lng = gcj_lng - d_lng
    p_lat = gcj_lat + d_lat
    p_lng = gcj_lng + d_lng
    for i in range(30):
        wgs_lat = (m_lat + p_lat) / 2
        wgs_lng = (m_lng + p_lng) / 2
        tmp_lat, tmp_lng = wgs2gcj(wgs_lat, wgs_lng)
        d_lat = tmp_lat - gcj_lat
        d_lng = tmp_lng - gcj_lng
        if abs(d_lat) < threshold and abs(d_lng) < threshold:
            return wgs_lat, wgs_lng
        if d_lat > 0:
            p_lat = wgs_lat
        else:
            m_lat = wgs_lat
        if d_lng > 0:
            p_lng = wgs_lng
        else:
            m_lng = wgs_lng
    return wgs_lat, wgs_lng


def distance(lat_a, lng_a, lat_b, lng_b):
    """
    计算两个经纬度之间的距离
    :param lat_a:
    :param lng_a:
    :param lat_b:
    :param lng_b:
    :return:
    """
    pi180 = math.pi / 180
    arc_lat_a = lat_a * pi180
    arc_lat_b = lat_b * pi180
    x = (math.cos(arc_lat_a) * math.cos(arc_lat_b) *
         math.cos((lng_a - lng_b) * pi180))
    y = math.sin(arc_lat_a) * math.sin(arc_lat_b)
    s = x + y
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    alpha = math.acos(s)
    d = alpha * earth_r
    return d


def gcj2bd(gcj_lat, gcj_lng):
    """
    GCJ－2转百度
    :param gcj_lat:
    :param gcj_lng:
    :return:
    """
    if out_of_china(gcj_lat, gcj_lng):
        return gcj_lat, gcj_lng

    x = gcj_lng
    y = gcj_lat
    z = math.hypot(x, y) + 0.00002 * math.sin(y * math.pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * math.pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lat, bd_lng


def bd2gcj(bd_lat, bd_lng):
    """
    百度转GCJ－2
    :param bd_lat:
    :param bd_lng:
    :return:
    """
    if out_of_china(bd_lat, bd_lng):
        return bd_lat, bd_lng

    x = bd_lng - 0.0065
    y = bd_lat - 0.006
    z = math.hypot(x, y) - 0.00002 * math.sin(y * math.pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
    gcj_lng = z * math.cos(theta)
    gcj_lat = z * math.sin(theta)
    return gcj_lat, gcj_lng


def wgs2bd(wgs_lat, wgs_lng):
    return gcj2bd(*wgs2gcj(wgs_lat, wgs_lng))


def bd2wgs(bd_lat, bd_lng):
    return gcj2wgs(*bd2gcj(bd_lat, bd_lng))
