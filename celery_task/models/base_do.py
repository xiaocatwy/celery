#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql.functions import now



from sqlalchemy.orm import MapperExtension
class DataUpdateExtension(MapperExtension):
    '''
    自动更新时间
    '''
    def before_update(self, mapper, connection, instance):
        if hasattr(instance, 'gmt_modified'):
            instance.gmt_modified = now()

class ModelMixin(object):
    __mapper_args__ = {
        'extension': DataUpdateExtension()
    }
    id = Column(Integer, primary_key=True, doc='ID 自动增长列')
    gmt_created = Column(DateTime,default=now(),doc='创建时间')
    gmt_modified = Column(DateTime,default=now(),doc='最后更新时间')
    deleted = Column(Boolean,default=0,doc='记录状态 0 删除 1 正常')

    @classmethod
    def get_by_id(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                return query.scalar()
            return query.first()
        return None

    @classmethod
    def get_by_column(cls, session,columns=None, lock_mode=None):
        scalar = False
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                scalar = True
                query = session.query(columns)
        else:
            query = session.query(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        query = query.filter(cls.id == id)
        if scalar:
            return query.scalar()
        return query.first()

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            if hasattr(cls, 'deleted'):
                query = session.query(cls).filter(cls.deleted==0)
            else:
                query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()


    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()


    @classmethod
    def exist(cls,session,**kargs):

        query = session.query(func.count('*')).select_from(cls)
        for key in kargs.keys():
            key=kargs.get(key)
            if hasattr(cls, key):
                query = query.filter_by()
        # if hasattr(cls, 'id'):
        #    .filter(cls.id == id)
            # if lock_mode:
            #     query = query.with_lockmode(lock_mode)
        return query.scalar() > 0
        #return False


    def columns(self):
        return [c.name for c in self.__table__.columns]

    def to_dict(self):
        return dict([(c, getattr(self, c)) for c in self.columns()])

Base = declarative_base(cls=ModelMixin)

metadata = Base.metadata

