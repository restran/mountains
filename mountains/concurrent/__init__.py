# -*- coding: utf-8 -*-
# Created by restran on 2017/8/23
from __future__ import unicode_literals, absolute_import

import time
from concurrent import futures

from future.moves.queue import Queue


class TaskExecutor(object):
    """
    使用线程的执行器，可以并发执行任务
    """

    def __init__(self, fn_task, task_params_list, max_workers=5):
        self.fn_task = fn_task
        self.max_workers = max_workers
        self.task_list = task_params_list
        self.task_queue = Queue()
        for t in task_params_list:
            self.task_queue.put(t)

    def get_next_tasks(self, max_num):
        output = []
        count = 0
        while not self.task_queue.empty() and count < max_num:
            t = self.task_queue.get()
            output.append(t)
            count += 1

        return output

    def run(self, *args, **kwargs):
        print('executor start')
        start_time = time.time()
        with futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            next_tasks = self.get_next_tasks(self.max_workers)
            shut_down = False
            while not shut_down and len(next_tasks) > 0:
                future_to_task = {
                    executor.submit(self.fn_task, task, *args, **kwargs): task
                    for task in next_tasks
                }

                # 这里 ThreadPoolExecutor 必须要等当前的所有任务都执行完成后，
                # 才能开始下一批的任务
                for future in futures.as_completed(future_to_task):
                    _ = future_to_task[future]
                    try:
                        shut_down = future.result()
                    except Exception as exc:
                        print(exc)
                        continue

                    if shut_down:
                        break

                next_tasks = self.get_next_tasks(self.max_workers)
        end_time = time.time()
        print('executor done, %.3fs' % (end_time - start_time))
