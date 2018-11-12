# -*- coding: utf-8 -*-
# Created by restran on 2018/9/9
from __future__ import unicode_literals, absolute_import
import sys
from .terminal_size import get_terminal_size

TERMINAL_SIZE = get_terminal_size()


def terminal_pos(y, x):
    return '\x1b[%d;%dH' % (y, x)


def print_on_terminal_bottom(text):
    print('%s%s' % (terminal_pos(TERMINAL_SIZE[0], TERMINAL_SIZE[1]), text), end='')


def print_on_terminal_fix(text):
    sys.stdout.write("%s\r" % text)
    sys.stdout.flush()


class ColorConsole(object):
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"

    @classmethod
    def green(cls, message):
        return '%s%s%s' % (cls.GREEN, message, cls.END)

    @classmethod
    def blue(cls, message):
        return '%s%s%s' % (cls.BLUE, message, cls.END)

    @classmethod
    def red(cls, message):
        return '%s%s%s' % (cls.RED, message, cls.END)

    @classmethod
    def yellow(cls, message):
        return '%s%s%s' % (cls.YELLOW, message, cls.END)

    @classmethod
    def bold(cls, message):
        return '%s%s%s' % (cls.BOLD, message, cls.END)
