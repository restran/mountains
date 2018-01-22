# -*- coding: utf-8 -*-
# created by restran on 2018/01/22
from __future__ import unicode_literals, absolute_import
from mountains import json
import unittest
import uuid
from datetime import datetime


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_json_loads(self):
        a = json.loads('{"a": 123, "b": "456", "c": "中文"}')
        self.assertEqual(a['a'], 123)
        self.assertEqual(a['b'], '456')
        self.assertEqual(a['c'], '中文')

    def test_json_dumps(self):
        data = {
            'a': uuid.uuid4(),
            'b': datetime(year=2016, month=10, day=30, hour=12, minute=30, second=30)
        }
        a = json.dumps(data)
        a = json.loads(a)
        self.assertEqual(a['b'], '2016-10-30 12:30:30')


if __name__ == '__main__':
    unittest.main()
