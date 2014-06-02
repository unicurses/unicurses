from unicurses import *

def win_show(win, label, label_color):
    starty, startx = getbegyx(win)
    height, width = getmaxyx(win)
    box(win, 0, 0)
    mvwaddch(win, 2, 0, ACS_LTEE)
    mvwhline(win, 2, 1, ACS_HLINE, width - 2)
    mvwaddch(win, 2, width - 1, ACS_RTEE)
    print_in_middle(win, 1, 0, width, label, COLOR_PAIR(label_color))

def print_in_middle(win, starty, startx, width, string, color):
    if (win == None): win = stdscr
    y, x = getyx(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    wattron(win, color)
    mvwaddstr(win, y, x, string)
    wattroff(win, color)
    refresh()

def init_wins(wins, n):
    y = 2
    x = 10
    for i in range(0, n):
        wins[i] = newwin(10, 40, y, x)
        label = str.format("Window number {0}", i + 1)
        win_show(wins[i], label, i + 1)
        y += 3
        x += 7

NLINES = 10
NCOLS = 40
my_wins = [0] * 3
my_panels = [0] * 3

stdscr = initscr()
start_color()
cbreak()
noecho()
keypad(stdscr, True)

init_pair(1, COLOR_RED, COLOR_BLACK)
init_pair(2, COLOR_GREEN, COLOR_BLACK)
init_pair(3, COLOR_BLUE, COLOR_BLACK)
init_pair(4, COLOR_CYAN, COLOR_BLACK)

init_wins(my_wins, 3)

my_panels[0] = new_panel(my_wins[0])
my_panels[1] = new_panel(my_wins[1])
my_panels[2] = new_panel(my_wins[2])

set_panel_userptr(my_panels[0], my_panels[1])
set_panel_userptr(my_panels[1], my_panels[2])
set_panel_userptr(my_panels[2], my_panels[0])

update_panels()

attron(COLOR_PAIR(4))
mvaddstr(0, int(NCOLS / 2) - 2, "Use tab to browse through the windows (Q to Exit)")
attroff(COLOR_PAIR(4))
doupdate()

top = my_panels[2]

ch = -1
while ( (ch != CCHAR('q')) and (ch != CCHAR('Q')) ):
    ch = getch()
    if ch == 9:
        top = panel_userptr(top)
        top_panel(top)
    update_panels()
    doupdate()

endwin()
