# -*- coding: utf-8 -*-
# Created by restran on 2017/9/15
from __future__ import unicode_literals, absolute_import, print_function
from .. import force_text, text_type, binary_type
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


def text_type_dict(dict_data):
    if not isinstance(dict_data, dict):
        raise TypeError

    new_dict = {}
    for k, v in dict_data.items():
        if isinstance(k, binary_type):
            k = k.decode('utf-8')
        if isinstance(v, binary_type):
            v = v.decode('utf-8')

        new_dict[k] = v

    return new_dict


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


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value


def main():
    print(any_none(1, 2, 3, None))


if __name__ == '__main__':
    main()
