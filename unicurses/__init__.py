# -*- coding: utf-8 -*-

# UniCurses -- A unified multiplatform Curses provider library for Python 2.x/3.x
# Copyright (C) 2010 by Michael Kamensky.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# CONTRIBUTOR https://github.com/GiorgosXou

# import Curses (either natively if supported or via PDCurses using FFI if on MS Windows)

from glob import glob
import locale
import platform
import sys
import os


global lib1
global NCURSES   # Not needed but makes things more visually appealing? it could just be 'if not PDCURSES'
global PDCURSES
global PYCURSES  # Not sure if i would want to keep the support for the native python's module-ncurses
global PDC_LEAVEOK
global IS_CURSES_LIBRARY_UTF8

PDC_LEAVEOK            = False  # LeaveOK emulation in PDC
NCURSES                = False  # Native curses support
PDCURSES               = False  # Public Domain Curses support
UCS_DEFAULT_WRAPPER    = ""	    # A constant for the default wrapper (ucs_reconfigure)
IS_CURSES_LIBRARY_UTF8 = True   # Determine if the library iscompiled with UTF-8 support
stdscr                 = -1	    # A pointer to the standard screen
lib1                   = None   # PD\NCurses library (dll/.so)
lib2                   = None   # For NCurses's panel.so library else lib2=lib1
OPERATING_SYSTEM	   = platform.system()

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()   # TODO: fix this to actually work on native ncurses



#region +++ Main ++
def parse_ld_conf_file(fn):
    paths = []
    with open(fn, "r") as file:
        for l in file.readlines():
            l = l.strip()
            if not l:
                continue
            if l.startswith("#"):
                continue
            if l.startswith("include "):
                for sub_fn in glob(l[8:]):
                    paths.extend(parse_ld_conf_file(sub_fn))
                continue
            paths.append(l)
    return paths


def get_libncursesw_paths():
    from ctypes.util import find_library
    if OPERATING_SYSTEM == 'Darwin':
        lib_paths = [find_library('ncurses'),find_library('panel')]
    else:
        lib_paths = [find_library('ncursesw'),find_library('panelw')]

    if not lib_paths[0] or not lib_paths[1]:
        if OPERATING_SYSTEM == 'Darwin':
            msg = 'No version of shared-libraries of ncurses found on this system, please try `brew install ncurses` if this won\'t work please create an issue'
        elif OPERATING_SYSTEM == 'FreeBSD':
            msg = 'try `pkg search ncurses` then `pkg install ncurses-X.Y`'
        else:
            msg = 'No version of shared-libraries of ncurses found on this system, please try installing one\n try pgk\\apt\\etc. search ncurses and then install'
        raise Exception('NCursesNotFound: ' + msg)

    return lib_paths


try:
    import ctypes
except ImportError:
    raise ImportError("""
        Fatal error: this Python release does not support ctypes.
        Please upgrade your Python distribution
        if you want to use UniCurses on a {} platform.
        """.format(sys.platform))


if OPERATING_SYSTEM == 'Windows':
    if platform.architecture()[0] == '64bit':
        pdcurses = "64 bit binaries/pdcdllu/pdcurses.dll"  # wide-character (Unicode) &  UTF-8
    else:
        pdcurses = "32 bit binaries/pdcdllu/pdcurses.dll"  # wide-character (Unicode) &  UTF-8

    current_dir = os.path.dirname(os.path.realpath(__file__))
    path_to_pdcurses = os.path.join(current_dir, pdcurses)
    if not (os.access(pdcurses, os.F_OK)
            or os.access(path_to_pdcurses, os.F_OK)):
        raise ImportError("""
            Fatal error: can't find pdcurses.dll for linking.
            Make sure PDCurses is in the same folder as UniCurses
            if you want to use UniCurses on a {} platform.
            """.format(sys.platform))

    # We're on winXX, use pdcurses instead of native ncurses
    lib2 = lib1 = ctypes.CDLL(path_to_pdcurses)

    PDCURSES = True
    NCURSES  = False

else:
    ncurses,panel = get_libncursesw_paths()

    lib1 = ctypes.CDLL(ncurses,mode=ctypes.RTLD_GLOBAL)
    lib2 = ctypes.CDLL(panel)

    PDCURSES = False
    NCURSES  = True


# Reconfigure the UniCurses wrapper to use a certain library instead of the default
# PDCurses and the default NCurses. This must be called before initscr().
# Pass an empty string or UCS_DEFAULT_WRAPPER to use the default wrapper.
# !!! THIS IS NOT FOR GENERAL USE AND WILL IN MOST CASES BREAK UNICURSES !!!
# !!! EVEN IF IT DOESN'T MAKE YOUR APP CRASH OR HANG, IT MAY BREAK PORTABILITY !!!
# !!! IF YOU DON'T KNOW WHAT THIS MAY BE USED FOR, YOU DON'T NEED TO USE IT !!!

def ucs_reconfigure(wrapper_pdcurses = None, wrapper_ncurses = None, wrapper_ncurses_panel = None, is_utf8_dll = True):
    global IS_CURSES_LIBRARY_UTF8
    global lib1
    global lib2
    IS_CURSES_LIBRARY_UTF8 = is_utf8_dll

    if wrapper_ncurses and wrapper_ncurses_panel:
        lib1 = ctypes.CDLL(wrapper_ncurses,mode=ctypes.RTLD_GLOBAL)
        lib2 = ctypes.CDLL(wrapper_ncurses_panel)

    if wrapper_pdcurses:
        lib2 = lib1 = ctypes.CDLL(wrapper_pdcurses)	
#endregion +++ Main ++



#region +++ PDCurses/NCurses ncurses.h marco wrappers and other prereqs +++
#region ++ STRUCTS ++
# A PDC/NC structure for the mouse events
class MEVENT(ctypes.Structure):
    _fields_ = [("id", ctypes.c_short),
                ("x", ctypes.c_int),
                ("y", ctypes.c_int),
                ("z", ctypes.c_int),
                ("bstate", ctypes.c_ulong)]

# A NC structure for cchar_t
if NCURSES:
    CCHARW_MAX = 5
    WCHAR_5    = ctypes.c_wchar * CCHARW_MAX
    class cchar_t(ctypes.Structure):
        _fields_ = [("attr", ctypes.c_int),
                    ("chars", WCHAR_5)]
#endregion -- STRUCTS --


def CSTR(s):
    """
    Return a bytes-encoded C style string from anything that's convertable with str.
    It is used to pass strings to PDCurses which expects a C-formatted string.
    """

    global IS_CURSES_LIBRARY_UTF8

    if IS_CURSES_LIBRARY_UTF8:
        return str(s).encode()
    else:
        return str(s).encode(code)


if PDCURSES:
    def PD_COLOR_PAIR(n):
        """
        Choose a color pair.
        """

        return (n << PDC_COLOR_SHIFT) & A_COLOR


    def PD_PAIR_NUMBER(n):
        """
        Pair number from curses.h.
        """

        return (n & A_COLOR) >> PDC_COLOR_SHIFT


    def PD_GET_CURSCR(): # TODO: this should actually work in NCURSES too, idk why it's not a general function
        """
        Get the PDC curscr (NOT PORTABLE!), this is pointer to the current screen image.
        """

        return ctypes.c_int.in_dll(lib1, "curscr")

elif NCURSES:
    NCURSES_ATTR_SHIFT = 8


    def NCURSES_BITS(mask,shift):
        return (mask << ((shift) + NCURSES_ATTR_SHIFT))


    def NC_COLOR_PAIR(n):
        return (NCURSES_BITS((n), 0) & A_COLOR)
    
    def NC_PAIR_NUMBER(n):

        return lib1.PAIR_NUMBER(n)

    # TODO: implement getcursor in NCURSES and make the call platform independent
#endregion --- PDCurses/NCurses ncurses.h macro wrappers and other prereqs ---


