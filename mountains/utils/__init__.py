# -*- coding: utf-8 -*-
# Created by restran on 2017/9/15
from __future__ import unicode_literals, absolute_import, print_function
from mountains import force_text, text_type
import itertools


def grouper(iterable, size):
    """
    >>> a = grouper([1,2,3,4,5,6,7],2)
    >>> list(a)
    [(1, 2), (3, 4), (5, 6), (7,)]
    :param iterable:
    :param size:
    :return:
    """
    # http://stackoverflow.com/a/8991553
    it = iter(iterable)
    if size <= 0:
        yield it
        return
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def any_none(*params):
    return any(map(lambda x: x is None, params))


class PrintCollector(object):
    def __init__(self):
        self.collector = []

    def print(self, output):
        self.collector.append(output)
        print(text_type(output))

    def all_output(self):
        return '\n'.join([force_text(t) for t in self.collector])

    def smart_output(self, result=None, verbose=True):
        if verbose:
            return self.all_output()

        if result is None:
            result = self.collector

        return result


def main():
    print(any_none(1, 2, 3, None))


if __name__ == '__main__':
    main()
