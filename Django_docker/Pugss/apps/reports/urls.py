# -*- coding: utf-8 -*-
# @Time : 2025-5-26 16:03
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
router.register(r'record', views.RecordViewSet,basename='record')
router.register(r'report', views.ReportViewSet,basename='report')
urlpatterns = [
    path('', include(router.urls)),
]
