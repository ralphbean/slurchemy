import datetime
import time

from sqlalchemy.orm import class_mapper

def add_datetime_properties(cls):
    """ For every property of a class that contains '_time', add a
    corresponding '_datetime' property that converts to and from seconds
    since the epoch.

    Author:  Ralph Bean <ralph.bean@gmail.com>

    Use like::
        >>> DBSession = scoped_session(maker)
        >>> DBSession.configure(bind=engine)
        >>> metadata = MetaData(engine.url)
        >>> table = Table('thing_table', metadata, autoload=True)

        >>> class Thing(object):
        ...     pass
        >>> mapper(Thing, table)

        >>> add_datetime_properties(Thing)

        >>> t = DBSession.query(Thing).first()
        >>> print t.create_time
        ... 1314900554
        >>> print t.create_datetime
        ... 2011-09-01 14:09:14
    """

    for prop in class_mapper(cls).iterate_properties:
        if '_time' not in prop.key:
            continue  # Fugheddaboudit

        key = prop.key

        def getx(self):
            return datetime.datetime.fromtimestamp(
                float(getattr(self, key)))

        def setx(self, x):
            setattr(self, key, time.mktime(x.timetuple()))

        datetime_key = key.replace('_time', '_datetime')

        setattr(cls, datetime_key, property(getx, setx))

