from unicurses import *

def print_in_middle(win, starty, startx, width, string):
    if (win == None): win = stdscr
    y, x = getyx(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    mvaddstr(y, x, string)

stdscr = initscr()
noecho()
LINES, COLS = getmaxyx(stdscr)

if (has_colors() == False):
    endwin()
    print("Your terminal does not support color!")
    exit(1)

start_color()
init_pair(1, COLOR_RED, COLOR_BLACK)

border()
attron(COLOR_PAIR(1))
print_in_middle(stdscr, int(LINES / 2), 0, 0, "This line should be displayed in red color.")
attroff(COLOR_PAIR(1))
getch()
endwin()
