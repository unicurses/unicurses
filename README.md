UNICURSES (C) 2010 by Michael Kamensky (Agetian) | Maintainer, George Chousos 2021 | [v2.1.3](./changelog.md)  
Released as Free Software under the terms of General Public License (GPL) v3


# UniCurses
Unified Curses Wrapper for Python on Windows, FreeBSD, Linux, and Mac OS X


## What is UniCurses?
UniCurses is a Python module that is aimed at providing the Curses functionality on all operating systems *(MS Windows, FreeBSD, Linux, and Mac OS X)* using a unified set of commands that are syntactically close to the native C Curses functions. UniCurses strives to be as platform-independent as possible, not only by working on all operating systems *(as opposed to the original `curses` module which does not work on Microsoft Windows)* but also by ensuring compatibility both with the older (v2.x) and the newer (v3.x) versions of Python.
UniCurses is compatible with any Python distribution starting with version 2.6.1, including the newly released v2.7 and all the versions released so far in the Python 3 line, including v3.0.x and v3.1.x.

On Microsoft Windows, UniCurses operates by wrapping a curses library known as `Public Domain Curses`, or PDCurses. The dynamic link library for PDCurses is called `pdcurses.dll`. UniCurses is compatible with all flavors of PDCurses, including:

- The standard terminal PDCurses *([pdcdll](https://github.com/unicurses/unicurses/tree/master/unicurses/64%20bit%20binaries/pdcdll))*.
- The SDL PDCurses running in a fake terminal *([pdcdlls](https://github.com/unicurses/unicurses/tree/master/unicurses/64%20bit%20binaries/pdcdlls))*.
- The PDCurses with wide-character (Unicode) support *([pdcdllw](https://github.com/unicurses/unicurses/tree/master/unicurses/64%20bit%20binaries/pdcdllw))*.
- The PDCurses with wide-character (Unicode)/UTF-8 support *([pdcdllu](https://github.com/unicurses/unicurses/tree/master/unicurses/64%20bit%20binaries/pdcdllu))*.

Depending on whether you want your applications to run in a real Windows terminal window or in an emulated fake SDL window you can either use one of the common ones or the SDL one.

if you want to experiment with or use a newer version of PDCurses, you can build your own binaries by downloading the source code from the official link below:
http://pdcurses.sourceforge.net

NOTE: While it may be possible to use UniCurses with an older version of Python (v2.6.1) or PDCurses (v3.4) than officially listed as compatible, it has not been tested with such versions of software and as such it's impossible to guarantee that your configuration will work correctly or that you would not have to take extra steps and install additional packages in order to make your configuration work at least in part. It's highly recommended that you upgrade to the latest versions of Python and PDCurses before you install and start using UniCurses.


## Installing UniCurses
## `pip3 install uni-curses`
^ if this won't work and you get `ModuleNotFoundError` try specifying the python version like:

```terminal
python3.9 -m pip install uni-curses
```

or if you want to use the latest release, download the files from this repository, open your terminal and cd/navigate to the folder and then execute the below:
```terminal
pip3 install .
```


## Importing UniCurses
```python
from unicurses import *
```

OR:

```python
import unicurses
```

It's recommended that you use the first form of the expression so you do not need to precede each curses command in your program with the `unicurses` prefix to refer to the proper namespace.
NOTE: If importing UniCurses is unsuccessful, you will be presented with a message describing the cause of failure and your program will terminate. The most common cause is the absence of the PDCurses dynamic link library in the program folder while running on Microsoft Windows. Correct the problem and try again.
HINT: In order to make sure that UniCurses works correctly on your platform, run the test scripts that come bundled with the UniCurses package (many of them are ports of examples from the awesome "NCURSES Programming HOWTO" by Pradeep Padala). They should all run successfully and not crash with an error message.


## Using UniCurses
While UniCurses tries to stay as faithful to the original C syntax of curses functions as possible, there are certain important differences and peculiarities that you must be aware of when writing programs using UniCurses.
First of all, the function used to initialize curses (initscr) must be called in a special way with an assignment to a variable named `stdscr`. Therefore, instead of just calling `initscr()` you must use the following expression verbatim:

```python
stdscr = initscr()
```

In case you do not follow the above-mentioned convention and do not assign the result of initscr to the variable stdscr, or change the name of the variable from stdscr to anything else, your script or program will fail to work properly and will terminate with an exception. Therefore:

```python
initscr()           # This will NOT work
myscr = initscr()   # This will NOT work
stdscr = initscr()  # This will work correctly
```

After the curses is initialized with an expression above, you can use any of the functions provided by UniCurses in a manner similar to the way you would use them with any other standard curses implementation, such as NCurses or PDCurses. Please take a look at the example test scripts (`test_*.py`) and read the Curses manuals, such as the NCurses HOWTO, in order to learn about how to work with curses.


## Getting started
* ***Projects made with UniCurses:***
* * [unicurses demos](https://github.com/unicurses/unicurses/tree/master/demos)
* * [An interactive cellular automaton](https://github.com/lifesci/deerlang)
* * [A terminal-based file manager](https://github.com/GiorgosXou/TUIFIManager)
* ***Books (NCURSES):*** 
* * [Programmer's Guide to NCurses](https://books.google.gr/books?id=Htff8VRO-UEC&printsec=frontcover&hl=el&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false)
* ***Extra Resources:***
* * ***NCurses:***
* * * [Repository](https://github.com/mirror/ncurses)
* * * [Here you can search for functions too](https://linux.die.net/)
* * ***PDCurses:***
* * * [Repository](https://github.com/wmcbrine/PDCurses)
* * * [How to Build and\or Install PDCurses](https://stackoverflow.com/a/69632679/11465149)


Functions provided by UniCurses
-------------------------------

Here is a list of Curses functions that are provided by UniCurses. Most of them use the same syntax as their Ncurses/PDCurses counterparts, some functions are similar to the ones used in the `curses` module in Python (on Linux/Mac OS X), and som functions are specific to Unicurses. The differences in syntax from the standard Ncurses/PDCurses, as well as portability issues, will in most cases be noted separately.
NOTE 1: Optional parameters will be listed in square brackets.
NOTE 2: If you use any functions that are listed as not cross-platform, your program or script will not be compatible with all the operating systems and may crash on systems that are not compatible. Try to avoid using non-crossplatform functions in your scripts and programs if possible!

The functions that are cross-platform and safe to use:

```python
addch(ch, [attr])
addnstr(str, n, [attr])
addstr(str, [attr])
attroff(attr)
attron(attr)
attrset(attr)
baudrate()
beep()
bkgd(ch, [attr])
bkgdset(ch, [attr])
border([ls, rs, ts, bs, tl, tr, bl, br])
box(WINDOW, [verch], [horch])
can_change_color()
cbreak()
chgat(num, attr, color, [opts])  # NOTE: 'opts' is unused in UniCurses
clear()
clearok(WINDOW, yes)
clrtobot()
clrtoeol()
color_content(color_number) # NOTE: this function returns a tuple: (r, g, b)
color_pair(color_number)
copywin(src_id, dest_id, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol, overlay)
curs_set(visibility)
cursyncup(WINDOW)
def_prog_mode()
def_shell_mode()
delay_output(ms
delch()
deleteln()
delwin(WINDOW)
derwin(srcwin, nlines, ncols, begin_y, begin_x)
doupdate()
echo()
echochar(ch, [attr])
enclose(y, x)
endwin()
erase()
erasechar()
filter()
flash()
flushinp()
getbegyx(WINDOW) # NOTE: this function returns a tuple: (y, x)
getch()
getkey([y, x])
getmaxyx(WINDOW) # NOTE: this function returns a tuple: (y, x)
getmouse() # NOTE: this function returns a tuple: (id, x, y, z, bstate)
getparyx(WINDOW) # NOTE: this function returns a tuple: (y, x)
getstr()
getsyx() # NOTE: this function returns a tuple: (y, x)
getyx(WINDOW) # NOTE: this function returns a tuple: (y, x)
halfdelay(tenths)
has_colors()
has_ic()
has_il()
has_key(ch)
hline(ch, n)
idcok(WINDOW, flag)
idlok(WINDOW, yes)
immedok(WINDOW, flag)
inch()
init_color(color, r, g, b)
init_pair(pair_number, fg, bg)
initscr()
insch(ch, [attr])
insdelln(nlines)
insertln()
insnstr(str, n, [attr])
insstr(str, [attr])
instr([n])
is_linetouched(WINDOW, line)
is_wintouched(WINDOW)
isendwin()
keyname(k)
keypad(WINDOW, yes)
killchar()
leaveok(WINDOW, yes)
longname()
meta(WINDOW, yes) # NOTE: effect may differ on Win and X
mouseinterval(interval)
mousemask(mmask)
move(new_y, new_x)
mvaddch(y, x, ch, [attr])
mvaddnstr(y, x, str, n, [attr])
mvaddstr(y, x, str, [attr])
mvchgat(y, x, num, attr, color, [opts]) # NOTE: 'opts' is unused in UniCurses
mvdelch(y, x)
mvdeleteln(y, x)
mvderwin(WINDOW, pary, parx)
mvgetch(y, x)
mvgetstr(y, x)
mvhline(y, x, ch, n)
mvinch(y, x)
mvinsch(y, x, ch, [attr])
mvinsnstr(y, x, str, n, [attr])
mvinsstr(y, x, str, pattr])
mvinstr(y, x, [n])
mvvline(y, x, ch, n)
mvwaddch(WINDOW, y, x, ch, [attr])
mvwaddnstr(WINDOW, y, x, str, n, [attr])
mvwaddstr(WINDOW, y, x, str, [attr])
mvwchgat(WINDOW, y, x, num, attr, color, [opts]) # NOTE: 'opts' is unused
mvwdelch(WINDOW, y, x)
mvwdeleteln(WINDOW, y, x)
mvwgetch(WINDOW, y, x)
mvwgetstr(WINDOW, y, x)
mvwhline(WINDOW, y, x, ch, n)
mvwin(WINDOW, y, x)
mvwinch(WINDOW, y, x)
mvwinsch(WINDOW, y, x, ch, [attr])
mvwinsnstr(WINDOW, y, x, strn, n, [attr])
mvwinsstr(WINDOW, y, x, strn, [attr])
mvwinstr(WINDOW, y, x, [n])
mvwvline(WINDOW, y, x, ch, n)
napms(ms)
newpad(nlines, ncols)
newwin(nlines, ncols, begin_y, begin_x)
nl():
nocbreak()
nodelay(WINDOW, yes)
noecho()
nonl():
noqiflush()
noraw()
notimeout(WINDOW, yes)
noutrefresh(WINDOW)
overlay(src_id, dest_id)
overwrite(src_id, dest_id)
pair_content(pair_number) # NOTE: this function returns a tuple: (fg, bg)
pair_number(attr)
prefresh(WINDOW, pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)
qiflush()
raw()
redrawln(beg, num)
redrawwin(WINDOW)
refresh()
reset_prog_mode()
reset_shell_mode()
scroll([lines])
scrollok(WINDOW, flag)
setscrreg(top, bottom)
setsyx(y, x)
standend()
standout()
start_color()
subpad(scrwin, nlines, ncols, begin_y, begin_x)
subwin(srcwin, nlines, ncols, begin_y, begin_x)
syncdown()
syncok(WINDOW, flag)
syncup()
termattrs()
termname()
timeout(delay)
touchline(y, x, [changed])
touchln(y, x, [changed])
touchwin(WINDOW)
unctrl(ch)
ungetch(ch)
ungetmouse(id, x, y, z, bstate)
untouchwin(WINDOW)
use_default_colors()
use_env(flag)
vline(ch, n)
waddch(WINDOW, ch, [attr])
waddnstr(WINDOW, str, n, [attr])
waddstr(WINDOW, str, [attr])
wattroff(WINDOW, attr)
wattron(WINDOW, attr)
wattrset(WINDOW, attr)
wbkgd(WINDOW, ch, [attr])
wbkgdset(WINDOW, ch, [attr])
wborder(WINDOW, [ls, rs, ts, bs, tl, tr, bl, br])
wchgat(WINDOW, num, attr, color, [opts])  # NOTE: 'opts' is unused
wclear(WINDOW)
wclrtobot(WINDOW)
wclrtoeol(WINDOW)
wdelch(WINDOW)
wdeleteln(WINDOW)
wechochar(WINDOW, ch, [attr])
wenclose(WINDOW, y, x)
werase(WINDOW)
wgetch(WINDOW)
wgetkey(WINDOW, [y, x])
wgetstr(WINDOW)
whline(WINDOW, ch, n)
winch(WINDOW)
winsch(WINDOW, ch, [attr])
winsdelln(WINDOW, nlines)
winsertln(WINDOW)
winsnstr(WINDOW, strn, n, [attr])
winsstr(WINDOW, strn, [attr])
winstr(WINDOW, [n])
wmove(WINDOW, new_y, new_x)
wredrawln(WINDOW, beg, num)
wrefresh(WINDOW)
wscrl(WINDOW, [lines])
wsetscrreg(WINDOW, top, bottom)
wstandend(WINDOW)
wstandout(WINDOW)
wsyncdown(WINDOW)
wsyncup(WINDOW)
wtimeout(WINDOW, delay)
wtouchline(WINDOW, start, count, [changed])
wvline(WINDOW, ch, n)
```

The functions from the Panel module of Curses (fully cross-platform):
```python
bottom_panel(PANEL)
del_panel(PANEL)
hide_panel(PANEL)
move_panel(PANEL, y, x)
new_panel(scr_id)
panel_above(PANEL)
panel_below(PANEL)
panel_hidden(PANEL)
panel_userptr(PANEL)
panel_window(PANEL)
replace_panel(PANEL, win)
set_panel_userptr(PANEL, obj)
show_panel(PANEL)
top_panel(PANEL)
update_panels()
```

The following functions are specific to UniCurses, they are completely cross-
platform and they make the Curses functions easier to use:
```python
ALTCHAR(ch)     # NOTE: this function returns a C character from the alternate set (use it when inserting an alternate character wherever a 'ch' is required). This is effectively the same as CCHAR(ch | A_ALTCHARSET).
CCHAR(ch)       # NOTE: this function returns a C character from the standard set (use it when inserting a character wherever a 'ch' is required)
COLOR_PAIR(n)   # NOTE: this is a synonym for the lowercase color_pair(n) for better NCurses/PDCurses compliance.
KEY_F(n)        # NOTE: this function mimics the NCurses macro with the same name that is used to return a keycode for different function keys, e.g. KEY_F(1) returns the keycode for the F1 key.
```

The functions that are NOT cross-platform and are only available on Linux:

```python
getwin(file) # NOTE: this function will throw exception on Windows
putp(str) # NOTE: this function is a stub on Windows
putwin(WINDOW, file) # NOTE: this function will throw exception on Win
setupterm(termstr, fd) # NOTE: this function is a stub on Windows
tigetflag(capname) # NOTE: this function is a stub on Windows
tigetnum(capname) # NOTE: this function is a stub on Windows
tigetstr(capname) # NOTE: this function is a stub on Windows
tparm(str, [p1, p2, p3, p4, p5, p6, p7, p8, p9]) # NOTE: this function is a stub on Windows
typeahead(fd) # NOTE: this function is a stub on Windows
```

IMPORTANT: The following functions are generally portable and may be used on all platforms, but their output or effect may differ depending on the platform. It is up to the programmer to ascertain that the program behaves in the same way on all necessary platforms if these functions are used:
insdelln, insertln, winsdelln, winsertln, noutrefresh, setscrreg, unctrl.

Constants provided by UniCurses
-------------------------------
UniCurses provides the following constants on all platforms:

Function return values:
```python
OK
ERR
```

Attributes:
```python
A_ALTCHARSET
A_BLINK
A_BOLD
A_DIM
A_NORMAL
A_STANDOUT
A_UNDERLINE
A_REVERSE
A_PROTECT
A_ATTRIBUTES
A_COLOR
A_CHARTEXT
A_INVIS
```

Colors:
```python
COLOR_BLACK
COLOR_BLUE
COLOR_CYAN
COLOR_GREEN
COLOR_MAGENTA
COLOR_RED
COLOR_WHITE
COLOR_YELLOW
```

Alternate Character Set:
```python
ACS_ULCORNER
ACS_LLCORNER
ACS_URCORNER
ACS_LRCORNER
ACS_LTEE
ACS_RTEE
ACS_BTEE
ACS_TTEE
ACS_HLINE
ACS_VLINE
ACS_PLUS
ACS_S1
ACS_S9
ACS_DIAMOND
ACS_CKBOARD
ACS_DEGREE
ACS_PLMINUS
ACS_BULLET
ACS_LARROW
ACS_RARROW
ACS_DARROW
ACS_UARROW
ACS_BOARD
ACS_LANTERN
ACS_BLOCK
ACS_S3
ACS_S7
ACS_LEQUAL
ACS_GEQUAL
ACS_PI
ACS_NEQUAL
ACS_STERLING
ACS_BSSB
ACS_SSBB
ACS_BBSS
ACS_SBBS
ACS_SBSS
ACS_SSSB
ACS_SSBS
ACS_BSSS
ACS_BSBS
ACS_SBSB
ACS_SSSS
```

Keyboard and Mouse:
```python
KEY_MIN
KEY_BREAK
KEY_SRESET
KEY_RESET
KEY_DOWN
KEY_UP
KEY_LEFT
KEY_RIGHT
KEY_HOME
KEY_BACKSPACE
KEY_F0        # NOTE: Function keys 1-64 are provided via a function KEY_F(n)
KEY_DL
KEY_IL
KEY_DC
KEY_IC
KEY_EIC
KEY_CLEAR
KEY_EOS
KEY_EOL
KEY_SF
KEY_SR
KEY_NPAGE
KEY_PPAGE
KEY_STAB
KEY_CTAB
KEY_CATAB
KEY_ENTER
KEY_PRINT
KEY_LL
KEY_A1
KEY_A3
KEY_B2
KEY_C1
KEY_C3
KEY_BTAB
KEY_BEG
KEY_CANCEL
KEY_CLOSE
KEY_COMMAND
KEY_COPY
KEY_CREATE
KEY_END
KEY_EXIT
KEY_FIND
KEY_HELP
KEY_MARK
KEY_MESSAGE
KEY_MOVE
KEY_NEXT
KEY_OPEN
KEY_OPTIONS
KEY_PREVIOUS
KEY_REDO
KEY_REFERENCE
KEY_REFRESH
KEY_REPLACE
KEY_RESTART
KEY_RESUME
KEY_SAVE
KEY_SBEG
KEY_SCANCEL
KEY_SCOMMAND
KEY_SCOPY
KEY_SCREATE
KEY_SDC
KEY_SDL
KEY_SELECT
KEY_SEND
KEY_SEOL
KEY_SEXIT
KEY_SFIND
KEY_SHELP
KEY_SHOME
KEY_SIC
KEY_SLEFT
KEY_SMESSAGE
KEY_SMOVE
KEY_SNEXT
KEY_SOPTIONS
KEY_SPREVIOUS
KEY_SPRINT
KEY_SREDO
KEY_SREPLACE
KEY_SRIGHT
KEY_SRSUME
KEY_SSAVE
KEY_SSUSPEND
KEY_SUNDO
KEY_SUSPEND
KEY_UNDO
KEY_MOUSE
KEY_RESIZE
KEY_MAX

BUTTON1_RELEASED      
BUTTON1_PRESSED
BUTTON1_CLICKED       
BUTTON1_DOUBLE_CLICKED
BUTTON1_TRIPLE_CLICKED

BUTTON2_RELEASED      
BUTTON2_PRESSED
BUTTON2_CLICKED       
BUTTON2_DOUBLE_CLICKED
BUTTON2_TRIPLE_CLICKED

BUTTON3_RELEASED      
BUTTON3_PRESSED
BUTTON3_CLICKED       
BUTTON3_DOUBLE_CLICKED
BUTTON3_TRIPLE_CLICKED

BUTTON4_RELEASED      
BUTTON4_PRESSED
BUTTON4_CLICKED       
BUTTON4_DOUBLE_CLICKED
BUTTON4_TRIPLE_CLICKED

BUTTON_SHIFT
BUTTON_CTRL
BUTTON_ALT

ALL_MOUSE_EVENTS
REPORT_MOUSE_POSITION
```

Unimplemented things
---------------------
The following features are not yet completely implemented or may have bugs:
- Using localized characters in text strings (tested on PDCurses in Windows but may cause problems under Linux and Mac OS X).
- The module `textpad` (curses.textpad) has not yet been ported to UniCurses.

Some final technical considerations
-----------------------------------
1. Many UniCurses functions return `ERR` in case an error occurs while executing them. This behavior is the same across all platforms (note that it's different from the method used in the original "curses" Python module, where an exception is thrown in case of an error).
2. Even though UniCurses tends to unify the behavior of commands across various platforms, certain functions may in rare cases provide slightly different output depending on the implementation of Curses used on each particular platform. While such cases are relatively rare and are typically not fatal, it's the responsibility of the author of each particular program that uses UniCurses to test and ensure that his/her program works consistently across various platforms.
3. Even though UniCurses itself is compatible both with Python 2.x and Python 3.x, the target programs written using UniCurses don't have to be (and most often won't be). It's possible to write an exclusively Python 2 and an exclusively Python 3 program using UniCurses, as well as a Python-independent one in case your program does not use any language syntax or modules that are only present in either Python 2 or Python 3.
