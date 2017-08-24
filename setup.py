# -*- coding: utf-8 -*-
# Created by restran on 2017/7/27

from setuptools import setup
import sys
from mountains import __version__

VERSION = __version__
kwargs = {}

install_requires = [
    'requests',
    'future',
    'simplejson',
    'colorlog',
]

if sys.version_info < (3, 0):
    install_requires.append('futures')

kwargs['install_requires'] = install_requires

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mountains',  # 文件名
    version=VERSION,  # 版本(每次更新上传 pypi 需要修改)
    description="a util collection for python developing",
    long_description=long_description,  # 放README.md文件，方便在 pypi 页展示
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],  # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
    keywords='python util',  # 关键字
    author='restran',  # 用户名
    author_email='grestran@gmail.com',  # 邮箱
    url='https://github.com/restran/mountains',  # github上的地址
    license='MIT',  # 遵循的协议
    packages=['mountains'],  # 发布的包名
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    **kwargs
)
