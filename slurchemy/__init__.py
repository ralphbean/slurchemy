# -*- coding: utf-8 -*-

import os
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper
from zope.sqlalchemy import ZopeTransactionExtension

maker = sessionmaker(autoflush=False, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

class Base(object):
    def __unicode__(self):
        """ Default unicode representation of a model.  Very verbose. """
        return u", ".join([
            "%s: %s" % (p.key, getattr(self, p.key))
            for p in class_mapper(type(self)).iterate_properties
        ])

Base.query = DBSession.query_property()


def init_model(engine):
    """Call me before using any of the tables or classes in the model."""

    import slurchemy.reflect
    DBSession.configure(bind=engine)
    slurchemy.reflect.init_model(engine)


from slurchemy.reflect import (
    AccountCoord, Account, TableDefinition,
    Cluster, QOS, User, TXN,
    models,
    per_cluster_models,
    per_cluster_models_d,
)

__all__ = [
    AccountCoord, Account, TableDefinition,
    Cluster, User, TXN, QOS,
    models,
    per_cluster_models,
    per_cluster_models_d,
    DBSession, init_model
]

fname = os.sep.join(__file__.split(os.sep)[:-1] + ["README.rst"])
f = open(fname, 'r')
__doc__ = f.read().split(".. split here")[1]
f.close()
