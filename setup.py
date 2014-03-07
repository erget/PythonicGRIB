#!/usr/bin/env python

from distutils.core import setup

setup(name='PythonicGRIB',
      version='0.2.0',
      description="A Pythonic interface for the ECMWF's GRIB API",
      author='Daniel Lee',
      author_email='Lee.Daniel.1986@gmail.com',
      url='https://github.com/erget/PythonicGRIB',
      packages=['pyth_grib'],
      license='Apache',
      long_description=open("README").read())
