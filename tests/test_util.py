# -*- coding: utf-8 -*-
# Created by restran on 2017/10/13
from __future__ import unicode_literals, absolute_import

import logging
import unittest

from mountains.utils import *

logger = logging.getLogger(__name__)


class UtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_any_none(self):
        self.assertEqual(any_none(1, 2, 3, None), True)
        self.assertEqual(any_none(1, 2, 3), False)


if __name__ == '__main__':
    unittest.main()
