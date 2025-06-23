import json
import os
from django.conf import settings
from django.db import models, transaction
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers

from projects.models import TestEnv


def upload_file_path(instance, filename):
    return os.path.join(instance.upload_path, filename)


# Create your models here.

class TestPlans(models.Model):
    '''测试计划表'''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    name = models.CharField(max_length=50, verbose_name='测试计划名称', help_text='测试计划名称')
    project = models.ForeignKey('projects.Project', help_text='所属项目id', verbose_name='所属项目id',
                                on_delete=models.CASCADE, related_name='test_plans')

    scenes = models.ManyToManyField('TestScene', help_text='包含的关联场景', verbose_name='包含的关联场景', blank=True,
                                    related_name='testplan')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_test_plans'
        verbose_name = '测试计划表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']


class TestScene(models.Model):
    '''测试场景/测试套件'''
    project = models.ForeignKey('projects.Project', help_text='所属项目', verbose_name='项目名称',
                                on_delete=models.PROTECT, related_name='test_scenes')
    name = models.CharField(max_length=50, verbose_name='测试场景名称', help_text='测试场景名称')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_test_scenes'
        verbose_name = '测试场景表'
        verbose_name_plural = verbose_name


class SceneData(models.Model):
    '''测试场景数据'''
    step = models.ForeignKey('TestStep', help_text='步骤', verbose_name='步骤', on_delete=models.PROTECT)
    scene = models.ForeignKey(TestScene, help_text='所属场景', verbose_name='所属场景', on_delete=models.PROTECT,
                              related_name='scenedata_set')
    sort = models.IntegerField(verbose_name='执行排序', help_text='执行排序', blank=True)

    def __str__(self):
        return self.scene.name

    class Meta:
        db_table = 'tb_scene_data'
        verbose_name = '测试场景步骤'
        verbose_name_plural = verbose_name


setup_script = """# 前置脚本(python):
# global_tools : 全局工具函数
# data : 用例数据 
# env : 局部环境
# ENV : 全局环境
# db : 数据库操作对象
"""

teardown_script = """# 后置脚本(python):
# global_tools : 全局工具函数
# data : 用例数据 
# response : 响应对象response
# env : 局部环境
# ENV : 全局环境
# db : 数据库操作对象
"""


class TestStep(models.Model):
    '''用例表'''
    title = models.CharField(max_length=50, verbose_name='用例标题', help_text='用例标题')
    interface = models.ForeignKey('projects.Interface', help_text='所属接口', verbose_name='所属接口',
                                  on_delete=models.CASCADE)
    headers = models.JSONField(help_text='请求头', verbose_name='请求头', blank=True, default=dict)
    request = models.JSONField(help_text='请求信息', verbose_name='请求信息', blank=True, default=dict)
    file = models.JSONField(help_text='上传的文件参数', verbose_name='上传的文件参数', blank=True, default=list)
    setup_script = models.TextField(help_text='前置脚本', verbose_name='前置脚本', blank=True, default=setup_script)
    teardown_script = models.TextField(help_text='后置脚本', verbose_name='后置脚本', blank=True,
                                       default=teardown_script)

    def save(self, *args, **kwargs):
        if not self.headers:
            self.headers = {'Content-Type': 'application/json'}
        super().save(*args, **kwargs)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        if 'headers' in field_names:
            headers_index = field_names.index('headers')
            if values[headers_index] is None:
                instance.headers = {'Content-Type': 'application/json'}
        else:
            # 可选：设置默认值或者忽略处理
            instance.headers = {'Content-Type': 'application/json'}
        return instance

    @property
    def safe_headers(self):
        return self.headers or {'Content-Type': 'application/json'}

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_test_step'
        verbose_name = '测试步骤表'
        verbose_name_plural = verbose_name


class UploadFile(models.Model):
    '''文件上传'''
    # 存放文件的路径 相对于Django 中的 Setting 中的 MEDIA_URL
    # 也可以使用 upload_to='upload_file'  最后结果为 MEDIA_URL + upload_to

    file = models.FileField(upload_to=upload_file_path, verbose_name='上传文件', help_text='上传文件')

    '''文件信息如何处理'''
    info = models.JSONField(verbose_name='文件描述', help_text='文件描述', default=list)
    upload_path = models.CharField(max_length=255, verbose_name='上传路径', help_text='上传路径', blank=True,
                                   default='')

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'tb_upload_file'
        verbose_name = '上传文件表'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CrontabTask(models.Model):
    """
    定时任务表
    创建定时任务时，必须在 PeriodicTask 表中添加一条记录 才能实现定时执行的功能
    """
    CHOICES = [
        ('1', '开启'),
        ('2', '关闭'),
    ]
    project = models.ForeignKey('projects.Project', help_text='所属项目', verbose_name='项目名称',
                                on_delete=models.CASCADE, related_name='crontab_jobs')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    name = models.CharField(max_length=50, verbose_name='任务名称', help_text='任务名称', unique=True)
    plan = models.ForeignKey(TestPlans, help_text='关联计划', verbose_name='关联计划', on_delete=models.PROTECT)
    rule = models.CharField(max_length=50, verbose_name='定时执行规则', help_text='定时执行规则', default='* * * * *')
    status = models.BooleanField(default=False, verbose_name='任务状态', help_text='任务状态')
    env = models.ForeignKey(TestEnv, help_text='关联环境', verbose_name='关联环境', on_delete=models.PROTECT)
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_crontab_job'
        verbose_name = '定时任务表'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """
        当创建或者修改 CrontabTask数据时，同步去更新到 PeriodicTask 表中
        :param args:
        :param kwargs:
        :return:
        """
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
                # 创建和更新  PeriodicTask 表中
                qs = PeriodicTask.objects.filter(name=self.name)
                # 构造定时任务也的关键字参数
                params = {
                    'plan_id': self.plan.id,
                    'env_id': self.env.id,
                    'tester': self.tester
                }
                params_str = json.dumps(params, ensure_ascii=False)
                if qs:
                    # 更新
                    periodic_task_obj = qs.first()
                    periodic_task_obj.crontab = self.get_crontab()
                    periodic_task_obj.kwargs = params_str
                    periodic_task_obj.enabled = self.status
                    periodic_task_obj.save()

                else:
                    # 创建的时候指定定位任务的导入路径
                    PeriodicTask.objects.create(name=self.name,
                                                task='testplans.tasks.run_crontab_plan',
                                                crontab=self.get_crontab(),
                                                kwargs=params_str,
                                                expire_seconds=3600,  # 过期时间
                                                enabled=self.status  # 是否启用
                                                )
        except Exception as e:
            raise ValueError('创建定时任务失败')

    def delete(self, *args, **kwargs):
        """
        当删除 CrontabTask数据时，同步删除 PeriodicTask 表中数据
        :param args:
        :param kwargs:
        :return:
        """
        qs = PeriodicTask.objects.filter(name=self.name).delete()
        super().delete(*args, **kwargs)

    def get_crontab(self):
        """获取当前任务的crontab 对象"""
        crontab_list = self.rule.split(' ')
        crontab_dict = {
            'minute': crontab_list[0],
            'hour': crontab_list[1],
            'day_of_week': crontab_list[2],
            'day_of_month': crontab_list[3],  # 注意这里
            'month_of_year': crontab_list[4],  # 注意这里
        }

        queryset = CrontabSchedule.objects.filter(**crontab_dict)
        if queryset:
            crontab = queryset.first()
        else:
            crontab = CrontabSchedule.objects.create(**crontab_dict)
        return crontab
