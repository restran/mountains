# -*- coding: utf-8 -*-
# Created by restran on 2018/9/10
from __future__ import unicode_literals, absolute_import

import csv

__all__ = ['read_csv', 'read_csv_as_dict', 'write_csv', 'write_csv_from_dict']


def read_csv(filepath_or_buffer, encoding=None, delimiter=',', quotechar='"'):
    """
    读 CSV 文件
    :param encoding:
    :param filepath_or_buffer:
    :param delimiter:
    :param quotechar:
    :return:
    """

    if isinstance(filepath_or_buffer, str):
        with open(filepath_or_buffer, 'r', encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                yield row

    else:
        reader = csv.reader(filepath_or_buffer, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            yield row


def read_csv_as_dict(filepath_or_buffer, headers=None, encoding=None, delimiter=',', quotechar='"'):
    if isinstance(filepath_or_buffer, str):
        with open(filepath_or_buffer, 'r', encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=headers,
                                    delimiter=delimiter, quotechar=quotechar)
            for row in reader:
                yield dict(row)
    else:
        reader = csv.DictReader(filepath_or_buffer, fieldnames=headers,
                                delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            yield dict(row)


def write_csv(filepath_or_buffer=None, headers=None, data=None,
              encoding=None, delimiter=',', quotechar='"'):
    """
    写 CSV
    :param filepath_or_buffer:
    :param headers:
    :param data:
    :param encoding:
    :param delimiter:
    :param quotechar:
    :return:
    """
    if isinstance(filepath_or_buffer, str):
        with open(filepath_or_buffer, 'w', encoding=encoding) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            if headers is not None and isinstance(headers, list):
                writer.writerow(headers)

            writer.writerows(data)
    else:
        writer = csv.writer(filepath_or_buffer, delimiter=delimiter, quotechar=quotechar)
        if headers is not None and isinstance(headers, list):
            writer.writerow(headers)

        writer.writerows(data)


def write_csv_from_dict(filepath_or_buffer=None, headers=None, data=None,
                        write_header=True, encoding=None, delimiter=',',
                        quotechar='"'):
    """
    data 是 list 类型，每一项都是字典类型
    :param write_header:
    :param filepath_or_buffer:
    :param headers:
    :param data:
    :param encoding:
    :param delimiter:
    :param quotechar:
    :return:
    """
    if isinstance(filepath_or_buffer, str):
        with open(filepath_or_buffer, 'w', encoding=encoding) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=delimiter,
                                    quotechar=quotechar)
            if write_header:
                writer.writeheader()
            writer.writerows(data)
    else:
        writer = csv.DictWriter(filepath_or_buffer, fieldnames=headers, delimiter=delimiter,
                                quotechar=quotechar)
        if write_header:
            writer.writeheader()
        writer.writerows(data)
