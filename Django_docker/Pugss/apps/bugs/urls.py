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
router.register(r'bugs',views.BugViewSet)
router.register(r'blog',views.BugHandlerViewSet)
# 设置默认展示的 ViewSet
router.root_view_name = 'BugViewSet'
urlpatterns = [
    path('', include(router.urls)),
]