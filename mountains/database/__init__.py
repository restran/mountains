# -*- coding: utf-8 -*-
# created by restran on 2019/07/12
from __future__ import unicode_literals, absolute_import
import math

try:
    import records
except Exception as e:
    raise Exception('records is not installed')


def batch_insert(db, sql, data, batch_size):
    """
    :type db: records.Database
    :param db:
    :param sql:
    :param data:
    :param batch_size:
    :return:
    """

    total = len(data)
    if total <= 0:
        return

    times = math.ceil(total * 1.0 / batch_size)
    for i in range(times):
        data_list = data[i * batch_size:(i + 1) * batch_size]
        if len(data_list) > 0:
            db.bulk_query(sql, data_list)


def auto_batch_insert(db, sql, data, batch_size=500, force=False):
    """
    可以边添加数据，边自动批量插入数据
    :type db: records.Database
    :param db:
    :param sql:
    :param data:
    :param batch_size:
    :param force:
    :return:
    """
    total = len(data)
    if total <= 0:
        return data

    if total >= batch_size or force:
        if len(data) > 0:
            db.bulk_query(sql, data)
        data = []

    return data
