# -*- coding: utf-8 -*-

import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

maker = sessionmaker(autoflush=False, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

DeclarativeBase = declarative_base()

DeclarativeBase.query = DBSession.query_property()

metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""

    DBSession.configure(bind=engine)


__all__ = [
    DBSession, DeclarativeBase, metadata, init_model
]

with open(os.sep.join(__file__.split(os.sep)[:-2] + ["README.rst"])) as f:
    __doc__ = f.read().split(".. split here")[1]
