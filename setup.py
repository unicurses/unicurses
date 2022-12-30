#!/usr/bin/env python

import sys
from setuptools import setup 

root = sys.argv[0].replace("setup.py","")

setup(name='Uni-Curses',
      version='v2.1.3',
      description='Unified Curses Wrapper for Python',
      long_description='A universal Curses wrapper for Python on Windows, FreeBSD, Linux, and\nMac OS X, with syntax close to the original NCurses. In order\nto provide Curses functionality on Windows it utilizes the ctype\nforeign function interface to wrap PDCurses, a free and open-source\nCurses implementation for Windows. CONTRIBUTORS = [GiorgosXou]\n\nif you have `ModuleNotFoundError` try specifying the python version like use `python3.9 -m pip install uni-curses`',
      author='Michael Kamensky',
      author_email='stavdev@mail.ru',
      maintainer='George Chousos',
      maintainer_email='gxousos@gmail.com',
      url='https://github.com/unicurses/unicurses',
      license='General Public License v3',
      platforms=['Windows', 'FreeBSD', 'Linux', 'Mac OS X'],
      packages=['unicurses'],
      package_data={'unicurses': ['32 bit binaries/*/*.*', '64 bit binaries/*/*.*']},
      install_requires=[
          'x256',
      ],
      zip_safe=False)

# pip3 install .
# python setup.py sdist
# twine upload dist/*

