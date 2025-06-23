# -*- coding: utf-8 -*-
# @Time : 2025-5-26 16:12
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : filters.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from . import models
from django_filters import rest_framework as filters


class RecordFilterSet(filters.FilterSet):
    project = filters.NumberFilter(field_name='plan__project', lookup_expr='exact')
    env = filters.NumberFilter(field_name='plan__test_env', lookup_expr='exact')

    class Meta:
        model = models.Record
        fields = ['plan', 'env', 'project']