#region +++ CONSTANTS: PDCurses\Ncurses ncurses.h +++
if PDCURSES:
    #region ++ Attributs & Colors (PDC) ++
    PDC_COLOR_SHIFT  = 24
    PDC_ATTR_SHIFT   = 19

    # Attributes
    A_ALTCHARSET = 0x00010000
    A_RIGHT      = 0x00020000
    A_LEFT       = 0x00040000
    A_ITALIC     = 0x00080000
    A_UNDERLINE  = 0x00100000
    A_REVERSE    = 0x00200000
    A_BLINK      = 0x00400000
    A_BOLD       = 0x00800000
    A_NORMAL     = 0
    A_DIM        = 0
    A_INVIS      = 0
    A_HORIZONTAL = 0
    A_LOW  		 = 0
    A_TOP		 = 0
    A_VERTICAL   = 0
    A_STANDOUT   = (A_REVERSE | A_BOLD)
    A_PROTECT    = (A_UNDERLINE | A_LEFT | A_RIGHT)
    A_ATTRIBUTES = 0xffff0000
    A_COLOR      = 0xff000000
    A_CHARTEXT   = 0x0000ffff

    A_RIGHTLINE  = A_RIGHT
    A_LEFTLINE   = A_LEFT

    # Colors
    COLOR_BLACK   = 0
    COLOR_BLUE    = 1
    COLOR_GREEN   = 2
    COLOR_RED     = 4
    COLOR_CYAN    = (COLOR_BLUE | COLOR_GREEN)
    COLOR_MAGENTA = (COLOR_RED  | COLOR_BLUE )
    COLOR_YELLOW  = (COLOR_RED  | COLOR_GREEN)
    COLOR_WHITE   = 7
    #endregion -- Attributs & Colors (PDC) --


    #region ++ Key mapping (PDC) ++
    KEY_CODE_YES  = 0x100  # If get_wch() gives a key code
    KEY_BREAK     = 0x101  # Not on PC KBD
    KEY_MIN		  = KEY_BREAK
    KEY_DOWN      = 0x102  # Down arrow key
    KEY_UP        = 0x103  # Up arrow key
    KEY_LEFT      = 0x104  # Left arrow key
    KEY_RIGHT     = 0x105  # Right arrow key
    KEY_HOME      = 0x106  # home key
    KEY_BACKSPACE = 0x107  # not on pc
    KEY_F0        = 0x108  # function keys; 64 reserved
    KEY_DL        = 0x148  # delete line
    KEY_IL        = 0x149  # insert line
    KEY_DC        = 0x14a  # delete character
    KEY_IC        = 0x14b  # insert char or enter ins mode
    KEY_EIC       = 0x14c  # exit insert char mode
    KEY_CLEAR     = 0x14d  # clear screen
    KEY_EOS       = 0x14e  # clear to end of screen
    KEY_EOL       = 0x14f  # clear to end of line
    KEY_SF        = 0x150  # scroll 1 line forward
    KEY_SR        = 0x151  # scroll 1 line back (reverse)
    KEY_NPAGE     = 0x152  # next page
    KEY_PPAGE     = 0x153  # previous page
    KEY_STAB      = 0x154  # set tab
    KEY_CTAB      = 0x155  # clear tab
    KEY_CATAB     = 0x156  # clear all tabs
    KEY_ENTER     = 0x157  # enter or send (unreliable)
    KEY_SRESET    = 0x158  # soft/reset (partial/unreliable)
    KEY_RESET     = 0x159  # reset/hard reset (unreliable)
    KEY_PRINT     = 0x15a  # print/copy
    KEY_LL        = 0x15b  # home down/bottom (lower left)
    KEY_ABORT     = 0x15c  # abort/terminate key (any)
    KEY_SHELP     = 0x15d  # short help
    KEY_LHELP     = 0x15e  # long help
    KEY_BTAB      = 0x15f  # Back tab key
    KEY_BEG       = 0x160  # beg(inning) key
    KEY_CANCEL    = 0x161  # cancel key
    KEY_CLOSE     = 0x162  # close key
    KEY_COMMAND   = 0x163  # cmd (command) key
    KEY_COPY      = 0x164  # copy key
    KEY_CREATE    = 0x165  # create key
    KEY_END       = 0x166  # end key
    KEY_EXIT      = 0x167  # exit key
    KEY_FIND      = 0x168  # find key
    KEY_HELP      = 0x169  # help key
    KEY_MARK      = 0x16a  # mark key
    KEY_MESSAGE   = 0x16b  # message key
    KEY_MOVE      = 0x16c  # move key
    KEY_NEXT      = 0x16d  # next object key
    KEY_OPEN      = 0x16e  # open key
    KEY_OPTIONS   = 0x16f  # options key
    KEY_PREVIOUS  = 0x170  # previous object key
    KEY_REDO      = 0x171  # redo key
    KEY_REFERENCE = 0x172  # ref(erence) key
    KEY_REFRESH   = 0x173  # refresh key
    KEY_REPLACE   = 0x174  # replace key
    KEY_RESTART   = 0x175  # restart key
    KEY_RESUME    = 0x176  # resume key
    KEY_SAVE      = 0x177  # save key
    KEY_SBEG      = 0x178  # shifted beginning key
    KEY_SCANCEL   = 0x179  # shifted cancel key
    KEY_SCOMMAND  = 0x17a  # shifted command key
    KEY_SCOPY     = 0x17b  # shifted copy key
    KEY_SCREATE   = 0x17c  # shifted create key
    KEY_SDC       = 0x17d  # shifted delete char key
    KEY_SDL       = 0x17e  # shifted delete line key
    KEY_SELECT    = 0x17f  # select key
    KEY_SEND      = 0x180  # shifted end key
    KEY_SEOL      = 0x181  # shifted clear line key
    KEY_SEXIT     = 0x182  # shifted exit key
    KEY_SFIND     = 0x183  # shifted find key
    KEY_SHOME     = 0x184  # shifted home key
    KEY_SIC       = 0x185  # shifted input key
    KEY_SLEFT     = 0x187  # shifted left arrow key
    KEY_SMESSAGE  = 0x188  # shifted message key
    KEY_SMOVE     = 0x189  # shifted move key
    KEY_SNEXT     = 0x18a  # shifted next key
    KEY_SOPTIONS  = 0x18b  # shifted options key
    KEY_SPREVIOUS = 0x18c  # shifted prev key
    KEY_SPRINT    = 0x18d  # shifted print key
    KEY_SREDO     = 0x18e  # shifted redo key
    KEY_SREPLACE  = 0x18f  # shifted replace key
    KEY_SRIGHT    = 0x190  # shifted right arrow
    KEY_SRSUME    = 0x191  # shifted resume key
    KEY_SSAVE     = 0x192  # shifted save key
    KEY_SSUSPEND  = 0x193  # shifted suspend key
    KEY_SUNDO     = 0x194  # shifted undo key
    KEY_SUSPEND   = 0x195  # suspend key
    KEY_UNDO      = 0x196  # undo key
    KEY_A1        = 0x1c1
    KEY_A3        = 0x1c3
    KEY_B2        = 0x1c5
    KEY_C1        = 0x1c7
    KEY_C3        = 0x1c9
    KEY_MOUSE     = 0x21b
    KEY_RESIZE    = 0x222
    KEY_SDOWN     = 0x224
    KEY_MAX       = KEY_SDOWN
    #KEY_EVENT    = PDC_KEY_EVENT
    #endregion -- Key mapping (PDC) --


    #region ++ Mouse mapping (PDC) ++
    BUTTON1_RELEASED       = 0x00000001
    BUTTON1_PRESSED        = 0x00000002
    BUTTON1_CLICKED        = 0x00000004
    BUTTON1_DOUBLE_CLICKED = 0x00000008
    BUTTON1_TRIPLE_CLICKED = 0x00000010

    BUTTON2_RELEASED       = 0x00000020
    BUTTON2_PRESSED        = 0x00000040
    BUTTON2_CLICKED        = 0x00000080
    BUTTON2_DOUBLE_CLICKED = 0x00000100
    BUTTON2_TRIPLE_CLICKED = 0x00000200

    BUTTON3_RELEASED       = 0x00000400
    BUTTON3_PRESSED        = 0x00000800
    BUTTON3_CLICKED        = 0x00001000
    BUTTON3_DOUBLE_CLICKED = 0x00002000
    BUTTON3_TRIPLE_CLICKED = 0x00004000

    BUTTON4_RELEASED       = 0x00008000
    BUTTON4_PRESSED        = 0x00010000
    BUTTON4_CLICKED        = 0x00020000
    BUTTON4_DOUBLE_CLICKED = 0x00040000
    BUTTON4_TRIPLE_CLICKED = 0x00080000

    BUTTON5_RELEASED       = 0x00100000
    BUTTON5_PRESSED        = 0x00200000
    BUTTON5_CLICKED        = 0x00400000
    BUTTON5_DOUBLE_CLICKED = 0x00800000
    BUTTON5_TRIPLE_CLICKED = 0x01000000

    BUTTON_SHIFT		   = 0x04000000
    BUTTON_CTRL 		   = 0x08000000
    BUTTON_ALT   		   = 0x10000000

    ALL_MOUSE_EVENTS       = 0x1fffffff
    REPORT_MOUSE_POSITION  = 0x20000000
    #endregion -- Mouse mapping (PDC) --

