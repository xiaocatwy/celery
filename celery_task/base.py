from __future__ import absolute_import

#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from setting import ENGINE


# 连接模型
class DatabaseTasks(Task):
    abstract = True
    _db = None
    _rcache = None

    @property
    def db(self):
        if self._db is None:
            self._db = scoped_session(sessionmaker(bind=create_engine(ENGINE,echo=True),autoflush=True,autocommit=False))
        return self._db


def erp_coon():
    erp_engine = create_engine("mysql+pymysql://root:123456@localhost:3306/erp?charset=utf8",echo=True)
    session_factory = sessionmaker(bind=erp_engine)
    session = session_factory()
    return session


