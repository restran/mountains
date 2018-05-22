# -*- coding: utf-8 -*-
# Created by restran on 2017/12/11
from __future__ import unicode_literals, absolute_import

import logging
import platform
import time
from collections import deque

from future.moves.urllib.parse import urlunparse, urlparse, urlencode
from mountains import json as json_util
from .. import force_text
from ..http import random_agent

try:
    from tornado.gen import coroutine, is_future, Return
    from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
except ImportError:
    raise Exception('tornado is not installed')

logger = logging.getLogger(__name__)

DEFAULT_CONNECT_TIMEOUT = 20
DEFAULT_REQUEST_TIMEOUT = 20
ASYNC_HTTP_MAX_CLIENTS = 100

# pycurl 在 Windows Python 64 位环境下会崩溃
# https://github.com/pycurl/pycurl/issues/395
# libcurl 7.48.0 以后的版本修复了这个bug
if platform.architecture()[0] == '64bit' and platform.system() == 'Windows':
    AsyncHTTPClient.configure(
        'tornado.simple_httpclient.SimpleAsyncHTTPClient')
else:
    try:
        # curl_httpclient is faster than simple_httpclient
        AsyncHTTPClient.configure(
            'tornado.curl_httpclient.CurlAsyncHTTPClient',
            max_clients=ASYNC_HTTP_MAX_CLIENTS)
    except ImportError:
        AsyncHTTPClient.configure(
            'tornado.simple_httpclient.SimpleAsyncHTTPClient')


class AsyncHTTPExecutor(object):
    """
    异步HTTP请求，可以并发访问
    """

    def __init__(self, task_queue, on_request,
                 on_success, on_error, on_queue_empty=None,
                 proxy_list=None,
                 max_workers=20, timeout=5, verbose=False):
        self.fn_on_queue_empty = on_queue_empty
        self.fn_on_request = on_request
        self.fn_on_success = on_success
        self.fn_on_error = on_error
        self.task_queue = deque()
        self.task_queue.extend(task_queue)
        self.timeout = timeout
        self.max_workers = max_workers
        self.count = 0
        self.verbose = verbose
        self.start_time = None
        self.last_time = None
        self.proxy_list = proxy_list
        self.proxy_index = 0

    def get_proxy(self):
        """
        获取下一个可用的代理
        :return: proxy_host, proxy_port, proxy_username, proxy_password
        """
        if self.proxy_list is None or len(self.proxy_list) <= 0:
            return None, None, None, None
        self.proxy_index += 1
        self.proxy_index = self.proxy_index % len(self.proxy_list)
        item = self.proxy_list[self.proxy_index]
        if len(item) == 2:
            return item[0], item[1], None, None
        else:
            return item[0], item[1], item[2], item[3]

    def get_next_task(self):
        try:
            item = self.task_queue.popleft()
        except IndexError:
            if self.fn_on_queue_empty is None:
                return None
            else:
                item = self.fn_on_queue_empty(self.task_queue)
                if isinstance(item, list) and len(item) > 0:
                    self.task_queue.extend(item)
                    item = self.task_queue.popleft()
        return item

    @coroutine
    def do_request(self, item):
        self.count += 1
        current_time = time.time()
        # 每隔10秒输出一次
        if current_time - self.last_time > 10:
            self.last_time = current_time
            speed = self.count / (current_time - self.start_time)
            past_time = current_time - self.start_time
            logger.info('items, speed, time: %s, %.1f/s, %.1fs' % (self.count, speed, past_time))

        base_headers = {
            'User-Agent': random_agent()
        }

        url, method, headers, body, extra_params = self.fn_on_request(item)
        if url is None:
            return

        if headers is None:
            headers = {}

        base_headers.update(headers)
        headers = base_headers

        url = force_text(url)
        body = '' if method == 'POST' else None
        proxy_host, proxy_port, proxy_username, proxy_password = self.get_proxy()
        if proxy_port is not None:
            proxy_port = int(proxy_port)

        params_dict = {
            'decompress_response': True,
            'validate_cert': False,
            'proxy_host': proxy_host,
            'proxy_port': proxy_port,
            'proxy_username': proxy_username,
            'proxy_password': proxy_password,
            'connect_timeout': self.timeout,
            'request_timeout': self.timeout,
            'follow_redirects': False
        }
        # 允许再传其他参数
        if isinstance(extra_params, dict):
            params_dict.update(extra_params)

        try:
            response = yield AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method=method,
                            headers=headers,
                            body=body,
                            **params_dict))
            try:
                self.fn_on_success(url, item, method, response, self.task_queue)
            except Exception as e:
                logger.error(e)
        except HTTPError as e:
            if hasattr(e, 'response') and e.response:
                try:
                    self.fn_on_success(url, item, method, e.response, self.task_queue)
                except Exception as ex:
                    logger.error(ex)
            else:
                if self.verbose:
                    logger.error(e)
                    logger.error('%s, %s' % (method, item))
                try:
                    self.fn_on_error(url, item, method, e, self.task_queue)
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            if self.verbose:
                logger.error(e)
                logger.error('%s, %s' % (method, item))

            try:
                self.fn_on_error(url, item, method, e, self.task_queue)
            except Exception as e:
                logger.error(e)

    @coroutine
    def fetch_url(self, i):
        item = self.get_next_task()
        while item is not None:
            yield self.do_request(item)
            item = self.get_next_task()

    @coroutine
    def run(self, *args, **kwargs):
        logger.info('executor start')
        self.start_time = time.time()
        self.last_time = self.start_time
        # Start workers, then wait for the work queue to be empty.
        # 会卡在这里，等待所有的 worker 都结束
        yield [self.fetch_url(t) for t in range(self.max_workers)]
        end_time = time.time()
        logger.info('total count: %s' % self.count)
        cost_time = end_time - self.start_time
        if cost_time > 0:
            speed = self.count / cost_time
        else:
            speed = 1

        logger.info('executor done, %.3f, %.1f/s' % (cost_time, speed))


