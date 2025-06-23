# -*- coding: utf-8 -*-
# @Time : 2025-6-12 16:30
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : gunicorn.conf.py
# @Software : PyCharm
# @Project : Pugss
# @bak :

# gunicorn.conf.py
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent
# 绑定地址和端口（容器内）
bind = '0.0.0.0:8000'
reload =False
# 启动的 worker 数量（一般为 CPU 核心数 * 2 + 1）

pidfile = '/tmp/gunicorn.pid'
# 日志设置（建议输出到 stdout/stderr，Docker 日志系统会捕获）
accesslog = str(BASE_DIR / 'logs/gunicorn_access.log')  # 输出到标准输出
errorlog =  str(BASE_DIR / 'logs/gunicorn_error.log')
loglevel = 'info'
workers = 4
# 每个 worker 使用的类型（异步可选 eventlet/gevent，这里使用默认同步）
worker_class = 'sync'
# 最大并发请求数（根据应用负载调整）
worker_connections = 1000
# 超时时间（秒）
timeout = 120
# 设置最大请求次数，防止内存泄漏（可选）
max_requests = 1000
max_requests_jitter = 50