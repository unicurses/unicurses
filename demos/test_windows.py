from unicurses import *

def create_newwin(height, width, starty, startx):
    local_win = newwin(height, width, starty, startx)
    box(local_win, 0, 0)
    wrefresh(local_win)
    return local_win

def destroy_win(local_win):
    wborder(local_win, CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '))
    wrefresh(local_win)
    delwin(local_win)

stdscr = initscr()
cbreak()
noecho()
curs_set(0)
keypad(stdscr, True)

height = 3
width = 10
LINES, COLS = getmaxyx(stdscr)
starty = int((LINES - height) / 2)
startx = int((COLS - width) / 2)
addstr("Use cursor keys to move the window, press Q to exit")
refresh()

my_win = create_newwin(height, width, starty, startx)

ch = 0
while ( (ch != CCHAR('q')) and (ch != CCHAR('Q')) ):
    ch = getch()
    if ch == KEY_LEFT:
        if startx - 1 >= 0:
            destroy_win(my_win)
            startx -= 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == KEY_RIGHT:
        if startx + width < COLS:
            destroy_win(my_win)
            startx += 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == KEY_UP:
        if starty - 1 > 0:
            destroy_win(my_win)
            starty -= 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == KEY_DOWN:
        if starty + height < LINES:
            destroy_win(my_win)
            starty += 1
            my_win = create_newwin(height, width, starty, startx)

endwin()
