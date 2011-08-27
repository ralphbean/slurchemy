# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref

from slurchemy import Base


class AccountCoord(Base):
    pass

class Account(Base):
    pass

class TableDefinition(Base):
    pass

class Cluster(Base):
    def __unicode__(self):
        if hasattr(self, 'name'):
            return unicode(self.name)
        return super(Cluster, self).__unicode__()

class QOS(Base):
    pass

class User(Base):
    pass

class TXN(Base):
    pass

mappings = [
    (AccountCoord, 'acct_coord_table'),
    (Account, 'acct_table'),
    (TableDefinition, 'table_defs_table'),
    (Cluster, 'cluster_table'),
    (QOS,'qos_table'),
    (User, 'user_table'),
    (TXN, 'txn_table'),
]
per_cluster_suffixes = [
    'assoc_table',
    'assoc_usage_day_table',
    'assoc_usage_hour_table',
    'assoc_usage_month_table',
    'event_table',
    'job_table',
    'last_ran_table',
    'resv_table',
    'step_table',
    'suspend_table',
    'usage_day_table',
    'usage_hour_table',
    'usage_month_table',
    'wckey_table',
    'wckey_usage_day_table',
    'wckey_usage_hour_table',
    'wckey_usage_month_table',
]

per_cluster_models_d = {}
per_cluster_models = []

def tablename2CamelCase(name):
    return name.replace('_', ' ').title().replace(' ', '')[:-5]

def init_model(engine):
    print "Initializing models."
    from sqlalchemy import MetaData, Column, Table
    from sqlalchemy.orm import mapper

    metadata = MetaData(engine.url)
    for model, table_name in mappings:
        print "  Initializing", model.__name__, table_name
        table = Table(table_name, metadata, autoload=True)
        mapper(model, table)
    print "Done initializing simple models."

    for cluster in Cluster.query.all():
        clustername = cluster.name
        print "Initializing models for cluster", clustername
        per_cluster_models_d[clustername] = {}
        for suffix in per_cluster_suffixes:
            table_name = clustername + '_' + suffix
            model_name = tablename2CamelCase(table_name)
            print "  Initializing",model_name,table_name
            obj = type(model_name, (Base,), {})
            try:
                table = Table(table_name, metadata,autoload=True)
                mapper(obj, table)
                per_cluster_models_d[clustername][model_name] = obj
                per_cluster_models.append(obj)
            except sqlalchemy.exc.ArgumentError as e:
                print "** Failed to init", model_name, table_name
                print str(e)
