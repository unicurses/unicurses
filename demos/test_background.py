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
init_pair(2, COLOR_BLACK, COLOR_WHITE)
init_pair(3, COLOR_CYAN, COLOR_WHITE)
init_pair(4, COLOR_WHITE, COLOR_GREEN)

print_in_middle(stdscr, int(LINES / 2), 0, 0, "This is a background test, press any key to advance.")
getch()

bkgd(COLOR_PAIR(1))
getch()
bkgd(COLOR_PAIR(2))
getch()         
bkgd(COLOR_PAIR(3))
getch()
bkgd(COLOR_PAIR(4))
getch()
bkgd(COLOR_PAIR(4) | A_BOLD)
getch()
bkgd(CCHAR('#'))
getch()
bkgd(CCHAR(' '))
getch()
bkgdset(COLOR_PAIR(2))
mvaddstr(int(LINES / 2) + 2, 22, "This is the test of bkgdset function.")
getch()

endwin()