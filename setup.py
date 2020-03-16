# -*- coding: utf-8 -*-
# Created by restran on 2017/7/27
from __future__ import unicode_literals

import sys

from future.utils import bytes_to_native_str
from setuptools import setup, find_packages

from mountains import __version__

kwargs = {
    'packages': find_packages(),
    # 还需要创建一个 MANIFEST.in 的文件，然后将这些数据也放在那里
    # package_data 添加了配置，Python2会报错
    'package_data': {}
}

install_requires = [
    'requests',
]

if sys.version_info < (3, 0):
    install_requires.append('futures')

kwargs['install_requires'] = install_requires
readme_file = 'README.md'
long_description = open(readme_file, 'rb').read()

setup(
    name='mountains',  # 文件名
    version=__version__,  # 版本(每次更新上传 pypi 需要修改)
    description="a util collection for python developing",
    long_description=bytes_to_native_str(long_description),  # 放README.md文件，方便在 pypi 页展示
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
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
