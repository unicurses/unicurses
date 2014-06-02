#!/usr/bin/env python

from distutils.core import setup

setup(name='UniCurses',
      version='1.2',
      description='Unified Curses Wrapper for Python',
      long_description='A universal Curses wrapper for Python on Windows, Linux, and\nMac OS X, with syntax close to the original NCurses. In order\nto provide Curses functionality on Windows it utilizes the ctype\nforeign function interface to wrap PDCurses, a free and open-source\nCurses implementation for Windows.',
      author='Michael Kamensky',
      author_email='stavdev@mail.ru',
      url='http://pyunicurses.sourceforge.net',
      py_modules=['unicurses'],
      license='General Public License v3',
      platforms=['Windows', 'Linux', 'Mac OS X'],
      data_files=[('Lib/site-packages/unicurses/demos', ['demos/test_background.py', 'demos/test_chgat.py', 'demos/test_colors.py', 'demos/test_keymenu.py', 'demos/test_mousemenu.py', 'demos/test_panels_advanced.py', 'demos/test_panels_basic.py', 'demos/test_roguelike.py', 'demos/test_windows.py']),
                  ('Lib/site-packages/unicurses/docs', ['docs/readme.txt', 'docs/readme.rtf', 'docs/changelog'])])
