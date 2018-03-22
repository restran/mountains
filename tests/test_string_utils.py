# -*- coding: utf-8 -*-
# Created by restran on 2018/3/22
from __future__ import unicode_literals, absolute_import

from mountains.utils import string_utils
import unittest
import random
import string


class UtilsTest(unittest.TestCase):
    def test_line_break(self):
        s = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(3000)])
        break_s = string_utils.line_break(s)
        self.assertEqual(s, break_s.replace('\n', ''))

        break_s = string_utils.line_break(s, 10)
        self.assertEqual(s, break_s.replace('\n', ''))

        break_s = string_utils.line_break(s, 100)
        self.assertEqual(s, break_s.replace('\n', ''))

        break_s = string_utils.line_break(s, 3001)
        self.assertEqual(s, break_s.replace('\n', ''))

    def test_fixed_length_split(self):
        s = 'aaaabbbbccccdddd'
        r = string_utils.fixed_length_split(s, 4)
        self.assertEqual(r, ['aaaa', 'bbbb', 'cccc', 'dddd'])
        r = string_utils.fixed_length_split(s, 6)
        self.assertEqual(r, ['aaaabb', 'bbcccc', 'dddd'])
        r = string_utils.fixed_length_split(s, 16)
        self.assertEqual(r, ['aaaabbbbccccdddd'])


if __name__ == '__main__':
    unittest.main()
