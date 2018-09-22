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
