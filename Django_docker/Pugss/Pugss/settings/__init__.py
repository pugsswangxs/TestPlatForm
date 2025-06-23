# -*- coding: utf-8 -*-
# @Time : 2025-4-17 11:07
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : __init__.py.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
import os
import sys

# 获取环境变量
ENV = 'prod'
if os.environ.get('ENV') is None:
    print("当前环境为：dev")
    ENV = 'dev'
    from .dev import *
elif ENV in os.environ.get('ENV').strip().lower():
    print( "当前环境为：prod")
    from .pro import *
else:
    print("当前环境为：dev")
    from .dev import *