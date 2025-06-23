# -*- coding: utf-8 -*-
# @Time : 2025-4-25 14:30
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : urls.py
# @Software : PyCharm
# @Project : Pugss
# @bak :

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'teststep', TestStepViewSet)
router.register(r'upload/file', UploadFileViewSet)
router.register(r'testscene', TestSceneViewSet)
router.register(r'scenedata', TestSceneStepViewSet, basename='scenedata')
router.register(r'testplan', TestPlanViewSet)
router.register(r'cron', CrontabTaskViewSet)
# 设置默认展示的 ViewSet
router.root_view_name = 'TestPlanViewSet'
urlpatterns = [
    path('', include(router.urls)),
    path('runTest/', RunView.as_view())
]
