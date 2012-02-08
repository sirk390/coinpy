#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='coinpy',
      version='0.01',
      description='Python Bitcoin Library',
      author='Christian Bodt',
      author_email='sirk390.REMOVTHIS@gmail.com',
      packages=find_packages(),
	  package_data={
        "": ["coinpy"],
       },
)
