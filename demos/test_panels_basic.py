from unicurses import *

lines = 10
cols = 40
y = 2
x = 4
my_wins = [0] * 3
my_panels = [0] * 3

stdscr = initscr()
clear()
cbreak()
noecho()

my_wins[0] = newwin(lines, cols, y, x)
my_wins[1] = newwin(lines, cols, y + 1, x + 5)
my_wins[2] = newwin(lines, cols, y + 2, x + 10)

for i in range(0, 3):
    box(my_wins[i], 0, 0)

my_panels[0] = new_panel(my_wins[0])
my_panels[1] = new_panel(my_wins[1])
my_panels[2] = new_panel(my_wins[2])

# top_panel(my_panels[1])

update_panels()

doupdate()

getch()
endwin()
