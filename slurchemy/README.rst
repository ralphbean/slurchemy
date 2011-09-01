slurchemy
=========

.. split here

Python `SQLAlchemy <http://www.sqlalchemy.org>`_ bindings for your slurmdbd
(`SLURM <https://computing.llnl.gov/linux/slurm/>`_ database).


Installing
----------

Easy::

    $ virtualenv test-environment && source test-environment/bin/activate
    $ pip install slurchemy

or::

    $ sudo pip install slurchemy

Using
-----

Assuming you have ``slurmdbd`` configured in ``/etc/slurm/slurmdbd.conf``
with::

    StorageType=accounting_storage/mysql
    StorageHost=mysql.example.org
    StoragePass=pass
    StorageUser=slurm
    StorageLoc=slurmdb


Then in python you can do::

    import slurchemy
    from sqlalchemy import create_engine
    engine = create_engine('mysql://slurm:pass@mysql.example.org/slurmdb')
    slurchemy.init_model(engine)
    clusters = slurchemy.Cluster.query.all()

TODO
----

 - Builtin statistics queries
