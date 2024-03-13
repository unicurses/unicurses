"""Testing suite"""

import unicurses

stdscr = unicurses.initscr()


"""
waddch
wadd_wch
waddstr
waddwstr
waddnstr
wattroff
wattron
wattrset
baudrate
beep
COLOR_PAIR
copywin
wclear
wclrtobot
wclrtoeol
clearok
curs_set
cursyncup
def_prog_mode
def_shell_mode
delay_output
wdelch
wdeleteln
wbkgd
wbkgdset
wborder
box
can_change_color
cbreak
wchgat
color_content
color_pair
delwin
derwin
doupdate
echo
wechochar
wenclose
endwin
werase
erasechar
filter
flash
flushinp
getbegyx
wgetch
wget_wch
wgetkey
getmaxyx
getmaxy
getmaxx
getmouse
getparyx
wgetstr
getsyx
getwin
getyx
halfdelay
has_colors
has_ic
has_il
has_key
whline
idcok
idlok
immedok
winch
init_color
init_pair
initscr
winsch
winsdelln
winsstr
winsnstr
winstr
isendwin
winsertln
is_linetouched
is_wintouched
keyname
keypad
killchar
get_tabsize
set_tabsize
leaveok
longname
meta
mouseinterval
mousemask
wmove
mvwaddch
mvwadd_wch
mvwaddstr
mvwaddwstr
mvwaddnstr
mvwchgat
mvwdelch
mvwdeleteln
mvderwin
mvwgetch
mvwgetstr
mvwhline
mvwinch
mvwinsch
mvwinsstr
mvwinsnstr
mvwinstr
mvwinwstr
mvwvline
mvwin
napms
newpad
newwin
nl
nocbreak
nodelay
noecho
nonl
noqiflush
noraw
notimeout
noutrefresh
overlay
overwrite
pair_content
pair_number
prefresh
putp
putwin
qiflush
raw
wredrawln
redrawwin
wrefresh
reset_prog_mode
reset_shell_mode
wresize
resize_term
wscrl
scrollok
wsetscrreg
setsyx
setupterm
wstandend
wstandout
start_color
subpad
subwin
wsyncdown
syncok
wsyncup
termattrs
termname
tigetflag
tigetnum
tigetstr
wtimeout
wtouchline
touchwin
tparm
typeahead
wvline
unctrl
ungetch
ungetmouse
untouchwin
use_default_colors
use_env
attroff
attron
attrset
clear
getch
get_wch
mvinsnstr
insnstr
insch
refresh
border
bkgd
bkgdset
erase
timeout
hline
vline
mvhline
mvvline
scroll
setscrreg
delch
mvdelch
move
insertln
insdelln
inch
mvinch
clrtobot
clrtoeol
mvgetch
addch
mvaddch
add_wch
mvadd_wch
addstr
addwstr
mvaddstr
mvaddwstr
addnstr
mvaddnstr
insstr
mvinsstr
echochar
standout
standend
chgat
mvchgat
deleteln
mvdeleteln
enclose
getstr
mvgetstr
instr
mvinstr
mvinwstr
touchline
touchln
mvinsch
redrawln
syncdown
syncup
getkey
wrapper
panel_above
panel_below
bottom_panel
del_panel
panel_hidden
hide_panel
move_panel
new_panel
replace_panel
set_panel_userptr
show_panel
top_panel
update_panels
panel_userptr
panel_window
"""

unicurses.endwin()