"""Testing suite"""

import unicurses as uc

# --- functions ---


def main(stdscr, command: str) -> None:
    uc.clear()

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
            uc.wattron(stdscr, uc.A_BOLD)
            uc.addstr("test")
        case "wattroff":
            uc.wattron(stdscr, uc.A_BOLD)
            uc.addstr("test")
            uc.refresh()
            uc.napms(1000)
            uc.wattroff(stdscr, uc.A_BOLD)
            uc.addstr("test")
        case "wattrset":
            ...
        case "baudrate":
            uc.addstr(stdscr, uc.baudrate())
        case "beep":
            uc.beep()
        case "copywin":
            ...
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
            ...
        case "curs_set":
            uc.curs_set(0)
            uc.addstr("test")
            uc.curs_set(1)
        case "cursyncup":
            ...
        case "def_prog_mode":
            ...
        case "def_shell_mode":
            ...
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
            uc.wbkgd(stdscr, ".", uc.NCURSES_BITS(1, 13))
        case "wbkgdset":
            uc.addstr("test")
            uc.wbkgdset(stdscr, "-", uc.NCURSES_BITS(1, 13))
        case "wborder":
            uc.wborder(stdscr, "|", "|", "-", "-")
        case "box":
            uc.box(stdscr, "@", "?")
        case "can_change_color":
            uc.addstr(uc.can_change_color())
        case "cbreak":
            uc.getch()
            uc.getch()
        case "wchgat":
            uc.addstr("test1 test2")
            uc.move(0, 0)
            uc.wchgat(stdscr, 5, uc.A_BOLD, 1)
        case "color_content":
            color = 100
            uc.addstr("rbg of " + str(color) + " is " + str(uc.color_content(color)))
        case "color_pair":
            color = 100
            uc.addstr("rbg of " + str(color) + " is " + str(uc.color_pair(color)))
        case "delwin":
            uc.addstr("----------")
            uc.mvaddstr(1, 0, "----------")
            uc.mvaddstr(2, 0, "----------")
            uc.mvaddstr(3, 0, "----------")
            new_win = uc.derwin(stdscr, 2, 2, 1, 1)
            uc.waddstr(new_win, "@")
            uc.delwin(new_win)
            uc.waddstr(new_win, "@")
        case "derwin":
            uc.addstr("----------")
            uc.mvaddstr(1, 0, "----------")
            uc.mvaddstr(2, 0, "----------")
            uc.mvaddstr(3, 0, "----------")
            new_win = uc.derwin(stdscr, 2, 2, 1, 1)
            uc.waddstr(new_win, "@")
        case "doupdate":
            uc.addstr("test1")
            uc.wnoutrefresh(stdscr)
            uc.doupdate()
            uc.napms(1000)
            uc.move(0, 0)
            uc.addstr("test2")
        case "echo":
            uc.noecho()
            button = uc.getkey()
            uc.addstr(f"button pressed {button}")
        case "wechochar":
            uc.wechochar(stdscr, "e")
            uc.napms(1000)
            uc.wechochar(stdscr, "3")
        case "wenclose":
            uc.addstr(
                "(-1, 0) = "
                + str(uc.wenclose(stdscr, -1, 0))
                + ", (0, 0) = "
                + str(uc.wenclose(stdscr, 0, 0))
            )
        case "werase":
            uc.addstr("test")
            uc.refresh()
            uc.napms(1000)
            uc.werase(stdscr)
        case "erasechar":
            uc.addstr(uc.erasechar())
        case "erasewchar":
            l = [None]
            uc.erasewchar(l)
            uc.addstr(l[0])
        case "filter":
            ...
        case "nofilter":
            ...
        case "flash":
            uc.refresh()
            uc.flash()
        case "flushinp":
            uc.addstr("press arrow up")
            uc.getch()
            uc.flushinp()
            uc.mvaddstr(1, 0, "works!")
        case "getbegyx":
            ...
        case "wgetch":
            key = uc.wgetch(stdscr)
            uc.mvaddch(1, 0, key)
        case "wget_wch":
            key = uc.wget_wch(stdscr)
            uc.mvaddch(1, 0, key)
        case "wgetkey":
            uc.mvaddch(1, 0, "|")
            uc.mvaddch(0, 1, "_")
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
        case "getmouse":
            uc.getch()
            a,b,c,d,e = uc.getmouse()
            uc.addstr(f"{a} {b} {c} {d} {e}")
        case "getparyx":
            ...
        case "wgetstr":
            string = uc.wgetstr(stdscr)
            uc.mvaddstr(1, 0, string)
        case "getsyx":
            uc.move(1,1)
            y, x = uc.getsyx()
            uc.addstr(f"x={x}, y={y}")
        case "getyx":
            uc.move(1, 1)
            y, x = uc.getyx(stdscr)
            uc.addstr(f"x={x}, y={y}")
        case "halfdelay":
            uc.halfdelay(10)
            err = uc.getch()
            uc.addstr(err)
            uc.napms(2)
        case "has_colors":
            uc.addstr(uc.has_colors())
        case "has_ic":
            uc.addstr(uc.has_ic())
        case "has_il":
            uc.addstr(uc.has_il())
        case "has_key":
            uc.addwstr(f"e : {uc.has_key('e')}")
        case "whline":
            uc.whline(stdscr, "e",100)
        case "idcok":
            ...
        case "idlok":
            ...
        case "immedok":
            uc.immedok(stdscr, True)
            uc.addstr("writing..")
            uc.napms(1000)
            uc.addstr("done")
        case "winch":
            uc.addstr("h🌱llo")
            uc.move(0,1)
            char = uc.winch(stdscr)
            uc.mvaddstr(1, 0, char)
        case "init_color":
            ...
        case "init_pair":
            ...
        case "winsch":
            uc.addstr("ello world")
            uc.move(0, 0)
            uc.winsch(stdscr, "h")
        case "winsdelln":
            for i in range(10):
                uc.mvaddstr(i, 0, f"{i} line")
            uc.move(0, 0)
            uc.winsdelln(stdscr, 1)
            uc.mvaddstr(0, 0, "new line here")
            uc.move(2, 0)
            uc.winsdelln(stdscr, -1)
        case "winsstr":
            uc.addstr("world")
            uc.move(0, 0)
            uc.winsstr(stdscr, "hello ")
        case "winsnstr":
            uc.addstr("orld")
            uc.move(0, 0)
            uc.winsnstr(stdscr, "hello world", 6)
        case "winstr":
            uc.addstr("hello world")
            uc.move(0, 0)
            string = uc.winstr(stdscr)
            uc.mvaddstr(1, 0, string)
        case "isendwin":
            uc.addstr(uc.isendwin())
        case "winsertln":
            uc.addstr("test")
            uc.winsertln(stdscr)
        case "is_linetouched":
            uc.wrefresh(stdscr)
            uc.addstr("test")
            line1 = uc.is_linetouched(stdscr, 0)
            line2 = uc.is_linetouched(stdscr, 1)
            uc.mvaddstr(1, 0, f"line1 = {line1}, line2 = {line2}")
        case "is_wintouched":
            uc.wrefresh(stdscr)
            val = uc.is_wintouched(stdscr)
            uc.addstr(f"touched? {val}")
            val = uc.is_wintouched(stdscr)
            uc.mvaddstr(1, 0, f"touched? {val}")
        case "keyname":
            uc.addstr(f"101 = {uc.keyname(101)}")
        case "keypad":
            uc.keypad(stdscr, True)
            uc.addstr( uc.getkey() )
        case "killchar":
            uc.addstr( uc.killchar() )
        case "killwchar":
            v = [None]
            uc.killwchar(v)
            uc.addstr(v[0])
        case "get_tabsize":
            uc.addstr(uc.get_tabsize())
        case "set_tabsize":
            uc.addstr(uc.get_tabsize())
            uc.set_tabsize(4)
            uc.addstr(f" {uc.get_tabsize()}")
        case "leaveok":
            uc.leaveok(stdscr, True)
            uc.addstr("hello world")
        case "is_leaveok":
            uc.addstr(uc.is_leaveok())
            uc.leaveok(stdscr, True)
            uc.addstr(f" {uc.is_leaveok()}")
        case "longname":
            uc.addstr(uc.longname())
        case "meta":
            ...
        case "mouseinterval":
            for _ in range(50):
                uc.addstr(uc.getch())
            uc.mouseinterval(1000)
            for _ in range(50):
                uc.addstr(uc.getch())
        case "mousemask":
            ...
        case "wmove":
            uc.wmove(stdscr, 10, 1)
        case "mvwaddch":
            uc.mvwaddch(stdscr, 3, 3, "e")
        case "mvwadd_wch":
            uc.mvwadd_wch(stdscr, 3, 3, "🌱")
        case "mvwaddstr":
            uc.mvwaddstr(stdscr, 3, 3, "hello world")
        case "mvwaddwstr":
            uc.mvwaddwstr(stdscr, 3, 3, "hello world 🌱")
        case "mvwaddnstr":
            uc.mvwaddnstr(stdscr, 3, 3, "hello world", 5)
        case "mvwchgat":
            uc.addstr("hello world")
            uc.mvwchgat(stdscr, 0, 0, 5, uc.A_BOLD, uc.COLOR_RED)
        case "mvwdelch":
            uc.addstr("hello world")
            uc.mvwdelch(stdscr, 0, 0)
        case "mvwdeleteln":
            uc.addstr("line1")
            uc.mvaddstr(1, 0, "line2")
            uc.mvwdeleteln(stdscr, 0, 0)
        case "mvderwin":
            for i in range(10):
                uc.mvaddstr(i, 0, "----------")
            subwin = uc.subwin(stdscr, 5, 5, 0, 0)
            uc.mvderwin(subwin, 2, 2)
            uc.mvwaddstr(subwin, 0, 0, "@")
        case "mvwgetch":
            uc.mvwgetch(stdscr, 2, 2)
        case "mvwgetstr":
            string = uc.mvwgetstr(stdscr, 1, 1)
            uc.mvaddstr(0, 0, string)
        case "mvwhline":
            uc.mvwhline(stdscr, 1, 0, "-", 20)
        case "mvwinch":
            uc.addstr("hello world")
            char = uc.mvwinch(stdscr, 0, 1)
            uc.mvaddch(1, 0, char)
        case "mvwinsch":
            uc.addstr("ello world")
            uc.mvwinsch(stdscr, 0, 0, "h")
        case "mvwinsstr":
            uc.addstr("world")
            uc.mvwinsstr(stdscr, 0, 0, "hello ")
        case "mvwinsnstr":
            uc.addstr("world")
            uc.mvwinsnstr(stdscr, 0, 0, "hello John", 6)
        case "mvwinstr":
            uc.addstr("hello world!")
            string = uc.mvwinstr(stdscr, 0, 6, 5)
            uc.mvaddstr(1, 0, string)
        case "mvwinwstr":
            uc.addstr("hello worl🌱!")
            string = uc.mvwinwstr(stdscr, 0, 6, 5)
            uc.mvaddstr(1, 0, string)
        case "mvwvline":
            uc.mvwvline(stdscr, 0, 0, "@", 5)
        case "mvwin":
            ... # test later after checking how to draw the new window
        case "napms":
            uc.addstr("hello ")
            uc.refresh()
            uc.napms(2000)
            uc.addstr("world")
        case "newpad":
            ...
        case "newpad":
            ...
        case "nl":
            ...
        case "nocbreak":
            uc.cbreak()
            uc.getkey()
            uc.mvaddstr(1, 0, "now nocbreak: ")
            uc.nocbreak()
            uc.getkey()
        case "nodelay":
            uc.nodelay(stdscr, True)
        case "noecho":
            uc.noecho()
            button = uc.getkey()
            uc.addstr(f"typed {button}")
        case "nonl":
            ...
        case "noqiflush":
            ...
        case "noraw":
            ...
        case "notimeout":
            uc.notimeout(stdscr, True)
            button = uc.getch()
            uc.addstr(button)
            uc.napms(1000)
        case "wnoutrefresh":
            ...
        case "overlay":
            ...
        case "overwrite":
            ...
        case "pair_content":
            ...
        case "pair_number":
            ...
        case _:
            uc.addstr("command not found")

    uc.getkey()


if __name__ == "__main__":
    while (command := input("(ENTER to exit) command: ")) != "":
        uc.wrapper(main, command)