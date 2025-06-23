# -*- coding: utf-8 -*-
# @Time : 2025-6-10 16:28
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : pagination.py
# @Software : PyCharm
# @Project : Pugss
# @bak :

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class OptionalPageNumberPagination(PageNumberPagination):
    """
    如果请求中没有 page 或 page_size 参数，则返回完整列表
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        # 如果没有指定 page 或 page_size，不进行分页
        if 'page' not in request.query_params and 'page_size' not in request.query_params:
            return None  # 返回 None 表示不分页
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        # 可以加上当前页、总页数等信息
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })