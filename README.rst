mountains
=========

|travis-ci| |Coverage Status| |pypi package|

A util collection for python developing.

install
-------

::

    pip install mountains
    pip3 install mountains

features
--------

1. Python 2-3 compatible for much of code
2. …

Upload to PyPi
--------------

安装最新的 setuptools

::

    pip3 install -U pip setuptools twine

生成 wheel 包

::

    python3 setup.py register bdist_wheel --universal upload

生成 tar.gz 包，因为 setup.py 用到了 pypandoc，安装的时候会需要依赖

::

    python3 setup.py register sdist upload

通过 setup install 安装后删除
-----------------------------

::

    python3 setup.py install --record files.txt
    cat files.txt | xargs rm -rf

.. |travis-ci| image:: https://travis-ci.org/restran/mountains.svg?branch=master
   :target: https://travis-ci.org/restran/mountains
.. |Coverage Status| image:: https://coveralls.io/repos/github/restran/mountains/badge.svg?branch=master
   :target: https://coveralls.io/github/restran/mountains?branch=master
.. |pypi package| image:: https://img.shields.io/pypi/v/mountains.svg
   :target: https://pypi.python.org/pypi/mountains/
