# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

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

def init_model(engine):
    from sqlalchemy import MetaData, Column, Table
    from sqlalchemy.orm import mapper

    metadata = MetaData(engine.url)

    mappings = [
        (AccountCoord, 'acct_coord_table'),
        (Account, 'acct_table'),
        (TableDefinition, 'table_defs_table'),
        (Cluster, 'cluster_table'),
        (QOS,'qos_table'),
        (User, 'user_table'),
        (TXN, 'txn_table'),
    ]
    for model, table_name in mappings:
        table = Table(table_name, metadata, autoload=True)
        mapper(model, table)
