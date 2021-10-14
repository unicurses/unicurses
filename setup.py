#!/usr/bin/env python

import sys
from glob import glob
from setuptools import setup 

root = sys.argv[0].replace("setup.py","")

setup(name='Uni-Curses',
      version='v1.3.78',
      description='Unified Curses Wrapper for Python',
      long_description='A universal Curses wrapper for Python on Windows, Linux, and\nMac OS X, with syntax close to the original NCurses. In order\nto provide Curses functionality on Windows it utilizes the ctype\nforeign function interface to wrap PDCurses, a free and open-source\nCurses implementation for Windows. CONTRIBUTORS = [GiorgosXou]',
      author='Michael Kamensky',
      author_email='stavdev@mail.ru',
      url='https://github.com/unicurses/unicurses',
      license='General Public License v3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      packages=['unicurses'],
      package_data={'unicurses': ['32 bit binaries/*/*.*', '64 bit binaries/*/*.*']},
      install_requires=[
          'x256',
      ],
      zip_safe=False)

# pip3 install .
# python setup.py sdist
# twine upload dist/*

# CONTRIBUTOR https://github.com/GiorgosXou