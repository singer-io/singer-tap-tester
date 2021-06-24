#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

setup(name="singer-tap-tester",
      version='0.0.1',
      description="Library for testing Singer.io taps. ",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      install_requires=[
      ],
      extras_require={
          'test': [
              'ipdb',
              'pytest',
              'pytest-subtests',
              'tap-github',
          ]
      },
      # packages=find_packages(),
      # package_data = {
      #     'singer': [
      #         'logging.conf'
      #         ]
      #     },
)
