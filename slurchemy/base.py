# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref

from slurchemy import DeclarativeBase, metadata, DBSession


class Cluster(DeclarativeBase):
    __tablename__ = 'cluster_table'
    creation_time = Column(DateTime, nullable=False, default=None)
    mod_time = Column(DateTime, nullable=False, default=0)
    deleted = Column(Integer, nullable=True, default=0)
    name = Column(Unicode(256), nullable=False, primary_key=True, default=None)
    control_host = Column(Unicode(256), nullable=False, default=None)
    control_port = Column(Integer, nullable=False, default=0)
    rpc_version = Column(Integer, nullable=False, default=0)
    classification = Column(Integer, nullable=True, default=0)
    dimensions = Column(Integer, nullable=True, default=1)
    plugin_id_select = Column(Integer, nullable=True, default=0)
    flags = Column(Integer, nullable=True, default=0)

    def __eq__(self, other):
        return type(other) is Cluster and other.name == self.name

    def __unicode__(self):
        return unicode(self.name)
