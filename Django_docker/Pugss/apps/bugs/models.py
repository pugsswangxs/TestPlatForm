from django.db import models


# Create your models here.

class Bug(models.Model):
    CHOICES = [
        ('未处理', '未处理'),
        ('已处理', "已处理"),
        ("无效BUG", "无效BUG"),
        ("处理中", "处理中"), ]

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    project = models.ForeignKey('projects.Project', help_text='所属项目', verbose_name='所属项目',
                                on_delete=models.CASCADE)
    interface = models.ForeignKey('projects.Interface', help_text='接口', verbose_name='接口', on_delete=models.CASCADE)
    desc = models.TextField(verbose_name='BUG描述', help_text='BUG描述', blank=True, max_length=50000)
    info = models.JSONField(verbose_name='测试报告', help_text='测试报告', blank=True, default=dict)
    status = models.CharField(max_length=10, verbose_name='BUG状态', help_text='BUG状态', choices=CHOICES,
                              default='未处理')
    user = models.CharField(max_length=50, verbose_name='提交人员', help_text='提交人员', blank=True, default='')

    class Meta:
        db_table = 'tb_bug'
        verbose_name = 'bug表'
        verbose_name_plural = verbose_name


class BugHandle(models.Model):
    '''bug处理记录表'''
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    bug = models.ForeignKey('Bug', help_text='bug ID', verbose_name='bug ID', on_delete=models.CASCADE)
    handle = models.TextField(verbose_name='处理操作', help_text='处理操作', blank=True, max_length=50000)
    update_user = models.CharField(max_length=50, verbose_name='更新人员', help_text='更新操作', blank=True)
    reason = models.TextField(verbose_name='处理原因', help_text='处理原因', blank=True, max_length=50000)
    status = models.CharField(max_length=10, verbose_name='当前状态', help_text='当前状态', choices=Bug.CHOICES,
                                  default='未处理')

    class Meta:
        db_table = 'tb_bug_handle'
        verbose_name = 'bug处理记录表'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']