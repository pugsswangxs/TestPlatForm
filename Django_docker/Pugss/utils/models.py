# -*- coding: utf-8 -*-
# @Time : 2025-4-22 14:22
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : models.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField('逻辑删除', default=False, help_text='逻辑删除')

    class Meta:
        abstract = True
