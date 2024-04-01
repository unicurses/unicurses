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
            uc.wattrset(stdscr, uc.A_BOLD)
            uc.addstr("hello world")
        case "baudrate":
            uc.addstr(stdscr, uc.baudrate())
        case "beep":
            uc.beep()
        case "copywin":
            raise NotImplementedError
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
            uc.clearok(stdscr, True)
            uc.addstr("hello")
            uc.wrefresh(stdscr)
            uc.addstr(" world")
            uc.wrefresh(stdscr)
        case "curs_set":
            uc.curs_set(0)
            uc.addstr("test")
            uc.curs_set(1)
        case "wcursyncup":
            subwin = uc.subwin(stdscr, 10, 10, 0, 6)
            uc.addstr("hello")
            uc.waddstr(subwin, "world")
            uc.wcursyncup(stdscr)
        case "def_prog_mode":
            uc.def_prog_mode()
        case "def_shell_mode":
            uc.def_shell_mode()
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
            uc.addstr("button pressed " + str(button))
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
        case "flash":
            uc.refresh()
            uc.flash()
        case "flushinp":
            uc.addstr("press arrow up")
            uc.getch()
            uc.flushinp()
            uc.mvaddstr(1, 0, "works!")
        case "getbegyx":
            subwin = uc.subwin(stdscr, 10, 10, 1, 1)
            y, x = uc.getbegyx(subwin)
            uc.addstr("y=" + str(y) + " x=" + str(x))
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
            uc.addstr(str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str(e))
        case "getparyx":
            subwin = uc.subwin(stdscr, 10, 10, 1, 1)
            y, x = uc.getparyx(subwin)
            uc.addstr("y=" + str(y) + " x=" + str(x))
        case "wgetstr":
            string = uc.wgetstr(stdscr)
            uc.mvaddstr(1, 0, string)
        case "getsyx":
            uc.move(1,1)
            y, x = uc.getsyx()
            uc.addstr("x=" + str(x) + " y=" + str(y))
        case "getyx":
            uc.move(1, 1)
            y, x = uc.getyx(stdscr)
            uc.addstr("x=" + str(x) + " y=" + str(y))
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
            uc.addwstr("e" + str(uc.has_key('e')))
        case "whline":
            uc.whline(stdscr, "e",100)
        case "idcok":
            uc.idcok(stdscr, True)
        case "idlok":
            uc.idlok(stdscr, True)
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
            raise NotImplementedError
        case "init_pair":
            raise NotImplementedError
        case "winsch":
            uc.addstr("ello world")
            uc.move(0, 0)
            uc.winsch(stdscr, "h")
        case "winsdelln":
            for i in range(10):
                uc.mvaddstr(i, 0, str(i) + " line")
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
            uc.mvaddstr(1, 0, "line1=" + str(line1) + " line2=" + str(line2))
        case "is_wintouched":
            uc.wrefresh(stdscr)
            val = uc.is_wintouched(stdscr)
            uc.addstr("touched? " + str(val))
            val = uc.is_wintouched(stdscr)
            uc.mvaddstr(1, 0, "touched? " + str(val))
        case "keyname":
            uc.addstr("101= " + str(uc.keyname(101)))
        case "keypad":
            uc.keypad(stdscr, True)
            uc.addstr( uc.getkey() )
        case "killchar":
            uc.addstr( uc.killchar() )
        case "get_tabsize":
            uc.addstr(uc.get_tabsize())
        case "set_tabsize":
            uc.addstr(uc.get_tabsize())
            uc.set_tabsize(4)
            uc.addstr(" " + str(uc.get_tabsize()))
        case "leaveok":
            uc.leaveok(stdscr, True)
            uc.addstr("hello world")
        case "is_leaveok":
            uc.addstr(uc.is_leaveok())
            uc.leaveok(stdscr, True)
            uc.addstr(" " + str(uc.is_leaveok()))
        case "longname":
            uc.addstr(uc.longname())
        case "meta":
            uc.meta(True)
        case "mouseinterval":
            for _ in range(50):
                uc.addstr(uc.getch())
            uc.mouseinterval(1000)
            for _ in range(50):
                uc.addstr(uc.getch())
        case "mousemask":
            uc.mousemask(uc.ALL_MOUSE_EVENTS)
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
            raise NotImplementedError # test later after checking how to draw the new window
        case "napms":
            uc.addstr("hello ")
            uc.refresh()
            uc.napms(2000)
            uc.addstr("world")
        case "newpad":
            raise NotImplementedError
        case "newpad":
            raise NotImplementedError
        case "nl":
            raise NotImplementedError
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
            uc.addstr("typed " + str(button))
        case "nonl":
            raise NotImplementedError
        case "noqiflush":
            raise NotImplementedError
        case "noraw":
            uc.raw()
            uc.addstr("press ctrl+c: ")
            strn = uc.getstr()
            uc.mvaddstr(1, 0, strn)
            uc.noraw()
            uc.mvaddstr(2, 0, "press ctrl+c again: ")
            strn = uc.getstr()
        case "notimeout":
            uc.notimeout(stdscr, True)
            button = uc.getch()
            uc.addstr(button)
            uc.napms(1000)
        case "wnoutrefresh":
            raise NotImplementedError
        case "overlay":
            raise NotImplementedError
        case "overwrite":
            raise NotImplementedError
        case "pair_content":
            raise NotImplementedError
        case "pair_number":
            raise NotImplementedError
        case "prefresh":
            raise NotImplementedError
        case "putp":
            raise NotImplementedError
        case "putwin":
            raise NotImplementedError
        case "getwin":
            raise NotImplementedError
        case "qiflush":
            raise NotImplementedError
        case "raw":
            uc.raw()
            uc.addstr("press ctrl+c: ")
            strn = uc.getstr()
            uc.mvaddstr(1, 0, strn)
        case "wredrawln":
            raise NotImplementedError
        case "redrawwin":
            raise NotImplementedError
        case "wrefresh":
            uc.addstr("hello")
            uc.wrefresh(stdscr)
            uc.napms(1000)
            uc.addstr(" world")
        case "reset_prog_mode":
            raise NotImplementedError
        case "reset_shell_mode":
            raise NotImplementedError
        case "wresize":
            raise NotImplementedError
        case "resize_term":
            raise NotImplementedError
        case "wscrl":
            raise NotImplementedError
        case "scrollok":
            raise NotImplementedError
        case "is_scrollok":
            uc.scrollok(stdscr, True)
            uc.addstr( uc.is_scrollok(stdscr) )
        case "wsetscrreg":
            raise NotImplementedError
        case "setsyx":
            uc.addstr("hello")
            uc.setsyx(1, 6)
            uc.addstr(" world")
        case "setupterm":
            raise NotImplementedError
        case "wstandend":
            uc.wattrset(stdscr, uc.A_BOLD)
            uc.addstr("hello")
            uc.wstandend(stdscr)
            uc.addstr(" world")
        case "wstandout":
            uc.wstandout(stdscr)
            uc.addstr("hello world")
        case "start_color":
            uc.start_color()
            uc.addstr("hello world")
        case "subpad":
            raise NotImplementedError
        case "subwin":
            subwin = uc.subwin(stdscr, 5, 10, 0, 6)
            uc.addstr("hello")
            uc.waddstr(subwin, "world")
        case "wsyncdown":
            raise NotImplementedError
        case "syncok":
            raise NotImplementedError
        case "is_syncok":
            uc.addstr(uc.is_syncok(stdscr))
            uc.syncok(stdscr, True)
            uc.addstr(" " + str(uc.is_syncok(stdscr)))
        case "wsyncup":
            raise NotImplementedError
        case "termattrs":
            uc.addstr(uc.termattrs())
        case "termname":
            uc.addstr(uc.termname())
        case "tigetflag":
            raise NotImplementedError
        case "tigetnum":
            raise NotImplementedError
        case "tigetstr":
            raise NotImplementedError
        case "wtimeout":
            uc.wtimeout(stdscr, 1000)
            uc.getch()
        case "wtouchline":
            uc.addstr("line1")
            uc.mvaddstr(1, 0, "line2")
            uc.wtouchline(stdscr, 0, 1, 0)
        case "touchwin":
            raise NotImplementedError
        case "tparm":
            raise NotImplementedError
        case "typeahead":
            raise NotImplementedError
        case "wvline":
            uc.wvline(stdscr, "@", 20)
        case "unctrl":
            uc.addstr(uc.unctrl("e"))
        case "wunctrl":
            raise NotImplementedError
        case "ungetch":
            uc.ungetch("e")
            button = uc.getkey()
            uc.addstr("input= " + str(button))
        case "ungetmouse":
            uc.mousemask(uc.ALL_MOUSE_EVENTS)
            uc.ungetmouse(1, 1, 1, 1, 1)
            button = uc.getch()
            uc.addstr("input= " + str(button))
        case "untouchwin":
            uc.addstr("hello")
            uc.refresh()
            uc.addstr(" world")
            uc.untouchwin(stdscr)
        case "use_default_colors":
            raise NotImplementedError
        case "use_env":
            raise NotImplementedError
        case _:
            uc.addstr("command not found")

    uc.getkey()


if __name__ == "__main__":
    print("ENTER to exit")
    while (command := input("command: ")) != "":
        # some routines are to be run before initscr
        match command:
            case "filter":
                uc.filter()
                uc.initscr()
                uc.addstr("hello world")
                uc.getkey()
                uc.endwin()
            case "nofilter":
                uc.filter()
                uc.nofilter()
                uc.initscr()
                uc.addstr("hello world")
                uc.getkey()
                uc.endwin()
            case _:
                uc.wrapper(main, command)