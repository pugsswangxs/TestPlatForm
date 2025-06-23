# -*- coding: utf-8 -*-
# @Time : 2025-5-30 9:21
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : celery.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
import os

from celery import Celery

# 设置环境变量- Django 的环境配置路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pugss.settings')
# 创建APP应用
app = Celery('Pugss', )
# 设置配置来源
app.config_from_object('django.conf:settings', namespace='CELERY')
# 加载异步任务方式
app.autodiscover_tasks()