# -*- coding: utf-8 -*-
# Created by restran on 2018/11/13
from __future__ import unicode_literals, absolute_import

import unittest

from mountains.http import random_agent, random_mobile_agent, random_wx_agent


class HTTPTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_random_agent(self):
        random_agent()
        random_agent('pc')
        random_agent('wexin')
        random_agent('mobile')
        random_wx_agent()
        random_mobile_agent()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
