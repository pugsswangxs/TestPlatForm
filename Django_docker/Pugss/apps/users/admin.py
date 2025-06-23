from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # 列表显示的字段
    list_display = ('username', 'email', 'mobile', 'is_staff', 'is_superuser', 'is_active')

    # 搜索字段
    search_fields = ('username', 'email', 'mobile')

    # 过滤器
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # 字段集，用于详细视图
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        ('权限', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )

    # 添加用户时的字段集
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    # 只读字段
    readonly_fields = ('last_login', 'date_joined')


# 注册自定义用户模型
admin.site.register(User, CustomUserAdmin)