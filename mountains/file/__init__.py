# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import
from collections import deque
from ..encoding import force_text, force_bytes
from .. import json


def read_dict(file_name, clear_none=False):
    """
    读取字典文件
    :param clear_none:
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as f:
        data = []
        i = 0
        for line in f:
            i += 1
            try:
                line = force_text(line).strip('\n').strip()
                data.append(line)
            except:
                print('read error line %s' % i)
        if clear_none:
            data = [t for t in data if t != '']
        data = deque(data)
    return data


def write_bytes_file(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(force_bytes(data))


def read_bytes_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()


def write_file(file_name, data):
    """
    写文本文件
    :param file_name:
    :param data:
    :return:
    """
    with open(file_name, 'w') as f:
        f.write(data)


def read_file(file_name):
    """
    读文本文件
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as f:
        return f.read()


def read_json(file_name):
    try:
        return json.loads(read_bytes_file(file_name))
    except:
        return None


def write_json(file_name, data, indent=None,
               ensure_ascii=True, sort_keys=False, **kwargs):
    with open(file_name, 'wb') as f:
        try:
            data = json.dumps(data, indent=indent,
                              ensure_ascii=ensure_ascii,
                              sort_keys=sort_keys, **kwargs)
            f.write(force_bytes(data))
            return True
        except:
            return False
