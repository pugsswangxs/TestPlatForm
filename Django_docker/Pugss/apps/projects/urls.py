# -*- coding: utf-8 -*-
# @Time : 2025-4-25 14:30
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : urls.py
# @Software : PyCharm
# @Project : Pugss
# @bak :


from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'interface', views.InterfaceViewSet)
router.register(r'testenv', views.TestEnvViewSet)
router.root_view_name = 'ProjectViewSet'
urlpatterns = router.urls