#!/usr/bin/env python

import sys
from glob import glob
from setuptools import setup
#from distutils.core import setup

root = sys.argv[0].replace("setup.py","")

setup(name='Uni-Curses',
      version='1.3.0',
      description='Unified Curses Wrapper for Python',
      long_description='A universal Curses wrapper for Python on Windows, Linux, and\nMac OS X, with syntax close to the original NCurses. In order\nto provide Curses functionality on Windows it utilizes the ctype\nforeign function interface to wrap PDCurses, a free and open-source\nCurses implementation for Windows. CONTRIBUTORS = [GiorgosXou]',
      author='Michael Kamensky',
      author_email='stavdev@mail.ru',
      url='https://github.com/unicurses/unicurses',
      py_modules=['unicurses'],
      license='General Public License v3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      data_files=[('Lib/site-packages/unicurses/pdc34dll64' , glob(root + 'pdc34dll64/*.*')),
                  ('Lib/site-packages/unicurses/pdc34dll32' , glob(root + 'pdc34dll32/*.*')),
                  ('Lib/site-packages/unicurses/pdc34dlls'  , glob(root + 'pdc34dlls/*.*' )),
                  ('Lib/site-packages/unicurses/pdc34dllu'  , glob(root + 'pdc34dllu/*.*' )),
                  ('Lib/site-packages/unicurses/pdc34dllw'  , glob(root + 'pdc34dllw/*.*' )),
                  ('Lib/site-packages/unicurses'            , [    root + '__init__.py']  )])
