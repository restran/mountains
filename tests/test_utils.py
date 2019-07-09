# -*- coding: utf-8 -*-
# Created by restran on 2017/10/13
from __future__ import unicode_literals, absolute_import

import logging
import unittest

from mountains.utils import *

logger = logging.getLogger(__name__)


class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_any_none(self):
        self.assertEqual(any_none(1, 2, 3, None), True)
        self.assertEqual(any_none(1, 2, 3), False)

    def test_any_in(self):
        self.assertEqual(any_in('123abc123', 'a', 'b'), True)
        self.assertEqual(any_in('123ab123', 'a', 'c'), True)
        self.assertEqual(any_in('123', 'a', 'b', 'c'), False)


if __name__ == '__main__':
    unittest.main()
