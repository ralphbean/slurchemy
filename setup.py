from setuptools import setup, find_packages
import sys, os

version = '0.2.6'

fname = os.sep.join(__file__.split(os.sep)[:-1] + ["slurchemy/README.rst"])
f = open(fname, 'r')
long_description = f.read().split(".. split here")[1]
f.close()


setup(name='slurchemy',
      version=version,
      description="SQLAlchemy bindings for your slurmdbd (SLURM database)",
      long_description=long_description,
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 2',
          'Topic :: Database',
          'Topic :: System :: Clustering',
          'Topic :: System :: Distributed Computing',
      ],
      keywords='slurm slurmdbd sqlalchemy',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/slurchemy',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "MySQL-python",
          "sqlalchemy",
          "zope.sqlalchemy",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
