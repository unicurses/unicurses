import unicurses as uc

stdscr = uc.initscr()
uc.cbreak()
uc.noecho()
uc.keypad(stdscr, True)

uc.mvaddstr(0, 0, "Press q to exit")
while True:
    key = uc.wgetkey(stdscr)
    
    if key == "q":
        break
        
    uc.move(1,0)
    uc.clrtoeol()
    uc.mvaddstr(1, 0, f"key = {key}")
        
uc.endwin()

