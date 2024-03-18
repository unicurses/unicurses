import unicurses as uc

stdscr = uc.initscr()
uc.cbreak()
uc.noecho()
uc.keypad(stdscr, True)

uc.mvaddstr(0, 0, "Press q to exit")
while True:
    key = uc.getkey()
    string = str(key, "utf-8")
    
    if string == "q":
        break
        
    uc.move(1,0)
    uc.clrtoeol()
    uc.mvaddstr(1, 0, f"key = {key}")
    uc.move(2,0)
    uc.clrtoeol()
    uc.mvaddstr(2, 0, f"str = {string}")
        
uc.endwin()

