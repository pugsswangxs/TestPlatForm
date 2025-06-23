# -*- coding: utf-8 -*-
# @Time : 2025-5-23 17:39
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : serializers.py.py
# @Software : PyCharm
# @Project : Pugss
# @bak :

from rest_framework import serializers
from . import models


class RecordSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    plan_name = serializers.StringRelatedField(source='plan')
    env_name = serializers.StringRelatedField(source='test_env')


    class Meta:
        model = models.Record
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Report
        fields = '__all__'
