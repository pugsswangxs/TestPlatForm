# -*- coding: utf-8 -*-
# @Time : 2025-4-17 11:02
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : pro.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from .base_setting import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'数据款名称',
        'USER':'用户名',
        'PASSWORD':'密码',
        'HOST':'pugss_mysql',   # 如果数据库在docker中，则使用docker中的服务名
        'PORT':'主机端口',    # 这里要注意如何连接的，再决定是为内网还是外网接口
        'OPTIONS':{
            'charset':'utf8mb4',
        }
    }
}


# 允许所有域名跨域
CORS_ALLOW_ALL_ORIGINS = True

CELERY_BROKER_URL = 'redis://user:password@pugss_redis:6379/1'
CELERY_RESULT_BACKEND = 'redis://user:password@pugss_redis:6379/2'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 禁用celery root logger 使用Django自身的日志器
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
