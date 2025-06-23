# -*- coding: utf-8 -*-
# @Time : 2025-4-21 11:33
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : serializers.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers

from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            if isinstance(e, serializers.ValidationError):
                data = {'status': 400, 'message': e.detail}
            else:
                data = {'status': 400, 'message': '登录失败'}
            return data

        data['token'] = data.pop('access')
        data['message'] = "登录成功"
        data['user_id'] = self.user.id
        data['user_name'] = self.user.username
        data['status'] = 200
        return data


class CustomTokeRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['token'] = data.pop('access')
        data['message'] = "刷新成功"
        data['status'] = 'Success'
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', min_length=3, max_length=10, help_text="请输入用户名,长度为3-10位")
    password_confirm = serializers.CharField(label='确认密码', min_length=6, max_length=20, write_only=True,
                                             help_text="请再次输入密码",
                                             error_messages={
                                                 'min_length': '密码最小长度为6位',
                                                 'max_length': '密码最大长度为20位',
                                             })

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'mobile', 'email']
        extra_kwargs = {
            'username': {
                'min_length': 3,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为3位',
                    'max_length': '用户名最大长度为20位',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为6位',
                    'max_length': '密码最大长度为20位',
                }
            },
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=model.objects.all(), message='邮箱已注册')]
            },
            'mobile': {
                'required': True,
                'validators': [UniqueValidator(queryset=model.objects.all(), message='手机号已注册')]
            }
        }

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError('输入的两次密码不一致')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create(**validated_data)