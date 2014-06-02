from unicurses import *

stdscr = initscr()
start_color()

init_pair(1, COLOR_CYAN, COLOR_BLACK)
addstr("A big string which I didn't care to type fully ")
mvchgat(0, 0, -1, A_BOLD, 1, None)

refresh()
getch()

endwin()
