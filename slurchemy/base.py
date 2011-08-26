# -*- coding: utf-8 -*-
"""Represents a research entry tied to an RC account."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref

from slurchemy import DeclarativeBase, metadata, DBSession

# XXX
# TODO - Use reflection.
#   http://reliablybroken.com/b/2008/06/choosing-sqlalchemy-over-django/
# XXX


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
        return type(other) is type(self) and other.name == self.name

    def __unicode__(self):
        return unicode(self.name)

class QOS(DeclarativeBase):
    """ Quality of Service """
    __tablename__ = "qos_table"

    creation_time = Column(Integer(10), nullable=False, default=None)
    mod_time = Column(Integer(10), nullable=False, default=None)
    deleted = Column(Integer(4), nullable=True, default=0)
    id = Column(Integer(11), nullable=False, primary_key=True)
    name = Column(Unicode(256), nullable=False, default=None)
    description = Column(Unicode(256), nullable=True, default=None)
    # TODO -- work all these out.
#    flags = Column(Integer(10), nullable=True, default=0)
#    max_jobs_per_user = Column(Integer(11), nullable=True, default=None)
#    max_submit_jobs_per_user = Column(Integer(11), nullable=True, default=None)
#    max_cpus_per_job = Column(Integer(11), nullable=True, default=None)
#    max_nodes_per_job = Column(Integer(11), nullable=True, default=None)
#    max_wall_duration_per_job = Column(Integer(11), nullable=True, default=None)
#    max_cpu_mins_per_job = Column(Integer(20), nullable=True, default=None)
#    max_cpu_run_mins_per_user = Column(Integer(20), nullable=True, default=None)
#    grp_jobs = Column(Integer(11), nullable=True, default=None)
#    grp_submit_jobs = Column(Integer(11), nullable=True, default=None)
#    grp_cpus = Column(Integer(11), nullable=True, default=None)
#    grp_nodes = Column(Integer(11), nullable=True, default=None)
#    grp_wall = Column(Integer(11), nullable=True, default=None)
#    grp_cpu_mins = Column(Integer(20), nullable=True, default=None)
#    grp_cpu_run_mins = Column(Integer(20), nullable=True, default=None)
#    preempt = Column(Unicode(256), nullable=False, default=None)
#    preempt_mode = Column(Integer(11), nullable=True, default=0)
#    priority = Column(Integer(11), nullable=True, default=0)
#    usage_factor = Column(Unicode(256), nullable=False, default=1)
#    usage_thres = Column(Unicode(256), nullable=True, default=None)

    def __unicode__(self):
        return u"(%i) '%s' '%s'" % (
            self.id, self.name, self.description)


class User(DeclarativeBase):
    __tablename__ = 'user_table'

    creation_time = Column(DateTime, nullable=False, default=None)
    mod_time = Column(DateTime, nullable=False, default=0)
    deleted = Column(Integer, nullable=True, default=0)
    name = Column(Unicode(256), nullable=False, primary_key=True, default=None)
    admin_level = Column(Integer, nullable=False, default=1)

    def __unicode__(self):
        return unicode(self.name)


class TXN(DeclarativeBase):
    """ TODO -- what is a TXN? """
    __tablename__ = 'txn_table'

    id = Column(Integer, nullable=False, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=0)
    action = Column(Integer, nullable=False, default=None)
    name = Column(Unicode(256), nullable=False, default=None)
    actor = Column(Unicode(256), nullable=False, default=None)
    cluster = Column(Unicode(256), nullable=False, default=None)
    # TODO .. txn.info ?
    ##info = Column(blob?

    def __unicode__(self):
        return u"(%i) '%s' did '%s' called '%s' on cluster '%s'" % (
            self.id, self.actor, self.action, self.name, self.cluster)
