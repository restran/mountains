# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

from mountains import logging
from mountains.logging import StreamHandler, FileHandler, RotatingFileHandler, TimedRotatingFileHandler


def test1():
    logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                     FileHandler(format=logging.FORMAT_VERBOSE, level=logging.INFO))
    logger = logging.getLogger(__name__)

    logger.debug('hello')


def test2():
    logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                     RotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.INFO))
    logger = logging.getLogger(__name__)

    logger.debug('hello')


def test3():
    logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                     TimedRotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.INFO))
    logger = logging.getLogger(__name__)

    logger.debug('hello')


test3()