elif NCURSES:
    #region ++ Attributs & Colors (NC) ++
    # Attributes
    A_NORMAL     = 0
    A_ATTRIBUTES = NCURSES_BITS(~(1 - 1),0)
    A_CHARTEXT   = NCURSES_BITS(1,0) - 1
    A_COLOR      = NCURSES_BITS(((1) << 8) - 1,0)
    A_STANDOUT   = NCURSES_BITS(1,8)
    A_UNDERLINE  = NCURSES_BITS(1,9)
    A_REVERSE    = NCURSES_BITS(1,10)
    A_BLINK      = NCURSES_BITS(1,11)
    A_DIM        = NCURSES_BITS(1,12)
    A_BOLD       = NCURSES_BITS(1,13)
    A_ALTCHARSET = NCURSES_BITS(1,14)
    A_INVIS      = NCURSES_BITS(1,15)
    A_PROTECT    = NCURSES_BITS(1,16)
    A_HORIZONTAL = NCURSES_BITS(1,17)
    A_LEFT       = NCURSES_BITS(1,18)
    A_LOW        = NCURSES_BITS(1,19)
    A_RIGHT      = NCURSES_BITS(1,20)
    A_TOP        = NCURSES_BITS(1,21)
    A_VERTICAL   = NCURSES_BITS(1,22)
    A_ITALIC	 = NCURSES_BITS(1,23)

    # Colors
    COLOR_BLACK   = 0
    COLOR_RED     = 1
    COLOR_GREEN   = 2
    COLOR_YELLOW  = 3
    COLOR_BLUE    = 4
    COLOR_MAGENTA = 5
    COLOR_CYAN    = 6
    COLOR_WHITE   = 7
    #endregion -- Attributs & Colors (NC) --


    #region ++ Key mapping (NC) ++
    KEY_CODE_YES  = 0o400  # A wchar_t contains a key code
    KEY_MIN       = 0o401  # Minimum curses key
    KEY_BREAK     = 0o401  # Break key (unreliable)
    KEY_SRESET    = 0o530  # Soft (partial) reset (unreliable)
    KEY_RESET     = 0o531  # Reset or hard reset (unreliable)
    KEY_DOWN      = 0o402  # down-arrow key
    KEY_UP        = 0o403  # up-arrow key
    KEY_LEFT      = 0o404  # left-arrow key
    KEY_RIGHT     = 0o405  # right-arrow key
    KEY_HOME      = 0o406  # home key
    KEY_BACKSPACE = 0o407  # backspace key
    KEY_F0        = 0o410  # Function keys.  Space for 64
    KEY_DL        = 0o510  # delete-line key
    KEY_IL        = 0o511  # insert-line key
    KEY_DC        = 0o512  # delete-character key
    KEY_IC        = 0o513  # insert-character key
    KEY_EIC       = 0o514  # sent by rmir or smir in insert mode
    KEY_CLEAR     = 0o515  # clear-screen or erase key
    KEY_EOS       = 0o516  # clear-to-end-of-screen key
    KEY_EOL       = 0o517  # clear-to-end-of-line key
    KEY_SF        = 0o520  # scroll-forward key
    KEY_SR        = 0o521  # scroll-backward key
    KEY_NPAGE     = 0o522  # next-page key
    KEY_PPAGE     = 0o523  # previous-page key
    KEY_STAB      = 0o524  # set-tab key
    KEY_CTAB      = 0o525  # clear-tab key
    KEY_CATAB     = 0o526  # clear-all-tabs key
    KEY_ENTER     = 0o527  # enter/send key
    KEY_PRINT     = 0o532  # print key
    KEY_LL        = 0o533  # lower-left key (home down)
    KEY_A1        = 0o534  # upper left of keypad
    KEY_A3        = 0o535  # upper right of keypad
    KEY_B2        = 0o536  # center of keypad
    KEY_C1        = 0o537  # lower left of keypad
    KEY_C3        = 0o540  # lower right of keypad
    KEY_BTAB      = 0o541  # back-tab key
    KEY_BEG       = 0o542  # begin key
    KEY_CANCEL    = 0o543  # cancel key
    KEY_CLOSE     = 0o544  # close key
    KEY_COMMAND   = 0o545  # command key
    KEY_COPY      = 0o546  # copy key
    KEY_CREATE    = 0o547  # create key
    KEY_END       = 0o550  # end key
    KEY_EXIT      = 0o551  # exit key
    KEY_FIND      = 0o552  # find key
    KEY_HELP      = 0o553  # help key
    KEY_MARK      = 0o554  # mark key
    KEY_MESSAGE   = 0o555  # message key
    KEY_MOVE      = 0o556  # move key
    KEY_NEXT      = 0o557  # next key
    KEY_OPEN      = 0o560  # open key
    KEY_OPTIONS   = 0o561  # options key
    KEY_PREVIOUS  = 0o562  # previous key
    KEY_REDO      = 0o563  # redo key
    KEY_REFERENCE = 0o564  # reference key
    KEY_REFRESH   = 0o565  # refresh key
    KEY_REPLACE   = 0o566  # replace key
    KEY_RESTART   = 0o567  # restart key
    KEY_RESUME    = 0o570  # resume key
    KEY_SAVE      = 0o571  # save key
    KEY_SBEG      = 0o572  # shifted begin key
    KEY_SCANCEL   = 0o573  # shifted cancel key
    KEY_SCOMMAND  = 0o574  # shifted command key
    KEY_SCOPY     = 0o575  # shifted copy key
    KEY_SCREATE   = 0o576  # shifted create key
    KEY_SDC       = 0o577  # shifted delete-character key
    KEY_SDL       = 0o600  # shifted delete-line key
    KEY_SELECT    = 0o601  # select key
    KEY_SEND      = 0o602  # shifted end key
    KEY_SEOL      = 0o603  # shifted clear-to-end-of-line key
    KEY_SEXIT     = 0o604  # shifted exit key
    KEY_SFIND     = 0o605  # shifted find key
    KEY_SHELP     = 0o606  # shifted help key
    KEY_SHOME     = 0o607  # shifted home key
    KEY_SIC       = 0o610  # shifted insert-character key
    KEY_SLEFT     = 0o611  # shifted left-arrow key
    KEY_SMESSAGE  = 0o612  # shifted message key
    KEY_SMOVE     = 0o613  # shifted move key
    KEY_SNEXT     = 0o614  # shifted next key
    KEY_SOPTIONS  = 0o615  # shifted options key
    KEY_SPREVIOUS = 0o616  # shifted previous key
    KEY_SPRINT    = 0o617  # shifted print key
    KEY_SREDO     = 0o620  # shifted redo key
    KEY_SREPLACE  = 0o621  # shifted replace key
    KEY_SRIGHT    = 0o622  # shifted right-arrow key
    KEY_SRSUME    = 0o623  # shifted resume key
    KEY_SSAVE     = 0o624  # shifted save key
    KEY_SSUSPEND  = 0o625  # shifted suspend key
    KEY_SUNDO     = 0o626  # shifted undo key
    KEY_SUSPEND   = 0o627  # suspend key
    KEY_UNDO      = 0o630  # undo key
    KEY_MOUSE     = 0o631  # Mouse event has occurred
    KEY_RESIZE    = 0o632  # Terminal resize event
    KEY_EVENT     = 0o633  # We were interrupted by an event
    KEY_MAX       = 0o777  # Maximum key value is 0633
    #endregion -- Key mapping (NC) --


    #region ++ Mouse mapping (NC) ++
    NCURSES_MOUSE_VERSION = 2  # TODO: Understand how it is defined

    def NCURSES_MOUSE_MASK(b,m):
        if NCURSES_MOUSE_VERSION > 1:
            return ((m) << (((b) - 1) * 5))
        else:
            return ((m) << (((b) - 1) * 6))

    NCURSES_BUTTON_RELEASED =  1
    NCURSES_BUTTON_PRESSED  =  2
    NCURSES_BUTTON_CLICKED  =  4
    NCURSES_DOUBLE_CLICKED  = 10
    NCURSES_TRIPLE_CLICKED  = 20
    NCURSES_RESERVED_EVENT  = 40

    BUTTON1_RELEASED       = NCURSES_MOUSE_MASK(1, NCURSES_BUTTON_RELEASED)
    BUTTON1_PRESSED        = NCURSES_MOUSE_MASK(1, NCURSES_BUTTON_PRESSED)
    BUTTON1_CLICKED        = NCURSES_MOUSE_MASK(1, NCURSES_BUTTON_CLICKED)
    BUTTON1_DOUBLE_CLICKED = NCURSES_MOUSE_MASK(1, NCURSES_DOUBLE_CLICKED)
    BUTTON1_TRIPLE_CLICKED = NCURSES_MOUSE_MASK(1, NCURSES_TRIPLE_CLICKED)

    BUTTON2_RELEASED       = NCURSES_MOUSE_MASK(2, NCURSES_BUTTON_RELEASED)
    BUTTON2_PRESSED        = NCURSES_MOUSE_MASK(2, NCURSES_BUTTON_PRESSED)
    BUTTON2_CLICKED        = NCURSES_MOUSE_MASK(2, NCURSES_BUTTON_CLICKED)
    BUTTON2_DOUBLE_CLICKED = NCURSES_MOUSE_MASK(2, NCURSES_DOUBLE_CLICKED)
    BUTTON2_TRIPLE_CLICKED = NCURSES_MOUSE_MASK(2, NCURSES_TRIPLE_CLICKED)

    BUTTON3_RELEASED       = NCURSES_MOUSE_MASK(3, NCURSES_BUTTON_RELEASED)
    BUTTON3_PRESSED        = NCURSES_MOUSE_MASK(3, NCURSES_BUTTON_PRESSED)
    BUTTON3_CLICKED        = NCURSES_MOUSE_MASK(3, NCURSES_BUTTON_CLICKED)
    BUTTON3_DOUBLE_CLICKED = NCURSES_MOUSE_MASK(3, NCURSES_DOUBLE_CLICKED)
    BUTTON3_TRIPLE_CLICKED = NCURSES_MOUSE_MASK(3, NCURSES_TRIPLE_CLICKED)

    BUTTON4_RELEASED       = NCURSES_MOUSE_MASK(4, NCURSES_BUTTON_RELEASED)
    BUTTON4_PRESSED        = NCURSES_MOUSE_MASK(4, NCURSES_BUTTON_PRESSED)
    BUTTON4_CLICKED        = NCURSES_MOUSE_MASK(4, NCURSES_BUTTON_CLICKED)
    BUTTON4_DOUBLE_CLICKED = NCURSES_MOUSE_MASK(4, NCURSES_DOUBLE_CLICKED)
    BUTTON4_TRIPLE_CLICKED = NCURSES_MOUSE_MASK(4, NCURSES_TRIPLE_CLICKED)

    BUTTON5_RELEASED       = NCURSES_MOUSE_MASK(5, NCURSES_BUTTON_RELEASED)
    BUTTON5_PRESSED        = NCURSES_MOUSE_MASK(5, NCURSES_BUTTON_PRESSED)
    BUTTON5_CLICKED        = NCURSES_MOUSE_MASK(5, NCURSES_BUTTON_CLICKED)
    BUTTON5_DOUBLE_CLICKED = NCURSES_MOUSE_MASK(5, NCURSES_DOUBLE_CLICKED)
    BUTTON5_TRIPLE_CLICKED = NCURSES_MOUSE_MASK(5, NCURSES_TRIPLE_CLICKED)

    if NCURSES_MOUSE_VERSION > 1:
        BUTTON_CTRL  = NCURSES_MOUSE_MASK(6, 1)
        BUTTON_SHIFT = NCURSES_MOUSE_MASK(6, 2)
        BUTTON_ALT   = NCURSES_MOUSE_MASK(6, 4)

        REPORT_MOUSE_POSITION = NCURSES_MOUSE_MASK(6, 10)
    else:
        BUTTON_CTRL  = NCURSES_MOUSE_MASK(5, 1)
        BUTTON_SHIFT = NCURSES_MOUSE_MASK(5, 2)
        BUTTON_ALT   = NCURSES_MOUSE_MASK(5, 4)

        REPORT_MOUSE_POSITION = NCURSES_MOUSE_MASK(5, 10)

    ALL_MOUSE_EVENTS = (REPORT_MOUSE_POSITION - 1)
    #endregion -- Mouse mapping (NC) --
#endregion --- CONSTANTS: PDCurses\Ncurses ncurses.h ---



#region +++ CONSTANTS: Platform-independent +++
# General
OK = 0
ERR = -1


def RCCHAR(ch):
    """
    Reverse of CCHAR function.
    """

    if isinstance(ch, int):
        return chr(ch)
    if isinstance(ch, str) or isinstance(ch, bytes):
        return ch
    raise ValueError("RCCHAR: can't parse a non-char/non-int value.")

def CCHAR(ch):
    """
    Get a C character.
    """

    if isinstance(ch, str) or isinstance(ch, bytes):
        return ord(ch)
    if isinstance(ch, int):
        return ch
    raise ValueError("CCHAR: can't parse a non-char/non-int value.")


def ALTCHAR(ch):
    """
    Alternate character set.
    """

    if isinstance(ch, str) or isinstance(ch, bytes):
        return ord(ch) | A_ALTCHARSET
    if isinstance(ch, int):
        return ch | A_ALTCHARSET
    raise ValueError("ALTCHAR: can't parse a non-char/non-int value.")


def CTRL(ch):  #1
    """
    Returns CTRL + KEY.
    """

    return CCHAR(ch) & 0x1f


def KEY_F(n):
    """
    Return function keys 1-64.
    """

    return KEY_F0 + n


# ACS Alternate Character Set Symbols
ACS_ULCORNER = ALTCHAR('l')
ACS_LLCORNER = ALTCHAR('m')
ACS_URCORNER = ALTCHAR('k')
ACS_LRCORNER = ALTCHAR('j')
ACS_LTEE     = ALTCHAR('t')
ACS_RTEE     = ALTCHAR('u')
ACS_BTEE     = ALTCHAR('v')
ACS_TTEE     = ALTCHAR('w')
ACS_HLINE    = ALTCHAR('q')
ACS_VLINE    = ALTCHAR('x')
ACS_PLUS     = ALTCHAR('n')
ACS_S1       = ALTCHAR('o')
ACS_S9       = ALTCHAR('s')
ACS_DIAMOND  = ALTCHAR('`')
ACS_CKBOARD  = ALTCHAR('a')
ACS_DEGREE   = ALTCHAR('f')
ACS_PLMINUS  = ALTCHAR('g')
ACS_BULLET   = ALTCHAR('~')
ACS_LARROW   = ALTCHAR(',')
ACS_RARROW   = ALTCHAR('+')
ACS_DARROW   = ALTCHAR('.')
ACS_UARROW   = ALTCHAR('-')
ACS_BOARD    = ALTCHAR('h')
ACS_LANTERN  = ALTCHAR('i')
ACS_BLOCK    = ALTCHAR('0')
ACS_S3       = ALTCHAR('p')
ACS_S7       = ALTCHAR('r')
ACS_LEQUAL   = ALTCHAR('y')
ACS_GEQUAL   = ALTCHAR('z')
ACS_PI       = ALTCHAR('{')
ACS_NEQUAL   = ALTCHAR('|')
ACS_STERLING = ALTCHAR('}')
ACS_BSSB     = ACS_ULCORNER
ACS_SSBB     = ACS_LLCORNER
ACS_BBSS     = ACS_URCORNER
ACS_SBBS     = ACS_LRCORNER
ACS_SBSS     = ACS_RTEE
ACS_SSSB     = ACS_LTEE
ACS_SSBS     = ACS_BTEE
ACS_BSSS     = ACS_TTEE
ACS_BSBS     = ACS_HLINE
ACS_SBSB     = ACS_VLINE
ACS_SSSS     = ACS_PLUS

