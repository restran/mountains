# -*- coding: utf-8 -*-
# created by restran on 2018/05/20
from __future__ import unicode_literals, absolute_import
import pypandoc

# converts markdown to reStructured
z = pypandoc.convert('README.md', 'rst', format='markdown')

# writes converted file
with open('README.rst', 'w') as outfile:
    outfile.write(z)
