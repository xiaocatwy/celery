#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: child_agent_report_tasks.py
@time: 2019/7/22 4:41 PM
@desc:
'''
from celery_task.celery import app
import pymysql
import datetime
import sys



from . import dayport_time


@app.task()
def cache_view_set(table_name,object_id):
    count = cache_view_set.rcache.hget(table_name, object_id)
    cache_view_set.rcache.hset(table_name, object_id, int(count)+1 if count else 1)

    view_count = cache_view_set.rcache.hget(table_name+'_v',object_id)
    if view_count:
        cache_view_set.rcache.hset(table_name+'_v', object_id, int(view_count)+1)

@app.task()
def count_reply_set(table_name,object_id,default_count=0):
    '''
    :topic 回复总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_reply_set.rcache.hget(table_name+'_count_reply', object_id)
    if not count:
        count=default_count
    count_reply_set.rcache.hset(table_name+'_count_reply', object_id, int(count)+1)

@app.task()
def count_category_topics_set(table_name,object_id,default_count=0):
    '''
    :topic_ctegory 话题总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_category_topics_set.rcache.hget(table_name+'_count_topic', object_id)
    if not count:
        count=default_count
    count_category_topics_set.rcache.hset(table_name+'_count_topic', object_id, int(count)+1)

@app.task()
def count_topics_sns_set(table_name,object_id,default_count=0):
    '''
    :topic_ctegory 点赞总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_topics_sns_set.rcache.hget(table_name+'_count_sns', object_id)
    if not count:
        count=default_count
    count_topics_sns_set.rcache.hset(table_name+'_count_sns', object_id, int(count)+1)

