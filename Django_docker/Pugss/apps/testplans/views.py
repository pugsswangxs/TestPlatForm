import os
from rest_framework.request import Request
from rest_framework.views import APIView

# https://github.com/musen123/unittest-ApiTestEngine
from apitestengine.core.cases import run_test
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers as _serializers
from . import models
from . import serializers
from projects.models import TestEnv
from .serializers import RunSerializer
from .tasks import *
from reports.serializers import RecordSerializer


class TestStepViewSet(ModelViewSet):
    queryset = models.TestStep.objects.all()
    serializer_class = serializers.TestStepSerializer
    filterset_fields = ['interface']

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TestStepRetrieveSerializer
        else:
            return self.serializer_class

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        cases = request.data.get('data')
        env_id = request.data.get('env')
        if not env_id:
            return _serializers.ValidationError(f"请选择正确的运行环境：")
        try:
            env = TestEnv.objects.get(id=env_id)
        except Exception as e:
            return _serializers.ValidationError(f"请选择正确的运行环境：{e}")

        result = run_case(cases, env_id)
        return Response(result)


class UploadFileViewSet(ModelViewSet):
    queryset = models.UploadFile.objects.all()
    serializer_class = serializers.UploadFileSerializer

    # permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
        instance.delete()


class TestSceneViewSet(ModelViewSet):
    """测试场景视图集"""
    queryset = models.TestScene.objects.all()
    serializer_class = serializers.TestSceneSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'testplan']


    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        env_id = request.data.get('env')
        result = run_scene(pk, env_id)
        return Response(result)


class TestSceneStepViewSet(ModelViewSet):
    """测试场景步骤视图集"""
    queryset = models.SceneData.objects.all()
    serializer_class = serializers.TestSceneStepSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["scene",]

    @action(methods=['put'], detail=False)
    def order(self, request, *args, **kwargs):
        for stepData in request.data:
            scene_data_qs = models.SceneData.objects.filter(id=stepData['id'])
            if scene_data_qs.count() == 1:
                scene_data_obj = scene_data_qs.first()
                scene_data_obj.sort = int(stepData['sort'])
                scene_data_obj.save(update_fields=["sort"])

        return Response(request.data)


class TestPlanViewSet(ModelViewSet):
    """测试计划视图集"""
    queryset = models.TestPlans.objects.all()
    serializer_class = serializers.TestPlanSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project']

    @action(methods=['post'], detail=True)
    def run(self, request, pk):
        env_id = request.data.get('env')

        data = {
            "plan": pk,
            "test_env": env_id,
            "tester": request.user.username,
            "status": "执行中",

        }

        record_serializer = RecordSerializer(data=data)
        record_serializer.is_valid(raise_exception=True)
        record_obj = record_serializer.save()
        record_id = record_obj.id
        run_plan.delay(pk, env_id, record_id)
        return Response(record_serializer.data)


class RunView(APIView):
    """当前类视图仅实现一个运行接口（POST）"""

    def post(self, request: Request, *args, **kwargs):
        serializer = RunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取测试环境ID
        env_id = serializer.validated_data.get('env')

        # 获取数据
        plan_id = serializer.validated_data.get('plan')
        scene_id = serializer.validated_data.get('scene')
        cases = serializer.validated_data.get('data')

        if cases:
            result = run_case(cases, env_id)
        elif scene_id:
            result = run_scene(scene_id, env_id)
        elif plan_id:
            data = {
                "plan": plan_id,
                "test_env": env_id,
                "tester": request.user.username,
                "status": "执行中",

            }
            record_serializer = RecordSerializer(data=data)
            record_serializer.is_valid(raise_exception=True)
            record_obj = record_serializer.save()
            record_id = record_obj.id
            # 同步执行
            # run_plan(plan_id, env_id, record_id)
            # 异步执行
            run_plan.delay(plan_id, env_id, record_id)
            result = record_serializer.data
        else:
            result = {
                "status": "error",
                "message": "请选择正确的运行环境"
            }
        return Response(result)

class CrontabTaskViewSet(ModelViewSet):
    queryset = models.CrontabTask.objects.all()
    serializer_class = serializers.CrontabTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project','plan']