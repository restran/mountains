# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

from mountains.concurrent import TaskExecutor
import time
import random


def test_task_executor():
    def fn_task(item):
        print(item)
        time.sleep(random.choice(range(1, 5)))

    task_params_list = range(10)
    t = TaskExecutor(fn_task, task_params_list, max_workers=2)
    t.run()


if __name__ == '__main__':
    test_task_executor()
