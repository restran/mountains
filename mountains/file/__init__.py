# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import os
import shutil
from collections import deque

from .. import json
from ..datetime.converter import timestamp2datetime
from ..encoding import force_text, force_bytes


def read_dict(file_name, clear_none=False, encoding='utf-8'):
    """
    读取字典文件
    :param encoding:
    :param clear_none:
    :param file_name:
    :return:
    """
    with open(file_name, 'rb') as f:
        data = f.read()

    if encoding is not None:
        data = data.decode(encoding)

    line_list = data.splitlines()
    data = []
    i = 0
    for line in line_list:
        i += 1
        try:
            line = force_text(line).strip()
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


def read_file(file_name, encoding='utf-8'):
    """
    读文本文件
    :param encoding:
    :param file_name:
    :return:
    """
    with open(file_name, 'rb') as f:
        data = f.read()

    if encoding is not None:
        data = data.decode(encoding)

    return data


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


def get_file_size(file_path):
    """
    获取文件大小，返回的是字节
    :param file_path:
    :return:
    """
    return os.path.getsize(file_path)


def get_file_access_time(file_path):
    """
    获取文件访问时间，返回 datetime 类型
    :param file_path:
    :return:
    """
    return timestamp2datetime(os.path.getatime(file_path))


def get_file_create_time(file_path):
    """
    获取文件创建时间，返回 datetime 类型
    :param file_path:
    :return:
    """
    return timestamp2datetime(os.path.getctime(file_path))


def get_file_modify_time(file_path):
    """
    获取文件修改时间，返回 datetime 类型
    :param file_path:
    :return:
    """
    return timestamp2datetime(os.path.getmtime(file_path))


def copy_files(src_path, dst_path):
    """
    :param src_path:
    :param dst_path:
    :return:
    """
    abs_src_path = os.path.abspath(src_path)
    abs_dst_path = os.path.abspath(dst_path)
    # 遍历src_path目录下的所有文件
    for root, dirs, files in os.walk(src_path):
        try:
            for f in files:
                src_file_p = os.path.abspath(os.path.join(root, f))
                # 目标文件的完整路径
                dst_file_p = os.path.abspath(os.path.join(
                    abs_dst_path, src_file_p[len(abs_src_path) + 1:]))
                # 判断目标文件是否已存在，已存在则改名
                if os.path.exists(dst_file_p):
                    continue

                try:
                    # 判断目标文件所在的文件夹是否存在，不存在则递归创建文件夹
                    dst_p = os.path.dirname(dst_file_p)
                    if not os.path.exists(dst_p):
                        os.makedirs(dst_p)

                    # 移动文件
                    shutil.copy2(src_file_p, dst_file_p)
                except Exception as e:
                    print('move file error: {}'.format(e))

        except Exception as ex:
            print('error: {}'.format(ex))