# Unicurses-specific: pseudographic mode
SCS_ULCORNER = CCHAR('+')
SCS_LLCORNER = CCHAR('+')
SCS_URCORNER = CCHAR('+')
SCS_LRCORNER = CCHAR('+')
SCS_LTEE     = CCHAR('+')
SCS_RTEE     = CCHAR('+')
SCS_BTEE     = CCHAR('+')
SCS_TTEE     = CCHAR('+')
SCS_HLINE    = CCHAR('-')
SCS_VLINE    = CCHAR('|')
SCS_PLUS     = CCHAR('+')
SCS_S1       = CCHAR('-')
SCS_S9       = CCHAR('_')
SCS_DIAMOND  = CCHAR('+')
SCS_CKBOARD  = CCHAR(':')
SCS_DEGREE   = CCHAR('\\')
SCS_PLMINUS  = CCHAR('#')
SCS_BULLET   = CCHAR('o')
SCS_LARROW   = CCHAR('<')
SCS_RARROW   = CCHAR('>')
SCS_DARROW   = CCHAR('v')
SCS_UARROW   = CCHAR('^')
SCS_BOARD    = CCHAR('#')
SCS_LANTERN  = CCHAR('*')
SCS_BLOCK    = CCHAR('#')
SCS_S3       = CCHAR('-')
SCS_S7       = CCHAR('-')
SCS_LEQUAL   = CCHAR('<')
SCS_GEQUAL   = CCHAR('>')
SCS_PI       = CCHAR('n')
SCS_NEQUAL   = CCHAR('+')
SCS_STERLING = CCHAR('L')
SCS_BSSB     = ACS_ULCORNER
SCS_SSBB     = ACS_LLCORNER
SCS_BBSS     = ACS_URCORNER
SCS_SBBS     = ACS_LRCORNER
SCS_SBSS     = ACS_RTEE
SCS_SSSB     = ACS_LTEE
SCS_SSBS     = ACS_BTEE
SCS_BSSS     = ACS_TTEE
SCS_BSBS     = ACS_HLINE
SCS_SBSB     = ACS_VLINE
SCS_SSSS     = ACS_PLUS
#endregion --- CONSTANTS: Platform-independent ---



#region	 +++ FUNCTION DEFINITIONS (PDC)\(NC) +++
lib1.erasechar.restype        = ctypes.c_char
lib1.keyname.restype          = ctypes.c_char_p
lib1.killchar.restype         = ctypes.c_char
lib1.longname.restype         = ctypes.c_char_p
lib1.termattrs.restype        = ctypes.c_ulong
lib1.termname.restype         = ctypes.c_char_p
lib1.winch.restype            = ctypes.c_uint
lib1.mvwinch.restype          = ctypes.c_uint
lib1.unctrl.restype           = ctypes.c_char_p
lib1.is_wintouched.restype    = ctypes.c_bool
lib1.is_linetouched.restype   = ctypes.c_bool
lib1.can_change_color.restype = ctypes.c_bool
lib1.has_colors.restype       = ctypes.c_bool
lib1.has_ic.restype           = ctypes.c_bool
lib1.has_il.restype           = ctypes.c_bool
lib1.has_key.restype          = ctypes.c_bool
lib1.isendwin.restype         = ctypes.c_bool
lib2.new_panel.restype        = ctypes.c_void_p
lib1.derwin.restype           = ctypes.c_void_p
lib1.initscr.restype          = ctypes.c_void_p
lib1.newpad.restype           = ctypes.c_void_p
lib1.newwin.restype           = ctypes.c_void_p
lib1.subpad.restype           = ctypes.c_void_p
lib1.subwin.restype           = ctypes.c_void_p
lib2.panel_above.restype      = ctypes.c_void_p
lib2.panel_below.restype      = ctypes.c_void_p
lib2.panel_userptr.restype    = ctypes.c_void_p
lib2.panel_window.restype     = ctypes.c_void_p
#endregion --- FUNCTION DEFINITIONS (PDC)\(NC) ---



#region  +++ UNIFIED CURSES +++
#region ++ Functions ++
def waddch(scr_id, ch, attr=A_NORMAL):
    """
    Write the character ch in window scr_id.
    """

    return lib1.waddch(scr_id, CCHAR(ch) | attr)


if PDCURSES:
    def wadd_wch(scr_id, wch, attr=A_NORMAL):  # NEEDS_CHECK?
        """
        Write the wide character wch in window scr_id.
        """

        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
        ret = lib1.wadd_wch(scr_id, RCCHAR(wch))
        lib1.wattrset(scr_id, oldattr)
        return ret
        #return lib1.wadd_wch(scr_id, CCHAR(wch) | attr )  # ??? Why no working
elif NCURSES:
    def wadd_wch(scr_id, wch, attr=A_NORMAL):  # NEEDS_CHECK?
        """
        Write the wide character wch in window scr_id.
        """

        return lib1.wadd_wch(scr_id, ctypes.byref(cchar_t(attr, RCCHAR(wch))))


def waddstr(scr_id, cstr, attr="NO_USE"):
    """
    Write the string cstr in window scr_id.
    """

    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.waddstr(scr_id, CSTR(cstr))
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def waddwstr(scr_id, wstr, attr="NO_USE"):
    """
    Write the wide string wstr in window scr_id.
    """

    if wstr == '':
        return None
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    #wstr = ctypes.create_unicode_buffer(wstr)
    ret = lib1.waddwstr(scr_id, wstr)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def waddnstr(scr_id, cstr, n, attr="NO_USE"):
    """
    Write maximum n characters from the string cstr in window scr_id.
    """

    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.waddnstr(scr_id, CSTR(cstr), n)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def wattroff(scr_id, attr):
    """
    Turn off attributes attr of window scr_id.
    """

    return lib1.wattroff(scr_id, attr)


def wattron(scr_id, attr):
    """
    Turn on attributes attr of window scr_id.
    """

    return lib1.wattron(scr_id, attr)


def wattrset(scr_id, attr):
    """
    Set attributes attr of window scr_id.
    """

    return lib1.wattrset(scr_id, attr)


def baudrate():
    """
    Returns the output speed of the terminal.
    """

    return lib1.baudrate()


def beep():
    """
    Sound an audible alarm and, if not possible, flash the screen.
    """

    return lib1.beep()


def copywin(src_id, dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol, overlay_flag):
    """
    If overlay_flag is True apply overlay, otherwise overwrite. A rectangle is specified in window dest_id, via (dminrow, dmincol) and (dmaxrow, dmaxcol), and the upper-left-corner coordinates of window src_id, (sminrow, smincol).
    """

    return lib1.copywin(src_id, dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol, overlay_flag)


def wclear(scr_id):
    """
    Copy blanks to every position in window scr_id and call clearok.
    """

    return lib1.wclear(scr_id)


def wclrtobot(scr_id):
    """
    Erase from the current line to the end of screen in window scr_id.
    """

    return lib1.wclrtobot(scr_id)


def wclrtoeol(scr_id):
    """
    Erase the current line in window scr_id.
    """

    return lib1.wclrtoeol(scr_id)


def clearok(scr_id, yes):
    """
    If yes is True, the next call to wrefresh with window scr_id will clear the screen and redraw.
    """

    return lib1.clearok(scr_id, yes)


def curs_set(visibility):
    """
    Sets the cursor state to invisible (0), normal (1), or very visible (2).
    """

    return lib1.curs_set(visibility)


def wcursyncup(scr_id):
    """
    Update the current position of all window scr_id parents to reflect the current position of window stdscr.
    """

    return lib1.wcursyncup(scr_id)


def def_prog_mode():
    """
    Save the current terminal as the “program” (in curses) state for use by the reset_prog_mode.
    """

    return lib1.def_prog_mode()


def def_shell_mode():
    """
    Save the current terminal as the “shell” (not in curses) state for use by the reset_shell_mode.
    """

    return lib1.def_shell_mode()


def delay_output(ms):
    """
    Insert an ms millisecond pause in output.
    """

    return lib1.delay_output(ms)


def wdelch(scr_id):
    """
    Delete the current character in window scr_id. All characters to the right are moved to the left by one.
    """

    return lib1.wdelch(scr_id)


def wdeleteln(scr_id):
    """
    Delete the current line in window scr_id. All lines below are moved up one line.
    """

    return lib1.wdeleteln(scr_id)


def wbkgd(scr_id, ch, attr=A_NORMAL):
    """
    Set the background ch of window scr_id and apply this setting to every character position.
    """

    return lib1.wbkgd(scr_id, CCHAR(ch) | attr)


def wbkgdset(scr_id, ch, attr=A_NORMAL):
    """
    Set the background ch for window scr_id.
    """

    return lib1.wbkgdset(scr_id, CCHAR(ch) | attr)


def wborder(scr_id, ls=ACS_VLINE, rs=ACS_VLINE, ts=ACS_HLINE, bs=ACS_HLINE,
            tl=ACS_ULCORNER, tr=ACS_URCORNER, bl=ACS_LLCORNER, br=ACS_LRCORNER):
    """
    Draw a box around the edges of window scr_id with attributes ls (left side), rs (right side), ts (top side), bs (bottom side), tl (top left-hand corner), tr (top right-hand corner), bl (bottom left-hand corner), and br (bottom right-hand corner).
    """

    return lib1.wborder(scr_id, ls, rs, ts, bs, tl, tr, bl, br) # same as wborder_set (it supports unicode by default)


def box(scr_id, verch=ACS_VLINE, horch=ACS_HLINE):
    """
    Shorthand for wborder(scr_id, verch, verch, horch, horch, 0, 0, 0, 0).
    """

    return lib1.box(scr_id, verch, horch)


def can_change_color():
    """
    Return True if the programmer can change the colors of the terminal, otherwise return False.
    """

    return bool( lib1.can_change_color() )


def cbreak():
    """
    Make characters typed by the user immediately available.
    """

    return lib1.cbreak()


def wchgat(scr_id, num, attr, color, opts=None):
    """
    Set the attributes attr and color of num many characters in window scr_id. It does not update the current position and does not perform wrapping.
    """

    return lib1.wchgat(scr_id, num, attr, color, None)


def color_content(color_number): # TODO: not working
    """
    Return (r, g, b) of color_number.
    """

    r = ctypes.c_short()
    g = ctypes.c_short()
    b = ctypes.c_short()
    lib1.color_content( color_number, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b))
    return (r.value, g.value, b.value)


if PDCURSES:
    def color_pair(color_number):
        """
        Convert color_number to an attribute.
        """

        return PD_COLOR_PAIR(color_number)
elif NCURSES:
    def color_pair(color_number):
        """
        Convert color_number to an attribute.
        """

        return NC_COLOR_PAIR(color_number)


def COLOR_PAIR(color_number):
    """
    Convert color_number to an attribute.
    """

    return  color_pair(color_number)


def delwin(scr_id):
    """
    Delete window scr_id. It does not erase window scr_id screen image.
    """

    return lib1.delwin(scr_id)


def derwin(srcwin, nlines, ncols, y, x):
    """
    Return a new window with nlines and ncols, positioned at (y, x) relative to the origin of scrwin. The subwindow shares memory with window srcwin, so changes made to one window will affect both.
    """

    return ctypes.c_void_p(lib1.derwin(srcwin, nlines, ncols, y, x))


def doupdate():
    """
    Update the physical screen compared to the virtual screen.
    """

    return lib1.doupdate()


def echo():
    """
    Put getch in echo mode, so characters typed are echoed.
    """

    return lib1.echo()


def wechochar(scr_id, ch, attr=A_NORMAL):
    """
    Equivalent to a call to waddch followed by a call to wrefresh.
    """

    return lib1.wechochar(scr_id, CCHAR(ch) | attr)


