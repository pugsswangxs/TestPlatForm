# -*- coding: utf-8 -*-
# @Time : 2025-5-23 17:39
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : serializers.py.py
# @Software : PyCharm
# @Project : Pugss
# @bak :

from rest_framework import serializers
from . import models


class BugSerializer(serializers.ModelSerializer):
    # model.Bug.objects.all(pk=1)
    # interface_url = bug.interface.url
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    interface_url = serializers.CharField(source='interface.url', read_only=True)

    class Meta:
        model = models.Bug
        fields = '__all__'

    def create(self, validated_data):
        bug_obj = super().create(validated_data)
        # 获取当前登录用户
        request_user = self.context['request'].user

        models.BugHandle.objects.create(
            bug=bug_obj,
            handle=bug_obj.status,
            update_user=request_user  # 设置 update_user 为当前登录用户
        )

        return bug_obj

    def update(self, instance, validated_data):
        bug_obj = super().update(instance, validated_data)
        # 获取当前登录用户
        request_user = self.context['request'].user
        status = f"BUG状态已更新，状态为 {bug_obj.status} "
        # 获取用户修改原因
        reason = self.initial_data.get('reason', "")
        models.BugHandle.objects.create(
            bug=bug_obj,
            handle=status,
            update_user=request_user,  # 获取当前用户
            reason=reason,
            status=bug_obj.status
        )
        return bug_obj


class BugHandlerSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = models.BugHandle
        fields = '__all__'

