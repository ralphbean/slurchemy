# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref, class_mapper

import warnings
warnings.filterwarnings("ignore")

import logging as log

from slurchemy import Base
import slurchemy.utils

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
    def __unicode__(self):
        if hasattr(self, 'name'):
            return unicode(self.name)
        return super(Cluster, self).__unicode__()

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

def init_model(engine):
    log.info("Initializing models.")
    from sqlalchemy import MetaData, Column, Table
    from sqlalchemy.orm import mapper

    metadata = MetaData(engine.url)
    for model, table_name in mappings:
        log.info("  Initializing %s %s" % (model.__name__, table_name))
        table = Table(table_name, metadata, autoload=True)
        mapper(model, table)
        slurchemy.utils.add_datetime_properties(model)
        setattr(models, model.__name__, model)
    log.info("Done initializing simple models.")

    for cluster in Cluster.query.all():
        clustername = cluster.name
        log.info("Initializing models for cluster %s" % clustername)
        for suffix in per_cluster_suffixes:
            table_name = clustername + '_' + suffix
            model_name = tablename2CamelCase(table_name)
            log.info("  Initializing %s %s" % (model_name, table_name))
            cls = type(model_name, (Base,), {})
            try:
                table = Table(table_name, metadata,autoload=True)
                mapper(cls, table)
                slurchemy.utils.add_datetime_properties(model)
                per_cluster_models_d[model_name] = cls
                per_cluster_models.append(cls)
                setattr(models, model_name, cls)
            except sqlalchemy.exc.ArgumentError, e:
                log.warning("Failed to init %s %s" % (
                    model_name, table_name))
                print str(e)

        log.info("Initializing foreign relations on cluster %s" % clustername)

        assoc_model = per_cluster_models_d[
            tablename2CamelCase(clustername + "_assoc_table")
        ]
        assoc_table = class_mapper(assoc_model).tables[0]

        class_mapper(Account).add_property('%s_users' % clustername, relation(
            User,
            primaryjoin=Account.name==assoc_model.acct,
            secondaryjoin=assoc_model.user==User.name,
            secondary=assoc_table,
            backref=backref('%s_accounts' % clustername)
        ))
        class_mapper(Account).add_property(
            '%s_associations' % clustername, relation(
                assoc_model,
                primaryjoin=Account.name==assoc_model.acct,
                secondaryjoin=assoc_model.acct==Account.name,
                secondary=assoc_table,
                backref=backref('accounts')
            )
        )

        # TODO -- this needs to be fixed in el futuro

        ## XXX -- This is what we would *like* to do, but the slurmdb is set up
        ## so that QOSes are listed as a comma-separated list instead of
        ## separate foreign key entries.
#        class_mapper(Account).add_property('%s_QOSes' % clustername, relation(
#            QOS,
#            primaryjoin=Account.name==assoc_model.acct,
#            secondaryjoin=assoc_model.qos==QOS.id,
#            secondary=assoc_table,
#            backref=backref('%s_accounts' % clustername)
#        ))
        # Instead we'll do the following --

        def getx(self):
            qos_ids = []
            for assoc in getattr(self, '%s_associations' % clustername):
                qos_ids.extend(assoc.qos.split(','))

            qos_ids = [qid for qid in qos_ids if qid]

            return [QOS.query.filter(QOS.id==qid).one()  for qid in qos_ids]

        setattr(Account, '%s_QOSes' % clustername, property(getx))
