# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

from mountains import logging
from mountains.logging import StreamHandler, FileHandler, RotatingFileHandler, TimedRotatingFileHandler
import unittest


class UtilsTest(unittest.TestCase):
    def test_1(self):
        logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                         FileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))
        logger = logging.getLogger(__name__)
        print('123')
        logger.debug('hello')

    def test_2(self):
        logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                         RotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))
        logger = logging.getLogger(__name__)

        logger.debug('hello')

    def test_3(self):
        logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE),
                         TimedRotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))
        logger = logging.getLogger(__name__)

        logger.debug('hello')


if __name__ == '__main__':
    unittest.main()
