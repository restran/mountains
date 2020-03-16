# -*- coding: utf-8 -*-
# Created by restran on 2018/11/13
from __future__ import unicode_literals, absolute_import
from mountains import file
import unittest
import uuid
from datetime import datetime


class Test(unittest.TestCase):
    def setUp(self):
        pass

    # def test_json_loads(self):
    #     file.read_json('data/test.json')

    def test_json_dumps(self):
        pass

    # def test_file_size(self):
    #     size = file.get_file_size('data/test.txt')
    #     self.assertEqual(size, 57)


if __name__ == '__main__':
    unittest.main()
