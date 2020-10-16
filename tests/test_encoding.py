# -*- coding: utf-8 -*-
# Created by restran on 2018/3/7
from __future__ import unicode_literals, absolute_import

import unittest

from mountains.encoding import converter, is_base64, is_base32


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_hex2dec(self):
        s = '1F'
        r = converter.hex2dec(s)
        self.assertEqual(r, 31)
        s = '1F1F'
        r = converter.hex2dec(s)
        self.assertEqual(r, 7967)

    def test_dec2hex(self):
        s = '31'
        r = converter.dec2hex(s)
        self.assertEqual(r.upper(), '1F')
        s = '7967'
        r = converter.dec2hex(s)
        self.assertEqual(r.upper(), '1F1F')

    def test_bin2dec(self):
        s = '11111'
        r = converter.bin2dec(s)
        self.assertEqual(r, 31)

    def test_dec2bin(self):
        s = '31'
        r = converter.dec2bin(s)
        self.assertEqual(r, '11111')

    def test_str2dec(self):
        s = 'abcdef'
        r = converter.str2dec(s)
        self.assertEqual(r, 107075202213222)

    def test_dec2str(self):
        s = '107075202213222'
        r = converter.dec2str(s)
        self.assertEqual(r, 'abcdef')

    def test_str2hex(self):
        s = 'abcdef'
        r = converter.str2hex(s)
        self.assertEqual(r, '616263646566')

    def test_hex2str(self):
        s = '616263646566'
        r = converter.hex2str(s)
        self.assertEqual(r, 'abcdef')

    def test_hex2bin(self):
        s = '616263646566'
        r = converter.hex2bin(s)
        self.assertEqual(r, '011000010110001001100011011001000110010101100110')

    def test_bin2hex(self):
        s = '011000010110001001100011011001000110010101100110'
        r = converter.bin2hex(s)
        self.assertEqual(r, '616263646566')

    def test_to_digital(self):
        for i in range(10, 1000):
            for j in range(2, 10):
                r = converter.to_digital(i, j)
                x = converter.from_digital(r, j)
                self.assertEqual(str(i), x)

    def test_is_base64(self):
        data = [
            ("Y2QgL2QgIkM6L2luZXRwdWIvd3d3cm9vdCImd2hvYW1pJmVjaG8gW1NdJmNkJmVjaG8gW0Vd", True),
            ("Qzov", True),
            ("123", False),
            ("Y21k", True),
            ("0000", False),
            ("QzovaW5ldHB1Yi93d3dyb290Lw==", True),
            ("QzovaW5ldHB1Yi8=", True),
            ("aHR0cDovLzExOC4zMS42Ni4yMy8yMDIwc2tpbGwvYS5leGU=", True)
        ]

        for (s, real_r) in data:
            r = is_base64(s)
            self.assertEqual(r, real_r)

    def test_is_base32(self):
        data = [
            ("GFQWCYLB", True),
            ("1", False),
            ("123", False),
            ("GE======", True),
            ("0000", False),
            ("GFQXGZDGMFZWIZTBONSGMYLTMRTGC43EMY======", True)
        ]

        for (s, real_r) in data:
            r = is_base32(s)
            self.assertEqual(r, real_r)


if __name__ == '__main__':
    unittest.main()
