# -*- coding: utf-8 -*-
# @Time : 2025-4-27 10:48
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : serializers.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
import os

from django.conf import settings
from rest_framework import serializers

from projects.models import TestEnv
from projects.serializers import InterfaceSerializer
from testplans.models import TestStep, UploadFile
from . import models


class TestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = '__all__'


class TestStepRetrieveSerializer(serializers.ModelSerializer):
    interface = InterfaceSerializer(read_only=True)

    class Meta:
        model = TestStep
        fields = '__all__'


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'
        extra_kwargs = {
            'info': {'read_only': True},
            'file': {'write_only': True},
            'upload_path': {'write_only': True},
        }

    def validate(self, attrs):
        file = attrs.get('file')
        upload_path = attrs.get('upload_path', '')  # 获取上传路径
        # 处理文件信息
        file_name = file.name
        # 文件大小
        file_size = file.size
        # 检查 upload_path 是否以路径分隔符开头
        if upload_path and (upload_path.startswith('/') or upload_path.startswith('\\')):
            raise serializers.ValidationError('upload_path 不能以 / 或 \\ 开头')
        if file_size > 300 * 1024:
            raise serializers.ValidationError('文件大小不能超过300KB')
        if upload_path:
            relative_file_path = os.path.join(upload_path, file_name)  # 计算相对路径
        else:
            relative_file_path = file_name  # 使用默认路径
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, relative_file_path)
        if os.path.isfile(absolute_file_path):
            raise serializers.ValidationError('文件已存在')
        return attrs

    def create(self, validated_data):
        file = validated_data.get('file')
        upload_path = validated_data.get('upload_path', '')  # 获取上传路径

        # 处理文件信息
        file_name = file.name
        if upload_path:
            relative_file_path = os.path.join(upload_path, file_name)  # 计算相对路径
        else:
            relative_file_path = file_name  # 使用默认路径

        file_type = file.content_type
        info = [file_name, relative_file_path, file_type]

        # 创建并返回 UploadFile 实例
        instance = models.UploadFile.objects.create(
            file=file,  # 直接传递文件对象
            info=info,
            upload_path=upload_path  # 保存相对路径
        )
        return instance


class TestSceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestScene
        fields = '__all__'


class NestTestSceneStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStep
        fields = ['id', 'title']


class TestSceneStepSerializer(serializers.ModelSerializer):
    stepInfo = NestTestSceneStepSerializer(source='step', read_only=True)

    class Meta:
        model = models.SceneData
        fields = '__all__'


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestPlans
        fields = '__all__'


class TestSceneStepRunSerializer(serializers.ModelSerializer):
    """通过测试场景步骤 获取 测试步骤数据"""
    step = TestStepRetrieveSerializer()

    class Meta:
        model = models.SceneData
        fields = "__all__"


class TestSceneRunSerializer(serializers.ModelSerializer):
    """
    通过测试场景  获取测试场景步骤数据
    """
    scenedata_set = TestSceneStepRunSerializer(many=True)

    class Meta:
        model = models.TestScene
        fields = "__all__"


class TestPlanRunSerializer(serializers.ModelSerializer):
    """
    通过测试计划  获取测试场景步骤数据
    """
    scenes = TestSceneRunSerializer(many=True)

    class Meta:
        model = models.TestPlans
        fields = "__all__"


def exist_env_id(env_id):
    if not TestEnv.objects.filter(pk=env_id).exists():
        raise serializers.ValidationError('测试环境不存在')


class RunSerializer(serializers.Serializer):
    env = serializers.IntegerField(label='测试环境ID', help_text='测试环境ID', validators=[exist_env_id])
    plan = serializers.IntegerField(label='测试计划ID', help_text='测试计划ID', required=False, allow_null=True)
    scene = serializers.IntegerField(label='测试场景ID', help_text='测试场景ID', required=False, allow_null=True)
    data = serializers.JSONField(label='测试数据', help_text='测试数据', required=False, allow_null=True)

    def validate(self, attrs):
        # 检查 plan, scene, data 是否有且仅有一个被提供
        provided_fields = [field for field in ['plan', 'scene', 'data'] if field in attrs]

        if len(provided_fields) != 1:
            raise serializers.ValidationError('必须且只能提供 plan、scene 或 data 中的一个字段')

        plan_id = attrs.get('plan')
        scene_id = attrs.get('scene')
        data = attrs.get('data')

        if plan_id and not models.TestPlans.objects.filter(pk=plan_id).exists():
            raise serializers.ValidationError('传递的测试计划不存在')
        if scene_id and not models.TestScene.objects.filter(pk=scene_id).exists():
            raise serializers.ValidationError('传递的测试场景不存在')
        if data and not isinstance(data, dict):
            raise serializers.ValidationError('传递的测试数据必须是一个字典')

        return attrs


class CrontabTaskSerializer(serializers.ModelSerializer):
    plan_name = serializers.StringRelatedField(source='plan')
    env_name = serializers.StringRelatedField(source='env')

    class Meta:
        model = models.CrontabTask
        fields = '__all__'

    def create(self, validated_data):
        username = self.context['request'].user.username
        validated_data['tester'] = username
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        username = self.context['request'].user.username
        validated_data['tester'] = username
        instance = super().update(instance,validated_data)
        return instance
