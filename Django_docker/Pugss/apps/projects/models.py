from django.db import models
# Create your models here.
from reports.models import Record


class Project(models.Model):
    """项目表"""
    name = models.CharField(max_length=50, verbose_name='项目名称', help_text='项目名称')
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人', default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project'
        verbose_name = '项目表'
        verbose_name_plural = verbose_name

    def info(self):
        """返回项目的统计信息"""
        return [
            {"name": '执行环境', 'value': self.test_envs.count()},
            {"name": '测试场景', 'value': self.test_scenes.count()},
            {"name": '测试计划', 'value': self.test_plans.count()},
            {"name": '接口数量', 'value': self.interfaces.count()},
            {"name": '定时任务', 'value': 0},
            {"name": '执行记录', 'value': Record.objects.filter(plan__project=self).count()},
        ]

    def bugs(self):
        """返回项目的bug统计信息"""
        return [
            {"name": '未处理BUG', 'value': self.bug_set.filter(status='未处理').count()},
            {"name": '已处理BUG', 'value': self.bug_set.filter(status='已处理').count()},
            {"name": '无效BUG', 'value': self.bug_set.filter(status='无效BUG').count()},
            {"name": '处理中BUH', 'value': self.bug_set.filter(status='处理中').count()},
        ]


class TestEnv(models.Model):
    """测试环境表"""
    name = models.CharField(max_length=150, verbose_name='环境名称', help_text='环境名称')
    project = models.ForeignKey(Project, help_text='项目id', verbose_name='项目id', on_delete=models.CASCADE,
                                related_name='test_envs')
    globals_variables = models.JSONField(verbose_name='全局变量', help_text='全局变量', default=dict, null=True,
                                         blank=True)
    debug_globals_variables = models.JSONField(verbose_name='debug模式全局变量', help_text='debug模式全局变量',
                                               null=True,
                                               default=dict,
                                               blank=True)

    db = models.JSONField(verbose_name='数据库配置', help_text='数据库配置', default=list, null=True, blank=True)
    host = models.CharField(max_length=150, verbose_name='base_url地址', help_text='base_url地址', blank=True)
    headers = models.JSONField(verbose_name='请求头', help_text='请求头', default=dict, null=True, blank=True)
    global_func = models.TextField(verbose_name='测试工具文件', help_text='测试工具文件',
                                   default=open('utils/global_func.py', 'r', encoding='utf-8').read(),
                                   blank=True)

    def save(self, *args, **kwargs):
        if not self.headers:
            self.headers = {'Content-Type': 'application/json'}
        if self.globals_variables is None:
            self.globals_variables = {}
        if self.debug_globals_variables is None:
            self.debug_globals_variables = {}
        super().save(*args, **kwargs)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        headers_index = field_names.index('headers')
        if values[headers_index] is None:
            instance.headers = {'Content-Type': 'application/json'}
        for field in ['globals_variables', 'debug_globals_variables']:
            if field in field_names and getattr(instance, field) is None:
                setattr(instance, field, {})
        return instance

    @property
    def safe_headers(self):
        return self.headers or {'Content-Type': 'application/json'}

    @property
    def safe_globals(self):
        return self.globals_variables or {}

    @property
    def safe_debug_globals(self):
        return self.debug_globals_variables or {}

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_test_env'
        verbose_name = '测试环境表'
        verbose_name_plural = verbose_name


class Interface(models.Model):
    """接口表"""
    #  interface = Interface().objects.get(id=1)
    # 想要获取类型使用   interface.type
    # 想要获取接口类型使用 interface.get_type_display()

    CHOICES = [
        ('1', '项目接口'),
        ('2', '外部接口')
    ]
    project = models.ForeignKey(Project, help_text='项目id', verbose_name='项目id', on_delete=models.CASCADE,
                                related_name='interfaces')
    name = models.CharField(max_length=150, verbose_name='接口名称', help_text='接口名称')
    url = models.CharField(max_length=150, verbose_name='接口地址', help_text='接口地址')
    method = models.CharField(max_length=10, verbose_name='请求方法', help_text='请求方法')
    type = models.CharField(max_length=40, verbose_name='请求类型', help_text='请求类型', choices=CHOICES, default='1')

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'tb_interface'
        verbose_name = '接口表'
        verbose_name_plural = verbose_name
