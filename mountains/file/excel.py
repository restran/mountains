# -*- coding: utf-8 -*-
# created by restran on 2018/04/16
from __future__ import unicode_literals, absolute_import
from ..base import BytesIO
from ..file import write_bytes_file

try:
    import xlrd
except:
    raise Exception('xlrd is not installed')

try:
    import xlsxwriter
except:
    raise Exception('xlsxwriter is not installed')


def read_excel(file_name, offset=1):
    """
    读取 Excel
    :param file_name:
    :param offset: 偏移，一般第一行是表头，不需要读取数据
    :return:
    """
    try:
        workbook = xlrd.open_workbook(file_name)
    except Exception as e:
        return None

    if len(workbook.sheets()) <= 0:
        return []

    sh = workbook.sheets()[0]

    raw_data = []
    n_rows = sh.nrows
    row = sh.row_values(0)
    header = []
    for t in row:
        t = t.strip().lower()
        header.append(t)

    # n_cols = sh.ncols
    # 第0行是提示信息和标题，跳过
    for i in range(offset, n_rows):
        try:
            row = sh.row_values(i)
            d = {}
            for j, t in enumerate(header):
                d[t] = row[j]
            raw_data.append(d)
        except Exception as e:
            pass

    return raw_data


def write_excel(headers, data, file_name):
    sio = BytesIO()
    workbook = xlsxwriter.Workbook(sio)
    worksheet = workbook.add_worksheet()

    for i, t in enumerate(headers):
        worksheet.write(0, i, t['name'])

    index = 1
    for row in data:
        for i, x in enumerate(row):
            worksheet.write(index, i, x)
        index += 1
    # 关闭 Excel
    workbook.close()
    return write_bytes_file(sio.getvalue(), file_name)
