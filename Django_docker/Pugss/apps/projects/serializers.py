# -*- coding: utf-8 -*-
# @Time : 2025-4-25 14:36
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : serializer.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from rest_framework import serializers
from testplans.models import TestStep

from . import models


class ProjectSerializer(serializers.ModelSerializer):
    """项目序列化器类"""

    class Meta:
        model = models.Project
        fields = ['id', 'create_time', 'leader', 'name', 'info', 'bugs']


class NestTestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = ['id', 'title']


class InterfaceSerializer(serializers.ModelSerializer):
    """接口序列化器类"""
    # teststep_set = NestTestStepSerializer(many=True,read_only=True)
    # 修改返回的键值 由 teststep_set 修改为 steps
    steps = NestTestStepSerializer(many=True, read_only=True, source='teststep_set')

    class Meta:
        model = models.Interface
        fields = "__all__"


class TestEnvSerializer(serializers.ModelSerializer):
    """测试环境"""

    class Meta:
        model = models.TestEnv
        fields = "__all__"
