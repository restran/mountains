# -*- coding: utf-8 -*-
# created by restran on 2018/01/22
from __future__ import unicode_literals, absolute_import

import time
import unittest
from datetime import datetime
from mountains.datetime import converter


class DateTimeConverterTest(unittest.TestCase):
    def setUp(self):
        self.date_str = '2016-10-30 12:30:30'
        self.dt = datetime(year=2016, month=10, day=30, hour=12, minute=30, second=30)
        self.t = self.dt.timetuple()
        self.ts = int(time.mktime(self.t))
        self.ts_ms = int(time.mktime(self.t) * 1000)

    def test_str2datetime(self):
        dt = converter.str2datetime(self.date_str)
        self.assertEqual(dt, self.dt)

    def test_str2time(self):
        t = converter.str2time(self.date_str)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_str2timestamp(self):
        ts = converter.str2timestamp(self.date_str)
        self.assertEqual(ts, self.ts)
        ts = converter.str2timestamp(self.date_str, millisecond=True)
        self.assertEqual(ts, self.ts_ms)

    def test_datetime2str(self):
        s = converter.datetime2str(self.dt)
        self.assertEqual(s, self.date_str)

    def test_datetime2time(self):
        t = converter.datetime2time(self.dt)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_datetime2timestamp(self):
        ts = converter.datetime2timestamp(self.dt)
        self.assertEqual(ts, self.ts)
        ts = converter.datetime2timestamp(self.dt, millisecond=True)
        self.assertEqual(ts, self.ts_ms)

    def test_time2str(self):
        s = converter.time2str(self.t)
        self.assertEqual(s, self.date_str)

    def test_time2datetime(self):
        dt = converter.time2datetime(self.t)
        self.assertEqual(dt, self.dt)

    def test_time2timestamp(self):
        ts = converter.time2timestamp(self.t)
        self.assertEqual(ts, self.ts)
        ts = converter.time2timestamp(self.t, millisecond=True)
        self.assertEqual(ts, self.ts_ms)

    def test_timestamp2datetime(self):
        dt = converter.timestamp2datetime(self.ts)
        self.assertEqual(dt, self.dt)
        dt = converter.timestamp2datetime(self.ts_ms, millisecond=True)
        self.assertEqual(dt, self.dt)

    def test_timestamp2time(self):
        t = converter.timestamp2time(self.ts)
        self.assertEqual(t[0:6], self.t[0:6])
        t = converter.timestamp2time(self.ts_ms, millisecond=True)
        self.assertEqual(t[0:6], self.t[0:6])

    def test_timestamp2str(self):
        s = converter.timestamp2str(self.ts)
        self.assertEqual(s, self.date_str)
        s = converter.timestamp2str(self.ts_ms, millisecond=True)
        self.assertEqual(s, self.date_str)


if __name__ == '__main__':
    unittest.main()
