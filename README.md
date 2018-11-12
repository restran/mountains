# mountains

[![travis-ci](https://travis-ci.org/restran/mountains.svg?branch=master)](https://travis-ci.org/restran/mountains) [![Coverage Status](https://coveralls.io/repos/github/restran/mountains/badge.svg?branch=master)](https://coveralls.io/github/restran/mountains?branch=master) [![pypi package](https://img.shields.io/pypi/v/mountains.svg)](https://pypi.python.org/pypi/mountains/)

在开发Python的过程中经常会有一些常用的方法和工具类，因此将这些代码集成在一起，在开发新东西的时候就能直接调用，加速开发。

![icon](docs/icon.png)

## 安装

Python 2

    pip install mountains

Python3

    pip3 install mountains

## 功能

1. Python 2-3 兼容，大部分代码都尽可能做了兼容
2. 日期转换，各种日期、字符串、时间戳直接的转换



### 日期转换

datetime、time、时间戳、日期字符串之间的转换

```python

import time
from datetime import datetime
from mountains.datetime import converter

date_str = '2016-10-30 12:30:30'
dt = datetime(year=2016, month=10, day=30, hour=12, minute=30, second=30)

ts = int(time.mktime(self.t))
ts_ms = int(time.mktime(self.t) * 1000)

# 字符串转 datetime
dt = converter.str2datetime(date_str)
# 字符串转 time
converter.str2time(date_str)
# 日期字符串转时间戳，结果为秒
converter.str2timestamp(date_str)
# 日期字符串转时间戳，结果为毫秒
converter.str2timestamp(date_str, millisecond=True)
# datetime 转字符串，默认格式 %Y-%m-%d %H:%M:%S
converter.datetime2str(dt)
# datetime 转字符串，指定格式
converter.datetime2str(dt, '%Y-%m-%d')
```

###  日志功能 

对原生的 logging 进行了封装，使用起来更简单

```python
from mountains import logging
from mountains.logging import StreamHandler, FileHandler, RotatingFileHandler, TimedRotatingFileHandler

# 配置日志，输出到控制台、保存到文件、日志级别、输出格式等，文件默认保存到 log.txt
logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE), FileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))
# RotatingFileHandler 按文件大小分割日志文件
logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE), RotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))
# TimedRotatingFileHandler 按时间分割日志文件
logging.init_log(StreamHandler(format=logging.FORMAT_SIMPLE), TimedRotatingFileHandler(format=logging.FORMAT_VERBOSE, level=logging.DEBUG))

# 使用方法与原生的 logging 一样
logger = logging.getLogger(__name__)
logger.debug('hello')
```



