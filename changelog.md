v1.0:
-----

- Corrections in the readme
- Some minor fixes to the wrapper (don't deserve to be mentioned).
- Corrections to the test scripts so that they work fine on Mac OS X.

v1.1:
-----

- Changed the way UniCurses behaves if a module import error occurs (it now raises an exception instead of calling the 'exit' function).
- Released the module as a distutils package

v1.2:
-----

- Implemented a patch by Florian Stohr that fixes compatibility with Win64 pdcurses/Python. Big thanks to Florian Stohr for the fix!

v1.3:
-----

- **Fixed**: etc.
- **Fixed**: setup.py issues.
- **Added**: import pdcurses on windows 64 bit
- **Fixed**: set_panel_userptr() fails with memory access violation

v1.3.6:
-------

- **Added**: 64-bit  binaries

v1.3.7:
-------

- **Added**: 32-bit pdcurses-3.9 version binaries
- **Fixed**: sdl2 version with WIDE (Unicode) support

v1.3.74:
--------

- minor changes
- **Fixed**: (?) setup.py issues with other platforms 
- **Added**: set_tabsize() and get_tabsize() functions

v1.3.78:
--------

- overall minor changes
- Modified: test_panels_advanced.py example
- **Added**: test_move_panels_advanced.py example
- **Fixed**: setup.py & pip, finally work as they should.
- **Fixed**: waddch & wgetch & mvwaddch, now they support wide (unicode) characters
- **Fixed**: mvwinstr, now it doesn't throw error for n

v1.3.81:
--------
- **Added**: attribute A_ITALIC
- **Added**: resize_term function
- **Added**: new binaries (not v3.9)
- TEMPORARILY **Fixed**: mvwinch, now support wide (unicode) characters | Until https://github.com/python/cpython/pull/17825 gets merged or something

v2.0.0:
--------
- Update: Completly replaced cpython's ncurses-module with native the .so & .dylib libraries
- **Added**: Python2 support thanks to the ^Update although not excessively tested
- **Added**: UP-TO-DATE binaries for PDCURSES
- **Added**: cchar_t structure for NCURSES
- **Added**: wadd_wch, mvwadd_wch
- **Added**: addwstr, waddwstr, mvaddwstr, mvwaddwstr
- **Added**: CONSTANTS for both NCURSES and PDCURSES
- **Added**: extra stuff to ucs_reconfigure 
- **Added**: marco wrappers for both NCURSES and PDCURSES
- **Fixed**: removed the (TEMPORARILY Fixed) from v1.3.81
- DISCLAIMER: MANY THINGS ARE NOT TESTED YET.

v2.0.4:
--------
- **Fixed**: indentation at  "return ((m) << (((b) - 1) * 5))"
- **Fixed**: getmouse() and typo in MEVENT-structure 
- **Added**: BUTTON5 mouse events (scroll)
- **Added**: getmaxy(), getmaxx()
- **Added**: CTRL(ch) 

v2.0.5:
--------
- **Fixed**: issue with `libpanelw.so.x` on freeBSD thanks to [b1ru](https://github.com/b1ru)

v2.0.6:
--------
- **Fixed**: issue with paths in freeBSD thanks to [b1ru](https://github.com/b1ru)

v2.0.7:
--------
- **Fixed**: Typo in paths.

v2.0.8:
--------
- Finally somewhat fixed FreeBSD support. 

v2.0.9:
--------
- **Fixed**: Issue with finding `libncursesw.so`

v2.1.0:
--------
- **Fixed**: Issue with finding shared libraries *(finally!)*