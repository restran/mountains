# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import os
import random

import requests

from ..base import __base_path
from ..file import read_dict
from ..encoding import force_bytes

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2983.0 Safari/537.36'

GLOBAL_USER_AGENTS = {}

USER_AGENT_DATA_PATH = os.path.join(__base_path, 'http/data/user_agents.txt')
MOBILE_USER_AGENT_DATA_PATH = os.path.join(__base_path, 'http/data/mobile_ua.txt')


def random_agent(agent_type='pc'):
    """
    随机获取一个 User-Agent
    :return:
    """
    agent_type = agent_type.lower().strip()
    if agent_type in ('wexin', 'wx'):
        agent_type = 'wechat'

    if agent_type in ('ios',):
        agent_type = 'iphone'

    global GLOBAL_USER_AGENTS
    if agent_type not in GLOBAL_USER_AGENTS:
        if agent_type == 'pc':
            GLOBAL_USER_AGENTS[agent_type] = read_dict(USER_AGENT_DATA_PATH)
        elif agent_type in ('mobile', 'wechat', 'android', 'iphone', 'alipay'):
            if 'mobile' not in GLOBAL_USER_AGENTS:
                GLOBAL_USER_AGENTS['mobile'] = list(read_dict(MOBILE_USER_AGENT_DATA_PATH))
            mobile_data = GLOBAL_USER_AGENTS['mobile']

            if agent_type == 'wechat':
                GLOBAL_USER_AGENTS[agent_type] = [t for t in mobile_data if 'MicroMessenger' in t]
            elif agent_type == 'alipay':
                GLOBAL_USER_AGENTS[agent_type] = [t for t in mobile_data if 'Alipay' in t]
            elif agent_type == 'android':
                GLOBAL_USER_AGENTS[agent_type] = [t for t in mobile_data if 'Android' in t]
            elif agent_type == 'iphone':
                GLOBAL_USER_AGENTS[agent_type] = [t for t in mobile_data if 'iPhone' in t]
            else:
                GLOBAL_USER_AGENTS[agent_type] = mobile_data
        else:
            return DEFAULT_USER_AGENT

    return random.choice(GLOBAL_USER_AGENTS[agent_type])


def random_wx_agent():
    """
    返回一个微信的UserAgent
    :return:
    """
    return random_agent('wechat')


def random_mobile_agent():
    """
    返回一个手机端的UserAgent
    :return:
    """
    return random_agent('mobile')


def request(method, url, headers=None, data=None, session=None):
    """
    :type session requests.session
    :param method:
    :param url:
    :param headers:
    :param data:
    :param session:
    :return:
    """
    base_headers = {
        'User-Agent': random_agent()
    }
    if headers is None:
        headers = {}

    base_headers.update(headers)

    if 'Content-Length' in headers:
        del base_headers['Content-Length']

    headers = base_headers
    if session is not None:
        req = session.request
    else:
        req = requests.request

    r = req(method, url, headers=headers, data=data)
    return r


def read_request(file_name, **params):
    """
    从文件中读取请求头，并根据格式化字符串模板，进行字符串格式化
    :param file_name:
    :param params:
    :return:
    """
    with open(file_name, 'r') as f:
        data = f.read()
        return read_request_from_str(data, **params)


def read_request_from_str(data, **params):
    """
    从字符串中读取请求头，并根据格式化字符串模板，进行字符串格式化
    :param data:
    :param params:
    :return:
    """
    method, uri = None, None
    headers = {}
    host = ''

    try:
        split_list = data.split('\n\n')
        headers_text = split_list[0]
        body = '\n\n'.join(split_list[1:])
    except:
        headers_text = data
        body = ''

    body = force_bytes(body)
    for k, v in params.items():
        body = body.replace(b'{%s}' % force_bytes(k), force_bytes(v))

    header_list = headers_text.split('\n')

    for i, line in enumerate(header_list):
        line = line.strip()
        if line.strip() == '':
            continue

        line = line.format(**params)
        if i == 0:
            # 至多3个
            split_line = line.strip().split(' ')
            method, uri, _ = split_line[0], ' '.join(split_line[1:-1]), split_line[-1]
        else:
            # 至多2个
            header, value = line.split(':', 1)
            header = header.strip()
            value = value.strip()
            headers[header] = value
            if header.lower() == 'host':
                host = value

    return headers, method, uri, host, body


def query_str_2_dict(query_str):
    """
    将查询字符串，转换成字典
    a=123&b=456
    {'a': '123', 'b': '456'}
    :param query_str:
    :return:
    """
    if query_str:
        query_list = query_str.split('&')
        query_dict = {}
        for t in query_list:
            # 避免在非法查询字符串的情况下报错
            # 例如未对url参数转义
            try:
                x = t.split('=')
                query_dict[x[0]] = x[1]
            except:
                pass
    else:
        query_dict = {}
    return query_dict


def raw_headers_to_dict(raw_headers):
    """
    通过原生请求头获取请求头字典
    :param raw_headers: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in raw_headers.split("\n") if ': ' in line)
