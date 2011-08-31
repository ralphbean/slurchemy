# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref

from slurchemy import Base

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

class models(object):
    """ API access to models.

    Use like::

        import slurchemy
        print slurchemy.models.Cluster.query.count()
        print slurchemy.models.TestclusterUsageDay.query.all()

    """
    pass


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

def tablename2CamelCase(name):
    return name.replace('_', ' ').title().replace(' ', '')[:-5]


def log(msg, quiet):
    if not quiet:
        print "[slurchemy]", msg


def init_model(engine, quiet=False):
    log("Initializing models.", quiet)
    from sqlalchemy import MetaData, Column, Table
    from sqlalchemy.orm import mapper

    metadata = MetaData(engine.url)
    for model, table_name in mappings:
        log("  Initializing %s %s" % (model.__name__, table_name), quiet)
        table = Table(table_name, metadata, autoload=True)
        mapper(model, table)
        setattr(models, model.__name__, model)
    log("Done initializing simple models.", quiet)

    for cluster in Cluster.query.all():
        clustername = cluster.name
        log("Initializing models for cluster %s" % clustername, quiet)
        for suffix in per_cluster_suffixes:
            table_name = clustername + '_' + suffix
            model_name = tablename2CamelCase(table_name)
            log("  Initializing %s %s" % (model_name, table_name), quiet)
            obj = type(model_name, (Base,), {})
            try:
                table = Table(table_name, metadata,autoload=True)
                mapper(obj, table)
                per_cluster_models_d[model_name] = obj
                per_cluster_models.append(obj)
                setattr(models, model_name, obj)
            except sqlalchemy.exc.ArgumentError as e:
                log("** Failed to init %s %s" % (model_name, table_name), quiet)
                log(str(e), quiet)
