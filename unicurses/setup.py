#!/usr/bin/env python

import sys
from glob import glob
from setuptools import setup # 0 
#from distutils.core import setup # 1

root = sys.argv[0].replace("setup.py","")

setup(name='Uni-Curses',
      version='1.3.74',
      description='Unified Curses Wrapper for Python',
      long_description='A universal Curses wrapper for Python on Windows, Linux, and\nMac OS X, with syntax close to the original NCurses. In order\nto provide Curses functionality on Windows it utilizes the ctype\nforeign function interface to wrap PDCurses, a free and open-source\nCurses implementation for Windows. CONTRIBUTORS = [GiorgosXou]',
      author='Michael Kamensky',
      author_email='stavdev@mail.ru',
      url='https://github.com/unicurses/unicurses',
      py_modules=['unicurses'],
      license='General Public License v3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      data_files=[('lib/site-packages/unicurses/32 bit binaries/pdc39dll'   , glob(root + '32 bit binaries/pdc39dll/*.*' )),
                  ('lib/site-packages/unicurses/32 bit binaries/pdc39dlls'  , glob(root + '32 bit binaries/pdc39dlls/*.*')),
                  ('lib/site-packages/unicurses/32 bit binaries/pdc39dllu'  , glob(root + '32 bit binaries/pdc39dllu/*.*')),
                  ('lib/site-packages/unicurses/32 bit binaries/pdc39dllw'  , glob(root + '32 bit binaries/pdc39dllw/*.*')),

                  ('lib/site-packages/unicurses/64 bit binaries/pdc39dll'   , glob(root + '64 bit binaries/pdc39dll/*.*' )),
                  ('lib/site-packages/unicurses/64 bit binaries/pdc39dlls'  , glob(root + '64 bit binaries/pdc39dlls/*.*')),
                  ('lib/site-packages/unicurses/64 bit binaries/pdc39dllu'  , glob(root + '64 bit binaries/pdc39dllu/*.*')),
                  ('lib/site-packages/unicurses/64 bit binaries/pdc39dllw'  , glob(root + '64 bit binaries/pdc39dllw/*.*')),

                  ('lib/site-packages/unicurses'                            , [    root + '__init__.py']  )])



# 1 = when uploading to github | directly to C:\Users\gxous\AppData\Local\Programs\Python\Python39\Lib\site-packages
# https://stackoverflow.com/a/57644936/11465149
# 0 = When uploading to pip