def wenclose(scr_id, y, x):
    """
    Return True if the pair (y, x) is enclosed by window scr_id, ortherwise return False.
    """

    return lib1.wenclose(scr_id, y, x)


def endwin():
    """
    Must call endwin for each terminal being used before exiting from curses. If newterm is called more than once for the same terminal, the first terminal referred to must be the last one for which endwin is called.
    """

    return lib1.endwin()


def werase(scr_id):
    """
    Copy blanks to every position in window scr_id.
    """

    return lib1.werase(scr_id)


def erasechar():
    """
    Return the user's current erase character.
    """

    return lib1.erasechar()


def filter():
    """
    Called before initscr or newterm. Causes the following changes at initialization: LINES is set to 1, the capabilities clear, cud1, cud, cup, cuu1, cuu, vpa are disabled, the capability ed is disabled if bce is set, and the home string is set to the value of cr.
    """

    return lib1.filter()

if NCURSES:
    def nofilter():
        """
        Cancel the effect of a preceding filter call.
        """

        return lib1.nofilter()


def flash():
    """
    Flash the screen and, if not possible, sound an audible alarm.
    """

    return lib1.flash()


def flushinp():
    """
    Throw away any typeahead typed by the user that has not yet been read by the program.
    """

    return lib1.flushinp()


def getbegyx(scr_id):	
    """
    Return the origin of the subwindow scr_id relative to the parent window.
    """

    y = lib1.getbegy(scr_id)
    x = lib1.getbegx(scr_id)
    return (y, x)


def wgetch(scr_id):
    """
    Read a character from window scr_id.
    """

    ch = lib1.wgetch(scr_id)
    if ch == -1:
        raise TimeoutError("Time elapsed.")
    return ch


def wget_wch(scr_id): # NEEDS_CHECK? # https://stackoverflow.com/questions/1081456/wchar-t-vs-wint-t
    """
    Read a wide character from window scr_id.
    """

    wint = ctypes.c_uint16()
    lib1.wget_wch(scr_id,ctypes.byref(wint))
    return wint.value


def wgetkey(scr_id, y=-1, x=-1): # NEEDS_CHECK?	
    """
    Read a key from window scr_id after (optional) moving the current position to (y, x). Differently from getch, this function reads escape characters and transforms them into keys.
    """

    if (y == -1) or (x == -1):
        return keyname(wgetch(scr_id))
    return keyname(mvwgetch(scr_id, y, x))


def getmaxyx(scr_id):
    """
    Return the dimensions (height, width) of window scr_id.
    """

    y = lib1.getmaxy(scr_id)
    x = lib1.getmaxx(scr_id)
    return (y, x)


def getmaxy(scr_id):
    """
    Return the height of window scr_id.
    """

    return lib1.getmaxy(scr_id)


def getmaxx(scr_id):
    """
    Return the width of window scr_id.
    """

    return lib1.getmaxx(scr_id)

if PDCURSES:
    def getmouse():
        """
        Read a KEY_MOUSE event data queued in getch and pop the event off the queue.
        """

        m_event = MEVENT()
        lib1.nc_getmouse(ctypes.byref(m_event))  # ? https://github.com/wmcbrine/PDCurses/blob/f1cd4f4569451a5028ddf3d3c202f0ad6b1ae446/pdcurses/mouse.c#L105
        return (m_event.id, m_event.x, m_event.y, m_event.z, m_event.bstate)
elif NCURSES:
    def getmouse():
        """
        Read a KEY_MOUSE event data queued in getch and pop the event off the queue.
        """

        m_event = MEVENT()
        lib1.getmouse(ctypes.byref(m_event))
        return (m_event.id, m_event.x, m_event.y, m_event.z, m_event.bstate)


def getparyx(scr_id): # TODO: not working
    """
    Return the origin of the subwindow scr_id relative to its parent window.
    """

    y = lib1.getpary(scr_id)
    x = lib1.getparx(scr_id)
    return (y, x)


def wgetstr(scr_id):
    """
    Perform a series of calls to getch in window scr_id until a newline is received.
    """

    t_str = ctypes.create_string_buffer(1023)
    lib1.wgetstr(scr_id, ctypes.byref(t_str))
    return t_str.value.decode()


if PDCURSES:
    def getsyx():
        """
        Return the current position of the virtual screen.
        """

        if is_leaveok():
            return (-1, -1)
        curscr = PD_GET_CURSCR()
        return getyx(curscr)
elif NCURSES:
    def getsyx():
        """
        Return the current position of the virtual screen.
        """

        return getyx(stdscr)


def getyx(scr_id):
    """
    Return the current position of window scr_id.
    """

    cy = lib1.getcury(scr_id)
    cx = lib1.getcurx(scr_id)
    return (cy, cx)


def halfdelay(tenths): # TODO: error is -1, so how about actually raising an error in python if that's the ouput?
    """
    Similar to cbreak, make characters typed by the user immediately available. After blocking for tenths tenths of seconds, ERR is returned if nothing has been typed.
    """

    return lib1.halfdelay(tenths)


def has_colors():
    """
    Return True if the terminal has color capabilities, otherwise return False.
    """

    return bool( lib1.has_colors() )


def has_ic():
    """
    Return true if the terminal has insert and delete character capabilities, otherwise return False.
    """

    return bool( lib1.has_ic() )


def has_il():
    """
    Return True if the terminal has insert and delete-line capabilities, otherwise return False.
    """
    return bool( lib1.has_il() )


def has_key(ch): # TODO: maybe not working? Not sure..
    """
    Take a key-code value from the list as in (https://man7.org/linux/man-pages/man3/curs_getch.3x.html) and return True if the current terminal type recognizes a key with that value, otherwise return False.
    """

    return bool( lib1.has_key( CCHAR(ch) ) )


def whline(scr_id, ch, n):
    """
    Draw a horizontal line of maximum n characters ch starting from the current position in window scr_id. The current position is not updated.
    """

    return lib1.whline(scr_id, CCHAR(ch), n)


def idcok(scr_id, flag): # does nothing in PDCURSES
    """
    When the flag is False, the library no longer considers using the hardware insert/delete character feature of terminals so equipped in window scr_id. When the flag is True, it re-enables use of character insertion and deletion. (No effect in Windows)
    """

    return lib1.idcok(scr_id, flag)


def idlok(scr_id, yes): # does nothing in PDCURSES
    """
    When the flag is True, the library considers using the hardware insert/delete line feature of terminals so equipped in window scr_id. When the flag is False, it disables use use of line insertion and deletion. (No effect in Windows)
    """

    return lib1.idlok(scr_id, yes)


def immedok(scr_id, flag):
    """
    When the flag is True, any change in window scr_id image automatically cause a call to wrefresh.
    """

    return lib1.immedok(scr_id, flag)


def winch(scr_id):
    """
    Return the character of type chtype at the current position in window scr_id. If any attributes are set, their values are OR'ed into the value returned.
    """

    return RCCHAR( lib1.winch(scr_id) )


def init_color(color, r, g, b):
    """
    Change the definition of a color.
    """

    return lib1.init_color(color, r, g, b)


def init_pair(number_pair, fg, bg):
    """
    Change the definition of a color-pair.
    """

    return lib1.init_pair(number_pair, fg, bg)


def initscr():
    """
    Determine the terminal type and initializes all library's data structures. It then calls to refresh and returns a pointer to stdscr.
    """

    global stdscr

    stdscr = ctypes.c_void_p(lib1.initscr())
    return stdscr


def winsch(scr_id, ch, attr=A_NORMAL):
    """
    Insert the character ch before the current position in window scr_id. All characters to the right are moved by one.
    """

    return lib1.winsch(scr_id, CCHAR(ch) | attr)


def winsdelln(scr_id, nlines):
    """
    For positive nlines, insert nlines line into window scr_id above the current position. For negative nlines, delete nlines lines.
    """

    return lib1.winsdelln(scr_id, nlines)


def winsstr(scr_id, strn, attr="NO_USE"):
    """
    Insert the string strn before the current position in window scr_id. All characters to the right are moved by one.
    """

    oldattr = 0
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.winsstr(scr_id, CSTR(strn))
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def winsnstr(scr_id, strn, n, attr="NO_USE"):
    """
    Insert at most n characters of the string strn before the current position in window scr_id. All characters to the right are moved by one. If n<=0, the entire string is inserted.
    """

    oldattr = 0
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.winsnstr(scr_id, CSTR(strn), n)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def winstr(scr_id, n=-1):
    """
    Return a string of at most n characters from the current position in window scr_id.
    """

    t_str = ctypes.create_string_buffer(1023)
    lib1.winnstr(scr_id, ctypes.byref(t_str), n)
    return t_str.value.decode()


def isendwin():
    """
    Return True if endwin has been called without subsequent calls to wrefresh, otherwise return False.
    """

    return bool( lib1.isendwin() )


def winsertln(scr_id):
    """
    Insert a line above the current position in window scr_id.
    """

    return lib1.winsertln(scr_id)


def is_linetouched(scr_id, line):
    """
    Return True if the line line in window scr_id was modified since the last call to wrefresh; otherwise return False.
    """

    return bool( lib1.is_linetouched(scr_id, line) )


def is_wintouched(scr_id):
    """
    Return True if window scr_id was modified since the last call to wrefresh; otherwise return False.
    """

    return bool( lib1.is_wintouched(scr_id) )


def keyname(k):
    """
    Return the character string corresponding to the key k.
    """

    key = lib1.keyname(k)
    return key.decode() if key else key


def keypad(scr_id, yes):
    """
    With yes True, enable the keypad of the user's terminal. If enabled, the user can press a function key and wgetch returns a single value representing the function key.
    """

    return lib1.keypad(scr_id, yes)


def killchar():
    """
    Return the user's current line kill character.
    """

    return lib1.killchar()


def get_tabsize():
    """
    Return the size of TAB.
    """

    return ctypes.c_int.in_dll(lib1, "TABSIZE").value


def set_tabsize(size):
    """
    Set the size of TAB.
    """

    return lib1.set_tabsize(size)


if PDCURSES: # here we see the reason why PDCURSES is different, the virtual screen is a separate instance
    def leaveok(scr_id, yes):
        """
        Allow the current position to be left wherever the update happens to leave it.
        """

        global PDC_LEAVEOK

        curscr = PD_GET_CURSCR()
        if scr_id.value == curscr.value:
            PDC_LEAVEOK = yes
        return lib1.leaveok(scr_id, yes)
elif NCURSES:
    def leaveok(scr_id, yes):
        """
        Allow the current position to be left wherever the update happens to leave it.
        """

        return lib1.leaveok(scr_id, yes)


if PDCURSES:
    def is_leaveok():
        """
        Return the value set in leaveok.
        """

        return PDC_LEAVEOK
elif NCURSES:
    def is_leaveok():
        """
        Return the value set in leaveok.
        """

        return bool( lib1.is_leaveok(stdscr) )


def longname():
    """
    Return a pointer to a static area containing a verbose description of the current terminal.
    """

    return lib1.longname().decode()


def meta(yes):
    """
    If yes is False, force the terminal to return 8 significant bits, otherwise 7 significant bits if yes is True.
    """

    return lib1.meta(stdscr, yes) # The argument stdscr is ignored.


