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


Then you can run::

    $ python
    >>> import sqlalchemy, slurchemy
    >>> engine = create_engine('mysql:///slurm:pass@mysql.example.org/slurmdb')
    >>> slurchemy.init_model(engine)
    >>> accounts = slurchemy.Account.query.all()


