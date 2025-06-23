from django.db import models


# Create your models here.

class Record(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    plan = models.ForeignKey('testplans.TestPlans', help_text='执行计划', verbose_name='执行计划',
                             on_delete=models.CASCADE)
    all = models.IntegerField(default=0, verbose_name='用例总数', help_text='用例总数', blank=True)
    success = models.IntegerField(default=0, verbose_name='用例成功', help_text='用例成功', blank=True)
    fail = models.IntegerField(default=0, verbose_name='用例失败', help_text='用例失败', blank=True)
    error = models.IntegerField(default=0, verbose_name='用例错误', help_text='用例错误', blank=True)
    pass_rate = models.CharField(max_length=10, verbose_name='执行通过率', help_text='执行通过率', blank=True)
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员', blank=True)
    test_env = models.ForeignKey('projects.TestEnv', max_length=50, verbose_name='测试环境', help_text='测试环境',
                                 blank=True, on_delete=models.PROTECT, related_name='test_env')
    status = models.CharField(max_length=10, verbose_name='执行状态', help_text='执行状态', blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tb_record'
        verbose_name = '用例执行记录表'
        verbose_name_plural = verbose_name


class Report(models.Model):
    report_id = models.IntegerField(unique=True,  blank=True,primary_key=True)  # 新增字段
    info = models.JSONField(verbose_name='测试报告', help_text='测试报告', default=dict, blank=True)
    record = models.OneToOneField(Record, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.report_id and self.record:
            self.report_id = self.record.id  # 确保 report_id 与 record.id 保持一致
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tb_report'
        verbose_name = '用例报告表'
        verbose_name_plural = verbose_name