# -*- coding: utf-8 -*-
# @Time : 2025-4-17 11:02
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : dev.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from .base_setting import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'数据款名称',
        'USER':'用户名',
        'PASSWORD':'密码',
        'HOST':'主机地址',
        'PORT':'主机端口',
        'OPTIONS':{
            'charset':'utf8mb4',
        }
    }
}

# 允许所有域名跨域
CORS_ALLOW_ALL_ORIGINS = True


CELERY_BROKER_URL = 'redis://:pugss@127.0.0.1:9000/1'
CELERY_RESULT_BACKEND = 'redis://:pugss@127.0.0.1:9000/2'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 禁用celery root logger 使用Django自身的日志器
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
