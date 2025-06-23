"""
URL configuration for Pugss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view as yasg_get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

site_title = '后台API'
site_description = 'Pugss Manager API '
schema_view = yasg_get_schema_view(
    openapi.Info(
        title=site_title,
        default_version='v1.0.0',
        description=site_description,
        terms_of_service=" http://127.0.0.1:8000/",
        contact=openapi.Contact(email="xxxxxx@163.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=[IsAuthenticated],

)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 指向user 的 urls
    path('', include('users.urls'), name='users'),
    path('', include('testplans.urls'), name='testplans'),
    path('', include('projects.urls'), name='projects'),
    path('', include('reports.urls'), name='reports'),
    path('', include('bugs.urls'), name='bugs'),

    path('docs/', include_docs_urls(title=site_title, public=False, description=site_description)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

