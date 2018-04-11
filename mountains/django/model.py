# -*- coding: utf-8 -*-
# created by restran on 2018/01/22
from __future__ import unicode_literals, absolute_import

import logging
import traceback

try:
    from django.core.paginator import Paginator, EmptyPage
except ImportError:
    raise Exception('django is not installed')

from future.utils import iteritems

MAX_PAGE_SIZE = 100

DEFAULT_PAGE_SIZE = 20

logger = logging.getLogger(__name__)


def object_set_dict_data(model_class, dict_data):
    obj = model_class()
    for k, v in iteritems(dict_data):
        setattr(obj, k, v)

    return obj


def add_fields_2_json(obj, json_dict, fields):
    for t in fields:
        if hasattr(obj, t):
            json_dict[t] = getattr(obj, t)


def set_dict_none_default(dict_item, default_value):
    """
    对字典中为None的值，重新设置默认值
    :param dict_item:
    :param default_value:
    :return:
    """
    for (k, v) in iteritems(dict_item):
        if v is None:
            dict_item[k] = default_value


def auto_model_name_recognize(model_name):
    """
    自动将 site-user 识别成 SiteUser
    :param model_name:
    :return:
    """
    name_list = model_name.split('-')
    return ''.join(['%s%s' % (name[0].upper(), name[1:]) for name in name_list])


def model_get_entry(model_class, entry_id=None, filter_dict=None, select_related_fields=None):
    """
    """
    if filter_dict is None:
        filter_dict = {}

    if entry_id is not None:
        filter_dict['id'] = entry_id

    try:
        if select_related_fields is None:
            return model_class.objects.get(**filter_dict)
        else:
            fields = [t.attname for t in model_class._meta.fields]
            fields.extend(select_related_fields)
            obj = model_class.objects.values(*fields).get(**filter_dict)
            return object_set_dict_data(model_class, obj)
    except model_class.DoesNotExist:
        return None
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)
        return None


def model_delete_entry(model_class, entry_id):
    model_class.objects.filter(id=entry_id).delete()


def model_total_count(model_class, filter_dict=None, q_filter=None):
    if filter_dict is None:
        filter_dict = {}

    if q_filter is not None:
        filter_list = [q_filter]
    else:
        filter_list = []

    return model_class.objects.filter(
        *filter_list, **filter_dict).count()


def model_to_select_list(model_class, filter_dict=None, q_filter=None):
    """
    只选择 id 和 name，用来做列表选择
    :param model_class:
    :param filter_dict:
    :param q_filter:
    :return:
    """
    if filter_dict is None:
        filter_dict = {}

    if q_filter is not None:
        filter_list = [q_filter]
    else:
        filter_list = []

    objects = model_class.objects.filter(
        *filter_list, **filter_dict).values('id', 'name')

    return list(objects)


def model_to_list(model_class, filter_dict=None, order_by_list=None,
                  select_related_fields=None, q_filter=None,
                  values=None,
                  to_json_method='to_json'):
    """
    不分页
    :param values:
    :param to_json_method:
    :param model_class:
    :param filter_dict:
    :param order_by_list:
    :param select_related_fields:
    :param q_filter:
    :return:
    """
    return model_to_page_list(model_class, page_num=None,
                              filter_dict=filter_dict, order_by_list=order_by_list,
                              select_related_fields=select_related_fields,
                              q_filter=q_filter, values=values,
                              to_json_method=to_json_method)


def model_to_page_list(model_class, page_num,
                       page_size=DEFAULT_PAGE_SIZE,
                       filter_dict=None, order_by_list=None,
                       select_related_fields=None, q_filter=None,
                       values=None, to_json_method='to_json',
                       max_page_size=MAX_PAGE_SIZE):
    """
    :param max_page_size:
    :param model_class:
    :param page_num:
    :param page_size:
    :param filter_dict:
    :param order_by_list:
    :param select_related_fields:
    :param q_filter: Q(uuid__contains=keyword) | Q(memo__contains=keyword)
    :param values:
    :param to_json_method:
    :return:
    """
    if order_by_list is None:
        order_by_list = ['-id']

    if filter_dict is None:
        filter_dict = {}

    if q_filter is not None:
        filter_list = [q_filter]
    else:
        filter_list = []

    if select_related_fields is None:
        if values is None:
            objects = model_class.objects.filter(
                *filter_list, **filter_dict).order_by(*order_by_list)
        else:
            objects = model_class.objects.filter(
                *filter_list, **filter_dict).values(*values).order_by(*order_by_list)
    else:
        if values is None:
            fields = [t.attname for t in model_class._meta.fields]
        else:
            fields = values
        fields.extend(select_related_fields)
        objects = model_class.objects.filter(
            *filter_list, **filter_dict).values(*fields).order_by(*order_by_list)

    if page_num is not None:
        if page_size > max_page_size:
            page_size = max_page_size

        paginator = Paginator(objects, page_size)
        try:
            json_list = paginator.page(page_num)
        except EmptyPage as e:
            json_list = []
    else:
        json_list = list(objects)

    if select_related_fields is not None or values is not None:
        json_list = [object_set_dict_data(model_class, t) for t in json_list]
    return [getattr(t, to_json_method)() for t in json_list]
