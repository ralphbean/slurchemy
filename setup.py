from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='slurchemy',
      version=version,
      description="SQLAlchemy bindings for your slurmdbd (SLURM database)",
      long_description="""\
More of a description to come.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/slurchemy',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
