#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='file_utils',
      version='0.1.1',
      description='Python file utilities',
      url='http://github.com/asundaresan/file_utils',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=['file_utils'],
      scripts=[
        "bin/check_duplicates.py",
        "bin/filter_images.py"
        ],
      zip_safe=False
      )

