# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import logging
import logging.config

FORMAT_VERBOSE = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
# Python的logging使用的是time的datefmt，并没有提供毫秒的datefmt
# http://blog.csdn.net/arthur503/article/details/49359241
DATE_FMT_VERBOSE = "%Y-%m-%d %H:%M:%S"

FORMAT_SIMPLE = '%(levelname)s %(message)s'
DATE_FMT_SIMPLE = "%H:%M:%S"

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'


def getLogger(name):
    """
    用于替代 logging.getLogger
    :param name:
    :return:
    """
    return logging.getLogger(name)


def Logger(name):
    """
    用于替代 logging.getLogger
    :param name:
    :return:
    """
    return logging.getLogger(name)


class BaseHandler(object):
    def __init__(self, level=DEBUG, format=None, datefmt=None):
        self.level = level
        self.format = format
        self.datefmt = datefmt

        if self.datefmt is None:
            self.datefmt = DATE_FMT_VERBOSE

        if self.format is None:
            self.format = FORMAT_VERBOSE

        self.handler_class = 'logging.handlers.StreamHandler'

    def get_formatter_name(self):
        return self.__class__.__name__

    def get_formatter(self):
        formatter = {
            self.get_formatter_name(): {
                'format': self.format,
                'datefmt': self.datefmt,
            }
        }

        return formatter

    def get_handler(self):
        handler = {
            self.get_formatter_name(): {
                'level': self.level,
                'class': self.handler_class,
                'formatter': self.get_formatter_name()
            }
        }

        return handler


class StreamHandler(BaseHandler):
    def __init__(self, level=DEBUG, format=None, datefmt=None):
        super(StreamHandler, self).__init__(level, format, datefmt)
        self.handler_class = 'logging.StreamHandler'


class ColorStreamHandler(BaseHandler):
    def __init__(self, level=DEBUG, format=None, datefmt=None):
        super(ColorStreamHandler, self).__init__(level, format, datefmt)
        self.format = '%(log_color)s' + self.format
        self.handler_class = 'colorlog.StreamHandler'

    def get_formatter(self):
        formatter = {
            self.get_formatter_name(): {
                '()': 'colorlog.ColoredFormatter',
                'format': self.format,
                'datefmt': self.datefmt,
                'log_colors': {
                    'DEBUG': 'white',
                    'INFO': 'white',
                    'WARNING': 'green',
                    'ERROR': 'yellow',
                    'CRITICAL': 'red',
                    # 'CRITICAL': 'red, bg_white',
                }
            }
        }

        return formatter


class FileHandler(BaseHandler):
    def __init__(self, filename='log.txt', level=DEBUG, format=None, datefmt=None):
        super(FileHandler, self).__init__(level, format, datefmt)
        self.filename = filename
        self.handler_class = 'logging.FileHandler'

    def get_handler(self):
        handler = super(FileHandler, self).get_handler()
        new_params = {
            'filename': self.filename
        }

        handler[self.get_formatter_name()].update(new_params)
        return handler


class RotatingFileHandler(BaseHandler):
    def __init__(self, filename='log.txt', max_bytes=1024 * 1024 * 10,
                 backup_count=10, delay=True, level=DEBUG,
                 format=None, datefmt=None):
        super(RotatingFileHandler, self).__init__(level, format, datefmt)
        self.filename = filename
        self.handler_class = 'logging.handlers.RotatingFileHandler'
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.delay = delay

    def get_handler(self):
        handler = super(RotatingFileHandler, self).get_handler()
        new_params = {
            'filename': self.filename,
            'delay': self.delay,
            'maxBytes': self.max_bytes,
            'backupCount': self.backup_count
        }

        handler[self.get_formatter_name()].update(new_params)
        return handler


class TimedRotatingFileHandler(BaseHandler):
    def __init__(self, filename='log.txt', when='D', interval=1,
                 backup_count=10, delay=True, level=DEBUG,
                 format=None, datefmt=None):
        """
        when 可以使用这些参数
        'S' Seconds
        'M' Minutes
        'H' Hours
        'D' Days
        'W0'-'W6' Weekday (0=Monday)
        'midnight' Roll over at midnight
        :param filename:
        :param when:
        :param interval:
        :param backup_count:
        :param delay:
        :param level:
        :param format:
        :param datefmt:
        """
        super(TimedRotatingFileHandler, self).__init__(level, format, datefmt)
        self.filename = filename
        self.handler_class = 'logging.handlers.TimedRotatingFileHandler'
        self.when = when
        self.interval = interval
        self.delay = delay
        self.backup_count = backup_count

    def get_handler(self):
        handler = super(TimedRotatingFileHandler, self).get_handler()
        new_params = {
            'filename': self.filename,
            'delay': self.delay,
            'when': self.when,
            'interval': self.interval,
            'backupCount': self.backup_count
        }

        handler[self.get_formatter_name()].update(new_params)
        return handler


def init_log(*handlers, **kwargs):
    """
    :param handlers:
    :return:
    """
    disable_existing_loggers = kwargs.get('disable_existing_loggers', False)

    handlers_config = [t.get_handler() for t in handlers]
    new_handlers_config = {}
    for t in handlers_config:
        new_handlers_config.update(t)

    formatter_config = [t.get_formatter() for t in handlers]
    new_formatter_config = {}
    for t in formatter_config:
        new_formatter_config.update(t)

    handler_name_list = [t.get_formatter_name() for t in handlers]
    dict_config = {
        'version': 1,
        'disable_existing_loggers': disable_existing_loggers,
        'formatters': new_formatter_config,
        'handlers': new_handlers_config,
        'loggers': {
            '': {
                'handlers': handler_name_list,
                'level': 'DEBUG',
            }
        }
    }

    logging.config.dictConfig(dict_config)
