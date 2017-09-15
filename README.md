# mountains

A util collection for python developing.

## Upload to PyPi

生成 wheel 包

    python setup.py bdist_wheel --universal upload

生成 tar.gz 包，因为 setup.py 用到了 pypandoc，安装的时候会需要依赖

    python setup.py register sdist upload
