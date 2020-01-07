# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from celery import Celery

import logging

app = Celery('celery_task')
app.config_from_object('celery_task.celeryconfig')

if __name__ == '__main__':
    app.start()


#python3 dir/bin/celery -B -A asyn_crontab_tasks worker -l info