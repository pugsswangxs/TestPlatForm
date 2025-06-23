import re

from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import AbstractUser


def validate_mobile(value):
    """
    验证手机号
    """
    if not re.match(r'^1[3-9]\d{9}$', value):
        raise ValidationError('手机号格式错误')

class User(AbstractUser):
    """
    用户
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号", help_text="请输入手机号",
                              blank=True, validators=[validate_mobile])
    REQUIRED_FIELDS = ['mobile']
    class Meta:
        db_table = "tb_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
