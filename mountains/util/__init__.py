# -*- coding: utf-8 -*-
# Created by restran on 2017/9/15
from __future__ import unicode_literals, absolute_import

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


def any_none(params):
    return any(map(lambda x: x is None, params))


def main():
    print(any_none([1, 2, 3, 3]))


if __name__ == '__main__':
    main()
