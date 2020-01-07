# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from celery.schedules import crontab
from celery_task.config import broker_url,result_backend
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = True  # 关闭日志
result_expires=600
worker_concurrency=5
# worker_max_tasks_per_child = 100

# 导入任务所在文件
imports = [
    'celery_task.tasks.pay_order_import_tasks',
]

include = (
    'celery_task.tasks'
)

'''
 minute='*', hour='*', day_of_week='*',
                 day_of_month='*', month_of_year='*'
                 '''
# 需要执行任务的配置
beat_schedule = {

    'pay_order_import_operation': {
        'task': 'celery_task.tasks.pay_order_import_tasks.pay_order_import_operation',  #
        'schedule':  crontab(minute="*/1"),  # 更新一次
    },
}
