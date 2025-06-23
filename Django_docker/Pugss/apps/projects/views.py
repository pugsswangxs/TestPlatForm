from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from . import models
from . import serializers


class ProjectViewSet(ModelViewSet):
    """
    项目视图集

    create:
    创建项目

    update:
    更新项目

    patch:
    部分更新项目

    retrieve:
    获取项目详情

    list:
    获取项目列表

    destory:
    删除项目
    """
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class InterfaceViewSet(ModelViewSet):
    """
    接口视图集

    create:
    创建接口

    update:
    更新接口

    partial_update:
    部分更新接口

    retrieve:
    获取接口详情

    list:
    获取接口列表

    destroy:
    删除接口
    """
    queryset = models.Interface.objects.all()
    serializer_class = serializers.InterfaceSerializer
    # permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'type']



class TestEnvViewSet(ModelViewSet):
    """
    测试环境视图集

    create:
    创建测试环境

    update:
    更新测试环境

    partial_update:
    部分更新测试环境

    retrieve:
    获取测试环境详情

    list:
    获取测试环境列表

    destroy:
    删除测试环境
    """
    queryset = models.TestEnv.objects.all()
    serializer_class = serializers.TestEnvSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project']