@coroutine
def async_request(method='GET', url=None, params=None,
                  headers=None, data=None, json=None,
                  on_response=None, on_error=None,
                  connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                  request_timeout=DEFAULT_REQUEST_TIMEOUT,
                  follow_redirects=False,
                  proxy_host=None, proxy_port=None,
                  proxy_username=None, proxy_password=None):
    try:
        if url is None:
            return

        method = method.upper()

        base_headers = {
            'User-Agent': random_agent(),
        }

        if params is not None:
            url_parsed = urlparse(url)
            query = urlencode(params, doseq=True)
            if url_parsed.query != '':
                query = '%s&%s' % (query, url_parsed.query)

            url = urlunparse((url_parsed.scheme, url_parsed.netloc,
                              url_parsed.path, url_parsed.params,
                              query, url_parsed.fragment))

        if method == 'GET':
            body = None
        else:
            if json is not None:
                body = json_util.dumps(json)
                base_headers['Content-Type'] = 'application/json;charset=utf-8'
            elif isinstance(data, dict):
                body = urlencode(data, doseq=True)
                base_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            elif isinstance(data, list):
                body = force_text(data)
            else:
                body = data

        if isinstance(headers, dict):
            base_headers.update(headers)

        headers = base_headers
        response = yield AsyncHTTPClient().fetch(
            HTTPRequest(url=url,
                        headers=headers,
                        method=method,
                        body=body,
                        validate_cert=False,
                        decompress_response=True,
                        connect_timeout=connect_timeout,
                        request_timeout=request_timeout,
                        follow_redirects=follow_redirects,
                        proxy_host=proxy_host,
                        proxy_port=proxy_port,
                        proxy_username=proxy_username,
                        proxy_password=proxy_password))

        if on_response is not None:
            ret = on_response(response)
            if is_future(ret):
                yield ret

        raise Return(response)
    except Return as e:
        # 上面有抛出 Return 的异常，这里捕获到以后，要重新抛出
        # 否则返回的实际上就不是 response
        raise e
    except HTTPError as e:
        if hasattr(e, 'response') and e.response:
            if on_response is not None:
                ret = on_response(e.response)
                if is_future(ret):
                    yield ret

            raise Return(e.response)
        else:
            if on_error is not None:
                ret = on_error(e)
                if is_future(ret):
                    yield ret
            raise Return(None)
    except Exception as e:
        if on_error is not None:
            ret = on_error(e)
            if is_future(ret):
                yield ret

        raise Return(None)
