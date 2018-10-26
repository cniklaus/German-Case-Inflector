#!/usr/bin/env python

from distutils.core import setup

with open('VERSION', 'r') as i:
    version = i.read().strip()

setup(name='German Case Inflector',
      version=version,
      description='Inflector for German Noun Phrases',
      author='Christina Niklaus'
     )