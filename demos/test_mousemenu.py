from unicurses import *

WIDTH = 30
HEIGHT = 10
startx = 0
starty = 0

choices = ["Choice 1", "Choice 2", "Choice 3", "Choice 4", "Exit"]
n_choices = len(choices)

choice = 0
c = 0

def print_menu(menu_win, highlight):
    x = 2
    y = 2
    box(menu_win, 0, 0)
    for i in range(0, n_choices):
        if (highlight == i + 1):
            wattron(menu_win, A_REVERSE)
            mvwaddstr(menu_win, y, x, choices[i])
            wattroff(menu_win, A_REVERSE)
        else:
            mvwaddstr(menu_win, y, x, choices[i])
        y += 1
    wrefresh(menu_win)

def report_choice(mouse_x, mouse_y):
    i = startx + 2
    j = starty + 3
    for choice in range(0, n_choices):
        if (mouse_y == j + choice) and (mouse_x >= i) and (mouse_x <= i + len(choices[choice])):
            if choice == n_choices - 1:
                return -1
            else:
                return choice + 1
            break

stdscr = initscr()
clear()
noecho()
cbreak()
curs_set(0)
startx = int((80 - WIDTH) / 2)
starty = int((24 - HEIGHT) / 2)

menu_win = newwin(HEIGHT, WIDTH, starty, startx)
keypad(menu_win, True)
mvaddstr(0, 0, "Click on Exit to quit (works best in a virtual console)")
refresh()
print_menu(menu_win, 1)
mouseinterval(0)
mousemask(ALL_MOUSE_EVENTS)

while True:
    c = wgetch(menu_win)
    if c == KEY_MOUSE:
        id, x, y, z, bstate = getmouse()
        if bstate & BUTTON1_PRESSED:
            chosen = report_choice(x + 1, y + 1)
            if chosen != None:
                mvaddstr(23, 0, str.format("MOUSE: {0}, {1}, {2}, Choice made is: {3}, Chosen string is: {4}", x, y, bstate, chosen, choices[chosen-1]))
            clrtoeol()
            refresh()
            if (chosen == -1):
                endwin()
                exit(1)
            print_menu(menu_win, chosen)

endwin()