# TODO: test again, not sure it works
def mouseinterval(interval):
    """
    Set the maximum time in milliseconds that can elapse between press and release events for them to be recognized as a click. 0 disables click resolution.
    """

    return lib1.mouseinterval(interval)


# TODO: test again, not sure it works
def mousemask(mmask):
    """
    Make mouse events visible. By default, no mouse events are reported.
    """

    return lib1.mousemask(mmask, None)


def wmove(scr_id, y, x):
    """
    Move the position associated with window scr_id to position (y, x). The cursor won't move until refresh is called.
    """

    return lib1.wmove(scr_id, y, x)


def mvwaddch(scr_id, y, x, ch, attr=A_NORMAL):
    """
    Write the character ch in window scr_id at position (y, x).
    """

    return lib1.mvwaddch(scr_id, y, x, CCHAR(ch) | attr)


if PDCURSES:
    def mvwadd_wch(scr_id, y, x, wch, attr=A_NORMAL):
        """
        Write the wide character wch in window scr_id at position (y, x).
        """

        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
        ret = lib1.mvwadd_wch(scr_id, y, x, RCCHAR(wch))
        lib1.wattrset(scr_id, oldattr)
        return ret
elif NCURSES:
    def mvwadd_wch(scr_id, y, x, wch, attr=A_NORMAL):
        """
        Write the wide character wch in window scr_id at position (y, x).
        """

        return lib1.mvwadd_wch(scr_id, y, x, ctypes.byref(cchar_t(attr, RCCHAR(wch))))


def mvwaddstr(scr_id, y, x, cstr, attr="NO_USE"):
    """
    Write the string cstr in window scr_id at position (y, x).
    """

    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.mvwaddstr(scr_id, y, x, CSTR(cstr))
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def mvwaddwstr(scr_id, y, x, wstr, attr="NO_USE"):
    """
    Write the wide string wstr in window scr_id at position (y, x).
    """

    if wstr == '':
        return None
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    #wstr = ctypes.create_unicode_buffer(wstr)
    ret = lib1.mvwaddwstr(scr_id, y, x, wstr)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def mvwaddnstr(scr_id, y, x, cstr, n, attr="NO_USE"):
    """
    Write maximum n characters from the string cstr in window scr_id at position (y, x).
    """

    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.mvwaddnstr(scr_id, y, x, CSTR(cstr), n)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def mvwchgat(scr_id, y, x, num, attr, color, opts=None):
    """
    Set the attributes attr and color of num many characters in window scr_id at position (y, x). It does not update the current position and does not perform wrapping.
    """

    return lib1.mvwchgat(scr_id, y, x, num, attr, color, None)


def mvwdelch(scr_id, y, x):
    """
    Delete the character in window scr_id at position (y, x). All characters to the right are moved to the left by one.
    """

    return lib1.mvwdelch(scr_id, y, x)


if PDCURSES:
    def mvwdeleteln(scr_id, y, x):
        """
        Delete the line in window scr_id at position (y, x). All lines below are moved up one line.
        """

        return lib1.mvwdeleteln(scr_id, y, x)
elif NCURSES:
    def mvwdeleteln(scr_id, y, x):
        """
        Delete the line in window scr_id at position (y, x). All lines below are moved up one line.
        """

        lib1.wmove(scr_id, y, x)
        return lib1.wdeleteln(scr_id)


def mvderwin(scr_id, pary, parx):
    """
    Move the subwindow scr_id by (pary, parx) inside the parent window.
    """

    return lib1.mvderwin(scr_id, pary, parx)


def mvwgetch(scr_id, y, x):
    """
    Move the current position to (y, x) and read a character from window scr_id.
    """

    return lib1.mvwgetch(scr_id, y, x)


def mvwgetstr(scr_id, y, x):
    """
    Perform a series of calls to getch in window scr_id at position (y, x) until a newline is received.
    """

    t_str = ctypes.create_string_buffer(1023)
    lib1.mvwgetstr(scr_id, y, x, ctypes.byref(t_str))
    return t_str.value.decode()


def mvwhline(scr_id, y, x, ch, n):
    """
    Draw a horizontal line of maximum n characters ch starting from position (y, x) in window scr_id. The current position is not updated.
    """

    return lib1.mvwhline(scr_id, y, x, CCHAR(ch), n)


def mvwinch(scr_id, y, x):
    """
    Return the character at position (y, x) in window scr_id. If any attributes are set, their values are OR'ed into the value returned.
    """

    return lib1.mvwinch(scr_id, y, x)


def mvwinsch(scr_id, y, x, ch, attr=A_NORMAL):
    """
    Insert the character ch before position (y, x) in window scr_id. All characters to the right are moved by one.
    """

    return lib1.mvwinsch(scr_id, y, x, CCHAR(ch) | attr)


def mvwinsstr(scr_id, y, x, strn, attr="NO_USE"):
    """
    Insert the string strn before position (y, x) in window scr_id. All characters to the right are moved by one.
    """

    oldattr = 0
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.mvwinsstr(scr_id, y, x, CSTR(strn))
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def mvwinsnstr(scr_id, y, x, strn, n, attr="NO_USE"):
    """
    Insert at most n characters of the string strn before position (y, x) in window scr_id. All characters to the right are moved by one. If n<=0, the entire string is inserted.
    """

    oldattr = 0
    if attr != "NO_USE":
        oldattr = lib1.getattrs(scr_id)
        lib1.wattrset(scr_id, attr)
    ret = lib1.mvwinsnstr(scr_id, y, x, CSTR(strn), n)
    if attr != "NO_USE":
        lib1.wattrset(scr_id, oldattr)
    return ret


def mvwinstr(scr_id, y, x, n=-1):
    """
    Return a string of at most n characters from position (y, x) in window scr_id.
    """

    t_str = ctypes.create_string_buffer(1023)
    lib1.mvwinnstr(scr_id, y, x, ctypes.byref(t_str), n)
    return t_str.value.decode()


def mvwinwstr(scr_id, y, x, n=-1):
    """
    Return a wide string of maximum n characters from position (y, x) in window scr_id.
    """

    t_str = ctypes.create_unicode_buffer(2046) # not sure at all about the 2046 but it works? sorry for that
    if n ==-1:
        lib1.mvwinwstr(scr_id, y, x, ctypes.byref(t_str))
    else:
        lib1.mvwinnwstr(scr_id, y, x, ctypes.byref(t_str), n)
    return t_str.value


def mvwvline(scr_id, y, x, ch, n):
    """
    Draw a vertical line of maximum n characters ch starting at position (y, x) in window scr_id. The current position is not updated.
    """

    return lib1.mvwvline(scr_id, y, x, CCHAR(ch), n)


def mvwin(scr_id, y, x):
    """
    Move window scr_id so that the upper left-hand corner is at position (y, x).
    """

    return lib1.mvwin(scr_id, y, x)


def napms(ms):
    """
    Sleep for ms milliseconds.
    """

    return lib1.napms(ms)


def newpad(nlines, ncols):
    """
    Return a new pad data structure with nlines lines and ncols columns.
    """

    return ctypes.c_void_p(lib1.newpad(nlines, ncols))


def newwin(nlines, ncols, y, x):
    """
    Return a new window with nlines lines and ncols columns, whose upper left-hand corner is at (y, x).
    """

    return ctypes.c_void_p(lib1.newwin(nlines, ncols, y, x))


def nl():
    """
    Enable translation of the return key into newline on input.
    """

    return lib1.nl()


def nocbreak():
    """
    Return the terminal to normal (cooked) mode. The tty driver buffers typed characters until a newline is typed.
    """

    return lib1.nocbreak()


def nodelay(scr_id, yes):
    """
    Cause getch to be a non-blocking call.
    """

    return lib1.nodelay(scr_id, yes)


def noecho():
    """
    Disable echo mode for getch, so characters typed are not echoed.
    """

    return lib1.noecho()


def nonl():
    """
    Disable translation of the return key into newline on input.
    """

    return lib1.nonl()


def noqiflush():
    """
    Normal flush of input and output queues associated with the INTR, QUIT and SUSP characters will not be done.
    """

    return lib1.noqiflush()


def noraw():
    """
    Characters typed are not immediately passed through to the user program. Used to disable raw mode.
    """

    return lib1.noraw()


def notimeout(scr_id, yes):
    """
    If yes is True, disable the timer in window scr_id that the function wgetch waits for when interpreting an escape sequence. If yes is False, restore the timer.
    """

    return lib1.notimeout(scr_id, yes)


def wnoutrefresh(scr_id):
    """
    Copy window scr_id to the virtual screen. To be used followed by doupdate.
    """

    return lib1.wnoutrefresh(scr_id)


def overlay(src_id, dest_id):
    """
    Overlay src_id on top of dest_id in a non-destructive way.
    """

    return lib1.overlay(src_id, dest_id)


def overwrite(src_id, dest_id):
    """
    Overwrite src_id on top of dest_id in a destructive way.
    """

    return lib1.overwrite(src_id, dest_id)


def pair_content(number_pair):
    """
    Return what colors pair_number consists of.
    """

    fg = ctypes.c_short()
    bg = ctypes.c_short()
    lib1.pair_content(number_pair, ctypes.byref(fg), ctypes.byref(bg))
    return (fg.value, bg.value)


if PDCURSES:
    def pair_number(attr):
        """
        Extract the color value from attrs.
        """

        return PD_PAIR_NUMBER(attr)
elif NCURSES:
    def pair_number(attr):
        """
        Extract the color value from attrs.
        """

        return NC_PAIR_NUMBER(attr)

def prefresh(scr_id, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol):
    """
    Similar to wrefresh but for pads instead of windows. pminrow and pmincol specify the upper left-hand corner of the rectangle to be displayed in the pad. sminrow, smincol, smaxrow, and smaxcol specify the edges of the rectangle to be displayed on the screen.
    """

    return lib1.prefresh(scr_id, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol) # TODO: fix | https://github.com/wmcbrine/PDCurses/pull/121 # NEEDS_CHECK?


def putp(cstring):
    # TODO: I don't fully understand what this function does
    return lib1.putp(CSTR(cstring))


if PDCURSES:
    # TODO
    def putwin(scr_id, file):	# TODO: https://github.com/wmcbrine/PDCurses/search?q=putwin # NEEDS_CHECK?
        raise Exception("UNICURSES_PUTWIN: 'putwin' is unavailable under Windows at this momment!")
elif NCURSES:
    # TODO
    pass


if PDCURSES:
    # TODO
    def getwin(file):   # THIS IS NOT CROSS-PLATFORM YET, AVOID IF POSSIBLE # NEEDS_CHECK?
        raise Exception("UNICURSES_GETWIN: 'getwin' is unavailable under Windows!")
elif NCURSES:
    # TODO
    pass


def qiflush():
    """
    Normal flush of input and output queues associated with the INTR, QUIT and SUSP characters are read.
    """

    return lib1.qiflush()


def raw():
    """
    Characters typed are immediately passed through to the user program. Differently from cbreak, the interrupt, quit, suspend, and flow control characters are all passed through uninterpreted,
    """

    return lib1.raw()


