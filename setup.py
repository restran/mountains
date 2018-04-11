# -*- coding: utf-8 -*-
# Created by restran on 2017/7/27
from __future__ import unicode_literals
import sys

import pypandoc
from setuptools import setup, find_packages

from mountains import __version__

kwargs = {
    'packages': find_packages(),
    # 还需要创建一个 MANIFEST.in 的文件，然后将这些数据也放在那里
    'package_data': {
        'mountains.http': [
            'data/user-agents.txt'
        ],
    }
}

install_requires = [
    'requests',
    'future',
    'simplejson',
    'colorlog',
    'pypandoc'
]

if sys.version_info < (3, 0):
    install_requires.append('futures')

kwargs['install_requires'] = install_requires

# converts markdown to reStructured
z = pypandoc.convert('README.md', 'rst', format='markdown')

# writes converted file
with open('README.rst', 'w') as outfile:
    outfile.write(z)

long_description = z

setup(
    name='mountains',  # 文件名
    version=__version__,  # 版本(每次更新上传 pypi 需要修改)
    description="a util collection for python developing",
    long_description=long_description,  # 放README.md文件，方便在 pypi 页展示
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],  # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
    keywords='python utils',  # 关键字
    author='restran',  # 用户名
    author_email='grestran@gmail.com',  # 邮箱
    url='https://github.com/restran/mountains',  # github上的地址
    license='MIT',  # 遵循的协议
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    **kwargs
)
