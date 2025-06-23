# -*- coding: utf-8 -*-
# @Time : 2025-5-8 16:29
# @Author : wangxs1
# @Email : wangxs1@xiaopeng.com
# @File : task.py
# @Software : PyCharm
# @Project : Pugss
# @bak :
from apitestengine.core.cases import run_test
from celery import shared_task
from projects.models import TestEnv
from testplans.models import TestScene, TestPlans
from reports.models import Report, Record
from rest_framework import serializers as _serializers_
from . import serializers


def __get_env_config(env_id, debug=True):
    """
    获取配置环境信息
    :param env_id:
    :return:
    """
    env = TestEnv.objects.get(id=env_id)

    if debug:
        # 如果处于调试模式，则合并全局变量和调试专用的变量
        # 使用字典解包（**）将两个字典合并，优先使用 debug_globals_variables 中的键值
        some_var = {**env.globals_variables, **env.debug_globals_variables}
    else:
        # 如果不是调试模式，只使用全局变量
        some_var = {**env.globals_variables}

    env_config = {
        "ENV": {
            "host": env.host,
            'headers': env.headers,
            **some_var
        },

        "DB": env.db,
        'global_func': env.global_func,
    }

    if env.globals_variables:
        env_config['ENV'].update(env.globals_variables)
    if env.debug_globals_variables:
        env_config['ENV'].update(env.debug_globals_variables)
    return env_config


def run_case(cases, env_id):
    """
    执行单条用例
    :param cases:
    :param env_id:
    :return:
    """

    case_data = [{"Cases": [cases]}]
    env_config = __get_env_config(env_id)

    res, debug_var = run_test(case_data, env_config, thread_count=1, debug=True)
    result = res.get('results')[0]['cases'][0]
    env = TestEnv.objects.get(id=env_id)
    env.debug_globals_variables = debug_var
    env.save(update_fields=['debug_globals_variables'])
    return result


def run_scene(scene_id, env_id):
    """
    执行场景用例
    :param scene_id:
    :param env_id:
    :return:
    """
    env_config = __get_env_config(env_id)
    scene_obj = TestScene.objects.get(pk=scene_id)

    _serializers = serializers.TestSceneRunSerializer(instance=scene_obj)
    cases: list = _serializers.data.get('scenedata_set')
    if not cases:
        raise _serializers_.ValidationError('场景下没有用例')
    cases.sort(key=lambda x: x.get('sort'))
    case_data = [{"Cases": [item['step'] for item in cases], 'name': scene_obj.name}]

    res, debug_var = run_test(case_data, env_config, thread_count=1, debug=True)

    result = res.get('results')[0]
    env = TestEnv.objects.get(id=env_id)
    env.debug_globals_variables = debug_var
    env.save(update_fields=['debug_globals_variables'])
    return result


@shared_task
def run_plan(plan_id, env_id, record_id):
    # 1. 获取测试环境数据
    env_config = __get_env_config(env_id)
    # 2. 获取测试计划对象
    plan_obj = TestPlans.objects.get(pk=plan_id)
    # 3. 获取测试计划下的场景
    plan_serializers = serializers.TestPlanRunSerializer(instance=plan_obj)
    plan_data = plan_serializers.data

    case_data = []
    # 4. 获取场景下的用例并排序
    for scene_dict in plan_data['scenes']:
        scene_case = scene_dict.get('scenedata_set')
        scene_case.sort(key=lambda x: x.get('sort'))
        case_data.append({"Cases": [item['step'] for item in scene_case],
                          'name': scene_dict.get('name')})

    # 5. 运行测试用例
    res = run_test(case_data, env_config, thread_count=1, debug=False)

    # 6. 修改运行状态

    record_obj = Record.objects.get(pk=record_id)
    record_obj.all = res.get('all', 0)
    record_obj.fail = res.get('fail', 0)
    record_obj.success = res.get('success', 0)
    record_obj.error = res.get('error', 0)
    #  通过率 使用百分制 并且保留两位小数
    record_obj.pass_rate = '%.2f' % (record_obj.success / record_obj.all * 100) if record_obj.all else 0
    # 7. 保存记录
    record_obj.status = 'finished'
    record_obj.save()
    # 8. 创建测试报告
    report_obj = Report.objects.create(record_id=record_id, info=res)


@shared_task
def run_crontab_plan(plan_id, env_id, tester):
    """
    导入路径： testplans.tasks.run_crontab_plan
    :param plan_id:
    :param env_id:
    :param tester:
    :return:
    """
    test_env = TestEnv.objects.get(pk=env_id)
    # 创建 record 对象
    record_obj = Record.objects.create(plan_id=plan_id, test_env=test_env, tester=tester, status='running')
    # 调用run_plan 执行
    run_plan(plan_id, env_id, record_obj.id)