def wredrawln(scr_id, beginning, nlines):
    """
    Indicate the library that nlines lines in window scr_id, starting from beginning line, should be discarded before anything is written over them.
    """

    return lib1.wredrawln(scr_id, beginning, nlines)


def redrawwin(scr_id):
    """
    Indicate to the library that window scr_id should be discarded before anything is written over it.
    """

    return lib1.redrawwin(scr_id)


def wrefresh(scr_id):
    """
    Must be called to get window scr_id to output to the terminal.
    """

    return lib1.wrefresh(scr_id)


def reset_prog_mode():
    """
    Restore the current terminal to “program” (in curses) state.
    """

    return lib1.reset_prog_mode()


def reset_shell_mode():
    """
    Restore the current terminal to “shell” (not in curses) state.
    """

    return lib1.reset_shell_mode()


def wresize(scr_id, nlines, ncols):
    """
    Reallocate storage for window scr_id to adjust its dimensions to nlines lines and ncols columns.
    """

    return lib1.wresize(scr_id, nlines, ncols)


def resize_term(nlines, ncols):
    """
    Attempt to resize all windows to nlines lines and ncols columns, recursively adjusting subwindows by keeping them within the updated parent window's limits.
    """

    return lib1.resize_term(nlines, ncols)	


def wscrl(scr_id, nlines=1):
    """
    If nlines is positive, scroll window scr_id up, otherwise scroll the window down. The current position is not updated.
    """

    return lib1.wscrl(scr_id, nlines)


def scrollok(scr_id, flag):
    """
    When the cursor of window scr_id is moved off the edge as a result of adding lines or characters, if flag is False the cursor is left on the bottom line, otherwise if flag is True, window scr_id is scrolled up one line.
    """

    return lib1.scrollok(scr_id, flag)


def is_scrollok(scr_id):
    """
    Return the value set in scrollok.
    """

    return bool( lib1.is_scrollok(scr_id) )


def wsetscrreg(scr_id, top, bottom):
    """
    Set window scr_id scrolling region margins between top line and bottom line.
    """

    return lib1.wsetscrreg(scr_id, top, bottom)


if PDCURSES:
    # TODO check why it creates a variable that is garbage collected on function return
    # even if we want to keep this extra variable, why not simply calling leaveok?
    def setsyx(y, x):
        """"
        If y == x == -1 leaveok is set, otherwise set the virtual screen cursor to y, x.
        """

        global PDC_LEAVEOK

        if y == x == -1:
            PDC_LEAVEOK = True
        else:
            PDC_LEAVEOK = False
        return lib1.setsyx(y, x)
elif NCURSES:
    def setsyx(y, x):
        """"
        If y == x == -1 leaveok is set, otherwise set the virtual screen cursor to y, x.
        """

        if y == x == -1:
            leaveok(stdscr, True)
        else:
            leaveok(stdscr, False)
            move(y, x)


def setupterm(termstr, fd):
    """
    Read in the terminfo database, initializing the terminfo structures via term (terminal type, a string) and fd (file descriptor). Does not set up the output virtualization structures used by the library.
    """

    return lib1.setupterm(termstr, fd, None)


def wstandend(scr_id):
    """
    Same as wattrset(scr_id, A_NORMAL), turn off all attributes in window scr_id.
    """

    return lib1.wstandend(scr_id)


def wstandout(scr_id):
    """
    Same as wattron(scr_id, A_STANDOUT).
    """

    return lib1.wstandout(scr_id)


def start_color():
    """
    Must be called if want to use colors in the program.
    """

    return lib1.start_color()


def subpad(scrwin, nlines, ncols, y, x):
    """
    Return a pointer to a subwindow, positioned at (y, x) and with nlines lines and ncols columns, within a pad.
    """

    return ctypes.c_void_p(lib1.subpad(scrwin, nlines, ncols, y, x))


def subwin(srcwin, nlines, ncols, y, x):
    """
    Return a new window with nlines and ncols, positioned at (y, x). The subwindow shares memory with window srcwin, so changes made to one window will affect both.
    """

    return ctypes.c_void_p(lib1.subwin(srcwin, nlines, ncols, y, x))


def wsyncdown(scr_id):
    """
    Touch each location in window scr_id that has been touched in any of its ancestor windows.
    """

    return lib1.wsyncdown(scr_id)


def syncok(scr_id, flag):
    """
    If flag is True, then wsyncup(scr_id) is called automatically whenever there is a change in the window.
    """

    return lib1.syncok(scr_id, flag)


def is_syncok(scr_id):
    """
    Return the value set in syncok(scr_id).
    """

    return bool( lib1.is_syncok(scr_id) )


def wsyncup(scr_id):
    """
    Call touchwin to all parents of window scr_id.
    """

    return lib1.wsyncup(scr_id)


def termattrs():
    """
    Return a logical OR of all video attributes supported by the terminal using A_ constants.
    """

    return lib1.termattrs()


def termname():
    """
    Return the terminal name used by setupterm.
    """

    return lib1.termname().decode()


if NCURSES:
    def tigetflag(capname):
        """
        Return the value of the capability corresponding to the terminfo capname.
        """

        return lib1.tigetflag(CSTR(capname))


    def tigetnum(capname):
        """
        Return the value of the capability corresponding to the terminfo capname.
        """

        return lib1.tigetnum(CSTR(capname))


    def tigetstr(capname):
        """
        Return the value of the capability corresponding to the terminfo capname.
        """

        return lib1.tigetstr(CSTR(capname))


def wtimeout(scr_id, delay):
    """
    Set blocking or non-blocking reads for window scr_id. If delay<0, waits indefinitely for input (blocking). If delay>=0, returns ERR if there is no input after delay milliseconds (non-blocking).
    """

    return lib1.wtimeout(scr_id, delay)


def wtouchline(scr_id, start, nlines, changed=1):
    """
    Make nlines lines in window scr_id, starting at line start, look as if they have changed (1) or have not changed (0) since the last call to wrefresh(scr_id).
    """

    return lib1.wtouchln(scr_id, start, nlines, changed)


def touchwin(scr_id):
    """
    Make window scr_id look as if it changed since the last call to wrefresh(scr_id).
    """

    return lib1.touchwin(scr_id)


def tparm(strn, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=0, p8=0, p9=0):
    """
    Instantiate the expression string with parameters pi.
    """

    return lib1.tparm(CSTR(strn), p1, p2, p3, p4, p5, p6, p7, p8, p9)


def typeahead(fd):
    """
    Specify that the file descriptor fd is to be used to check for typeahead. If fd is -1, no typeahead checking is done.
    """

    return lib1.typeahead(fd)


def wvline(scr_id, ch, n):
    """
    Draw a vertical line of maximum n characters ch starting at the current position in window scr_id. The current position is not updated.
    """

    return lib1.wvline(scr_id, CCHAR(ch), n)


def unctrl(ch):
    """
    Return a string which is a printable representation of the character ch, ignoring attributes.
    """

    return lib1.unctrl( CCHAR(ch) ).decode()


# TODO: fix this, the problem is that wunctrl needs cchar_t as function argument, which is internal type of ncurses
def wunctrl(ch):
    """
    Return a string which is a printable representation of the wide character ch, ignoring attributes.
    """
    
    return lib1.wunctrl( ch )


if PDCURSES:
    def ungetch(ch):
        """
        Place ch back onto the input queue to be returned by the next call to getch/wgetch.
        """

        return lib1.PDC_ungetch( CCHAR(ch) )
elif NCURSES:
    def ungetch(ch):
        """
        Place ch back onto the input queue to be returned by the next call to getch/wgetch.
        """

        return lib1.ungetch( CCHAR(ch) )


def ungetmouse(id_mouse, x, y, z, bstate):
    """
    Pushes a KEY_MOUSE event onto the input queue. This event has the associates input data.
    """

    m_event = MEVENT()
    m_event.id = id_mouse
    m_event.x = x
    m_event.y = y
    m_event.z = z
    m_event.bstate = bstate
    return lib1.ungetmouse(ctypes.byref(m_event))


def untouchwin(scr_id):
    """
    Make window scr_id look as if it has not changed since the last call to wrefresh(scr_id).
    """

    return lib1.untouchwin(scr_id)


def use_default_colors():
    """
    Tell the library to assign terminal default foreground/background colors to color number -1.
    """

    return lib1.use_default_colors()


def use_env(flag):
    """
    Must be called before initscr or newterm are called. It modifies the way the library treats environment variables when determining the screen size. (No effect in Windows)
    """

    return lib1.use_env(flag)
#endregion -- Functions --


#region ++ REGULAR\MACRO FUNCTIONS THAT DO NOT TAKE A WINDOW AS AN ARGUMENT ++
def attroff(attr):
    """
    Turn off attributes attr.
    """

    return wattroff(stdscr, attr)


def attron(attr):
    """
    Turn on attributes attr.
    """

    return wattron(stdscr, attr)


def attrset(attr):
    """
    Set attributes attr.
    """

    return wattrset(stdscr, attr)


def clear():
    """
    Copy blanks to every position and call clearok.
    """

    return wclear(stdscr)


def getch():
    """
    Read a character.
    """

    return wgetch(stdscr)


def get_wch():
    """
    Read a wide character.
    """

    return wget_wch(stdscr)


def mvinsnstr(y, x, strn, n, attr="NO_USE"):
    """
    Insert at most n characters of the string strn before position (y, x). All characters to the right are moved by one. If n<=0, the entire string is inserted.
    """

    return mvwinsnstr(stdscr, y, x, strn, n, attr)


def insnstr(strn, n, attr="NO_USE"):
    """
    Insert at most n characters of the string strn before the current position. All characters to the right are moved by one. If n<=0, the entire string is inserted.
    """

    return winsnstr(stdscr, strn, n, attr)


def insch(ch, attr=A_NORMAL):
    """
    Insert the character ch before the current position. All characters to the right are moved by one.
    """

    return winsch(stdscr, ch, attr)


def refresh():
    """
    Must be called to get stdscr to output to the terminal.
    """

    return wrefresh(stdscr)


def border(ls=ACS_VLINE, rs=ACS_VLINE, ts=ACS_HLINE, bs=ACS_HLINE, tl=ACS_ULCORNER, tr=ACS_URCORNER, bl=ACS_LLCORNER, br=ACS_LRCORNER):
    """
    Draw a box around the edges with attributes ls (left side), rs (right side), ts (top side), bs (bottom side), tl (top left-hand corner), tr (top right-hand corner), bl (bottom left-hand corner), and br (bottom right-hand corner).
    """

    return wborder(stdscr, ls, rs, ts, bs, tl, tr, bl, br)


def bkgd(ch, attr=A_NORMAL):
    """
    Set the background ch and apply this setting to every character position.
    """

    return wbkgd(stdscr, ch, attr)


def bkgdset(ch, attr=A_NORMAL):
    """
    Set the background ch.
    """

    return wbkgdset(stdscr, ch, attr)


def erase():
    """
    Copy blanks to every position.
    """

    return werase(stdscr)


def timeout(delay):
    """
    Set blocking or non-blocking reads. If delay<0, blocking read is used, meaning waits indefinitely for input. If delay=0, non-blocking read is used. If delay>0, read blocks for delay milliseconds. If delay>=0, and returns ERR if there is no input after delay.
    """

    return wtimeout(stdscr, delay)


