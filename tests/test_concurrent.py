# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

from mountains.concurrent import TaskExecutor
import time
import random
import unittest


class DateTimeConverterTest(unittest.TestCase):

    def test_task_executor(self):
        def fn_task(item):
            print(item)
            time.sleep(random.choice(range(0, 10)) / 10.0)

        task_params_list = range(3)
        t = TaskExecutor(fn_task, task_params_list, max_workers=2)
        t.run()


if __name__ == '__main__':
    unittest.main()
