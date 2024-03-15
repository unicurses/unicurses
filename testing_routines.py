"""Testing suite"""

import unicurses as uc

# some variables

A_BOLD = uc.NCURSES_BITS(1,13)

# --- functions ---

def main(stdscr, command):

    match command:
        case "waddch":
            uc.waddch(stdscr, "e")
        case "wadd_wch":
            uc.wadd_wch(stdscr, "🌱")
        case "waddstr":
            uc.waddstr(stdscr, "test")
        case "waddwstr":
            uc.waddwstr(stdscr, "test 🌱")
        case "waddnstr":
            uc.waddnstr(stdscr, "long test", 6)
        case "wattron":
            uc.wattron(stdscr, A_BOLD)
            uc.addstr("test")
        case "wattroff":
            uc.wattron(stdscr, A_BOLD)
            uc.addstr("test")
            uc.refresh()
            uc.napms(1000)
            uc.wattroff(stdscr, A_BOLD)
            uc.addstr("test")
        case "wattrset":
            pass
        case "baudrate":
            uc.addstr(stdscr, uc.baudrate())
        case "beep":
            uc.beep()
        case "copywin":
            pass
        case "wclear":
            uc.addstr("previous test")
            uc.wclear(stdscr)
            uc.addstr("works")
        case "wclrtobot":
            uc.addstr("line1/2")
            uc.mvaddstr(1, 0, "line2/2")
            uc.wmove(stdscr, 0, 0)
            uc.wclrtobot(stdscr)
        case "wclrtoeol":
            uc.addstr("line1/2")
            uc.mvaddstr(1, 0, "line2/2")
            uc.move(0, 0)
            uc.wclrtoeol(stdscr)
        case "clearok":
            pass
        case "curs_set":
            uc.curs_set(0)
            uc.addstr("test")
            uc.curs_set(1)
        case "cursyncup":
            pass
        case "def_prog_mode":
            pass
        case "def_shell_mode":
            pass
        case "delay_output":
            uc.addstr("test1")
            uc.refresh()
            uc.delay_output(1000)
            uc.addstr("test2")
        case "wdelch":
            uc.addstr("Missing initial character")
            uc.move(0, 0)
            uc.wdelch(stdscr)
        case "wdeleteln":
            uc.addstr("line 1/2")
            uc.mvaddstr(1, 0, "line 2/2")
            uc.move(0, 0)
            uc.wdeleteln(stdscr)
        case "wbkgd":
            uc.addstr("test")
            uc.wbkgd(stdscr, ".", uc.NCURSES_BITS(1,13))
        case "wbkgdset":
            uc.addstr("test")
            uc.wbkgdset(stdscr, "-", uc.NCURSES_BITS(1,13))
        case "wborder":
            uc.wborder(stdscr, '|', '|', '-', '-')
        case "box":
            uc.box(stdscr, "@", "?")
        case "can_change_color":
            uc.addstr( uc.can_change_color() )
        case "cbreak":
            uc.getch()
            uc.getch()
        case "wchgat":
            uc.addstr("test1 test2")
            uc.move(0,0)
            uc.wchgat(stdscr, 5, A_BOLD, 1)
        case "color_content":
            color = 100
            uc.addstr("rbg of " + str(color) + " is " + str(uc.color_content(color)))
        case "color_pair":
            color = 100
            uc.addstr("rbg of " + str(color) + " is " + str(uc.color_pair(color)))
        case "delwin":
            uc.addstr("----------")
            uc.mvaddstr(1,0,"----------")
            uc.mvaddstr(2,0,"----------")
            uc.mvaddstr(3,0,"----------")
            new_win = uc.derwin(stdscr, 2, 2, 1, 1)
            uc.waddstr(new_win, "@")
            uc.delwin(new_win)
            uc.waddstr(new_win, "@")
        case "derwin":
            uc.addstr("----------")
            uc.mvaddstr(1,0,"----------")
            uc.mvaddstr(2,0,"----------")
            uc.mvaddstr(3,0,"----------")
            new_win = uc.derwin(stdscr, 2, 2, 1, 1)
            uc.waddstr(new_win, "@")
        case "doupdate":
            uc.addstr("test1")
            uc.noutrefresh(stdscr)
            uc.doupdate()
            uc.napms(1000)
            uc.move(0,0)
            uc.addstr("test2")
        case "echo":
            pass
        case "wechochar":
            uc.wechochar(stdscr, "e")
            uc.napms(1000)
            uc.wechochar(stdscr, "3")
        case "wenclose":
            uc.addstr("(-1, 0) = " + str(uc.wenclose(stdscr, -1, 0)) + ", (0, 0) = " + str(uc.wenclose(stdscr, 0, 0)) )
        case "werase":
            uc.addstr("test")
            uc.refresh()
            uc.napms(1000)
            uc.werase(stdscr)
        case "erasechar":
            uc.addstr(uc.erasechar())
        case "filter":
            pass
        case "nofilter":
            pass
        case "flash":
            uc.refresh()
            uc.flash()
        case "flushinp":
            uc.addstr("press arrow up")
            uc.getch()
            uc.flushinp()
            uc.mvaddstr(1, 0, "works!")
        case "getbegyx":
            pass
        case "wgetch":
            key = uc.wgetch(stdscr)
            uc.mvaddch(1,0,key)
        case "wget_wch":
            key = uc.wget_wch(stdscr)
            uc.mvaddch(1,0,key)
        case "wgetkey":
            uc.mvaddch(1,0,"|")
            uc.mvaddch(0,1,"_")
            key = uc.wgetkey(stdscr, 1, 1)
            uc.addch(key)
        case "getmaxyx":
            y, x = uc.getmaxyx(stdscr)
            uc.addstr("y = " + str(y) + ", x = " + str(x))
        case "getmaxy":
            y = uc.getmaxy(stdscr)
            uc.addstr("y = " + str(y))
        case "getmaxx":
            x = uc.getmaxx(stdscr)
            uc.addstr("x = " + str(x))
        case _:
            uc.addstr("command not found")

    uc.getkey()



if __name__ == "__main__":
    while (command := input("(q to exit) command: ")) != "q":
        uc.wrapper(main, command)