def hline(ch, n):
    """
    Draw a horizontal line of maximum n characters ch starting at the current position. The current position is not updated.
    """

    return whline(stdscr, ch, n)


def vline(ch, n):
    """
    Draw a vertical line of maximum n characters ch starting at the current position. The current position is not updated.
    """

    return wvline(stdscr, ch, n)


def mvhline(y, x, ch, n):
    """
    Draw a horizontal line of maximum n characters ch starting at position (y, x). The current position is not updated.
    """

    return mvwhline(stdscr, y, x, ch, n)


def mvvline(y, x, ch, n):
    """
    Draw a vertical line of maximum n characters ch starting at position (y, x). The current position is not updated.
    """

    return mvwvline(stdscr, y, x, ch, n)


def scroll(nlines=1):
    """
    If line is positive, scroll window stdscr up, otherwise scroll the window down. The current position is not updated.
    """

    return wscrl(stdscr, nlines)


def setscrreg(top, bottom):
    """
    Set scrolling region margins between top line and bottom line.
    """

    return wsetscrreg(stdscr, top, bottom)


def delch():
    """
    Delete the current character. All characters to the right are moved to the left by one.
    """

    return wdelch(stdscr)


def mvdelch(y, x):
    """
    Delete the character at position (y, x). All characters to the right are moved to the left by one.
    """

    return mvwdelch(stdscr, y, x)


def move(y, x):
    """
    Move the position in window stdscr to position (y, x). The cursor won't move until refresh is called.
    """

    return wmove(stdscr, y, x)


def insertln():
    """
    Insert a line above the current position.
    """

    return winsertln(stdscr)


def insdelln(nlines):
    """
    For positive nlines, insert nlines line above the current position. For negative nlines, delete nlines lines.
    """

    return winsdelln(stdscr, nlines)


def inch():
    """
    Return the character of type chtype. If any attributes are set, their values are OR'ed into the value returned.
    """

    return winch(stdscr)


def mvinch(y, x):
    """
    Return the character of type chtype at position (y, x). If any attributes are set, their values are OR'ed into the value returned.
    """

    return mvwinch(stdscr, y, x)


def clrtobot():
    """
    Erase from the line of the current position to the end of screen.
    """

    return wclrtobot(stdscr)


def clrtoeol():
    """
    Erase the current line.
    """

    return wclrtoeol(stdscr)


def mvgetch(y, x):
    """
    Move the current position to (y, x) and read a character.
    """

    ch = mvwgetch(stdscr, y, x)
    if ch == -1:
        raise TimeoutError("Time elapsed")
    return ch


def addch(ch, attr=A_NORMAL):
    """
    Write the character ch.
    """

    return waddch(stdscr, ch, attr)


def mvaddch(y, x, ch, attr=A_NORMAL):
    """
    Write the character ch at position (y, x).
    """

    return mvwaddch(stdscr, y, x, ch, attr)


def add_wch(wch, attr=A_NORMAL):
    """
    Write the wide character wch.
    """

    return wadd_wch(stdscr, wch, attr)


def mvadd_wch(y, x, wch, attr=A_NORMAL):
    """
    Write the wide character wch at position (y, x).
    """

    return mvwadd_wch(stdscr, y, x, wch, attr)


def addstr(cstr, attr="NO_USE"):
    """
    Write the string cstr.
    """

    return waddstr(stdscr, cstr, attr)


def addwstr(wstr, attr="NO_USE"):
    """
    Write the wide string wstr.
    """

    return waddwstr(stdscr, wstr, attr)


def mvaddstr(y, x, cstr, attr="NO_USE"):
    """
    Write the string cstr at position (y, x).
    """

    return mvwaddstr(stdscr, y, x, cstr, attr)


def mvaddwstr(y, x, wstr, attr="NO_USE"):
    """
    Write the wide string wstr at position (y, x).
    """

    return mvwaddwstr(stdscr, y, x, wstr, attr)


def addnstr(cstr, n, attr="NO_USE"):
    """
    Write maximum n characters from the string cstr.
    """

    return waddnstr(stdscr, cstr, n, attr)


def mvaddnstr(y, x, cstr, n, attr="NO_USE"):
    """
    Write maximum n characters from the string cstr at position (y, x).
    """

    return mvwaddnstr(stdscr, y, x, cstr, n, attr)


def insstr(cstr, attr="NO_USE"):
    """
    Insert the string strn before the current position. All characters to the right are moved by one.
    """

    return winsstr(stdscr, cstr, attr)


def mvinsstr(y, x, cstr, attr="NO_USE"):
    """
    Insert the string strn before position (y, x). All characters to the right are moved by one.
    """

    return mvwinsstr(stdscr, y, x, cstr, attr)


def echochar(ch, attr=A_NORMAL):
    """
    Equivalent to a call to addch followed by a call to refresh.
    """

    return wechochar(stdscr, ch, attr)


def standout():
    """
    Same as attron(A_STANDOUT).
    """

    return wstandout(stdscr)


def standend():
    """
    Same as attrset(A_NORMAL) or attrset(0), turn off all attributes.
    """

    return wstandend(stdscr)


def chgat(num, attr, color, opts=None):
    """
    Set the attributes attr and color of num many characters. It does not update the current position and does not perform wrapping.
    """

    return wchgat(stdscr, num, attr, color, opts)


def mvchgat(y, x, num, attr, color, opts=None):
    """
    Set the attributes attr and color of num many characters at position (y, x). It does not update the current position and does not perform wrapping.
    """

    return mvwchgat(stdscr, y, x, num, attr, color, opts)


def deleteln():
    """
    Delete the current line. All lines below are moved up one line.
    """

    return wdeleteln(stdscr)


def mvdeleteln(y, x):
    """
    Delete the line at position (y, x). All lines below are moved up one line.
    """

    return mvwdeleteln(stdscr, y, x)


def enclose(y, x):
    """
    Return True if the pair (y, x) is enclosed by window stdscr, ortherwise return False.
    """

    return wenclose(stdscr, y, x)


def getstr():
    """
    Perform a series of calls to getch until a newline is received.
    """

    return wgetstr(stdscr)


def mvgetstr(y, x):
    """
    Perform a series of calls to getch at position (y, x) until a newline is received.
    """

    return mvwgetstr(stdscr, y, x)


def instr(n=-1):
    """
    Return a string of at most n characters at the current position.
    """

    return winstr(stdscr, n)


def mvinstr(y, x, n=-1):
    """
    Return a string of at most n characters at position (y, x).
    """

    return mvwinstr(stdscr, y, x, n)


def mvinwstr(y, x, n=-1):
    """
    Return a wide string of maximum n characters at position (y, x).
    """

    return mvwinwstr(stdscr, y, x, n)


def touchline(y, x, changed=1):
    """
    Make nlines lines, starting at line start, look as if they have changed (=1) or have not changed (=0) since the last call to refresh.
    """

    return wtouchline(stdscr, y, x, changed)


def mvinsch(y, x, ch, attr=A_NORMAL):
    """
    Insert the character ch before position (y, x). All characters to the right are moved by one.
    """

    return mvwinsch(stdscr, y, x, ch, attr)


def redrawln(beg, num):
    """
    Indicate the library that num many lines, starting from beg line, should be discarded before anything is written over them.
    """

    return wredrawln(stdscr, beg, num)


def syncdown():
    """
    Touch each location in window stdscr that has been touched in any of its ancestor windows.
    """

    return wsyncdown(stdscr)


def syncup():
    """
    Call touchwin to all parents of window stdscr.
    """

    return wsyncup(stdscr)


def getkey(y=-1, x=-1):
    """
    Read a key after (optional) moving the current position to (y, x). Differently from getch, this function reads escape characters and transforms them into keys.
    """

    return wgetkey(stdscr, y, x)


def wrapper(function, *args, **kwargs):
    """
    Call to initscr and execute function with positional and keyword parameters, respectively, *args and **kwargs. If error is raised, call to endwin before raising the error, preventing the terminal from becoming unusable.
    """

    initscr()
    try:
        return function(stdscr, *args, **kwargs)
    except Exception as exception:
        raise exception
    finally:
        endwin()
#endregion -- REGULAR\MACRO FUNCTIONS THAT DO NOT TAKE A WINDOW AS AN ARGUMENT --


#region ++ UNIFIED CURSES: PANEL MODULE ++
def panel_above(pan_id):
    """
    Return a pointer to the panel above pan_id. If pan_id==0, return a pointer to the bottom panel in the stack.
    """

    return ctypes.c_void_p(lib2.panel_above(pan_id))


def panel_below(pan_id):
    """
    Return a pointer to the panel below pan_id. If pan_id==0, return a pointer to the top panel in the stack.
    """

    return ctypes.c_void_p(lib2.panel_below(pan_id))


def bottom_panel(pan_id):
    """
    Put panel pan_id at the bottom of all panels.
    """

    return lib2.bottom_panel(pan_id)


def del_panel(pan_id):
    """
    Remove panel pan_id from the stack.
    """

    return lib2.del_panel(pan_id)


def panel_hidden(pan_id):
    """
    Return True if panel pan_id is in the panel stack, otherwise return False.
    """

    mode = lib2.panel_hidden(pan_id)
    return mode == OK


def hide_panel(pan_id):
    """
    Remove the panel pan_id from the panel stack and hide it from view.
    """

    return lib2.hide_panel(pan_id)


def move_panel(pan_id, y, x):
    """
    Move panel pan_id's window so that its upper-left corner is at y, x.
    """

    return lib2.move_panel(pan_id, y, x)


def new_panel(scr_id):
    """
    Return a new panel structure which is associated with window scr_id and placed on the top of the stack.
    """

    return ctypes.c_void_p(lib2.new_panel(scr_id))


def replace_panel(pan_id, win):
    """
    Replace the window of panel pan_id with window scr_id.
    """

    return lib2.replace_panel(pan_id, win)


def set_panel_userptr(pan_id, obj):
    """
    Set the panel pan_id user pointer.
    """

    return lib2.set_panel_userptr(pan_id, obj)


def show_panel(pan_id):
    """
    Make a hidden panel pan_id visible by placing it on top of the panel stack.
    """

    return lib2.show_panel(pan_id)


def top_panel(pan_id):
    """
    Put a visible panel pan_id on top of all panels in the stack.
    """

    return lib2.top_panel(pan_id)


def update_panels():
    """
    Refresh the virtual screen to reflect the relations between the panels in the stack, but does not call doupdate.
    """

    return lib2.update_panels()


def panel_userptr(pan_id):
    """
    Return the user pointer for a given panel pan_id.
    """

    return ctypes.c_void_p(lib2.panel_userptr(pan_id))


def panel_window(pan_id):
    """
    Return a pointer to the window of the panel pan_id.
    """

    return ctypes.c_void_p(lib2.panel_window(pan_id))
#endregion -- UNIFIED CURSES: PANEL MODULE --
#endregion --- UNIFIED CURSES ---


# TODO: Python2 CHECK https://stackoverflow.com/questions/4843173/how-to-check-if-type-of-a-variable-is-string

#1 https://stackoverflow.com/a/43924525/11465149
