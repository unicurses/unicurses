from unicurses import *


def print_in_middle(window, starty, startx, width, string, color):
    if (window == None): window = stdscr

    y, x = getyx(window)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    
    wattron(window, color)
    mvwaddstr(window, y, x, string)
    wattroff(window, color)
    
    refresh()


def refresh_topbar(window):
    starty, startx = getbegyx(window)
    height, width  = getmaxyx(window)

    mvwaddch(window, 2, 0, ACS_LTEE)
    mvwhline(window, 2, 1, ACS_HLINE, width - 2)
    mvwaddch(window, 2, width - 1, ACS_RTEE)


def set_label(window, label, color):
    print_in_middle(window, 1, 0, getmaxyx(window)[1], label, color)


def clear_borders_of(window):
    wborder(window,                                                         
        CCHAR(' ') , CCHAR(' '),                                            # left - right
        CCHAR(' ') , CCHAR(' '),                                            # Up   - Down
        CCHAR(' ') , CCHAR(' '),                                            # left - right  (  top  corner)
        CCHAR(' ') , CCHAR(' ')                                             # left - right  (bottom corner)
    )


def set_borders_to(window):
    wborder(window#,                                                         # wide-unicode charachters are not supported for linux's wborder at this moment.
        #CCHAR('│') , CCHAR('│'),                                            # left - right
        #CCHAR('─') , CCHAR('─'),                                            # Up   - Down
        #CCHAR('╭') , CCHAR('╮'),                                            # left - right  (  top  corner)
        #CCHAR('╰') , CCHAR('╯')                                             # left - right  (bottom corner)
    )


def new_window_with(height, width, starty, startx, label, color):
    window = newwin(height, width, starty, startx)    
    box(window, 0, 0)

    set_borders_to(window)
    set_label(window,label,color)
    
    refresh_topbar(window)
    wrefresh(window)
    return window


def move_window(window, starty, startx):
    clear_borders_of(window)
    wrefresh(window)                                                        # Refresh Window

    mvwin(window,starty, startx)                                            # Move    Window
    
    set_borders_to(window)
    refresh_topbar(window)
    wrefresh(window)                                                        # Refresh Window


def initialize_pairs_of_colors():
    init_pair(1, COLOR_RED  , COLOR_BLACK)
    init_pair(2, COLOR_GREEN, COLOR_BLACK)
    init_pair(3, COLOR_BLUE , COLOR_BLACK)
    init_pair(4, COLOR_CYAN , COLOR_BLACK)


def check_and_start_color():
    if (not has_colors()):
        endwin()
        print("Your terminal does not support color!")
        exit(1)    
    start_color()



if __name__ == "__main__":
    stdscr = initscr()                                                      # Global Variable

    cbreak()
    noecho()
    curs_set(0)
    keypad(stdscr, True)
    set_borders_to(stdscr)
    check_and_start_color()
    initialize_pairs_of_colors()
    mvaddstr(0,10,"Use arrow keys to move and tab to browse through the windows, press Q to exit")

    LINES , COLS   = getmaxyx(stdscr)
    height, width  = 10, 38
    starty, startx = 2 , 10

    my_wins   = [0] * 3
    my_panels = [0] * 3

    for i in range(3):
        my_wins  [i] = new_window_with(height, width, starty, startx, "Window number " + str(i + 1), COLOR_PAIR(i+1))
        my_panels[i] = new_panel(my_wins[i])
        
        startx += 7
        starty += 3

    set_panel_userptr(my_panels[0], my_panels[1])
    set_panel_userptr(my_panels[1], my_panels[2])
    set_panel_userptr(my_panels[2], my_panels[0])

    update_panels()
    refresh()

    ch             = -1
    topPanel       = my_panels[2]
    temp_win       = panel_window(topPanel)
    starty, startx = getbegyx(temp_win)

    while ( (ch != CCHAR('q')) and (ch != CCHAR('Q')) ):
        ch = getch()

        if ch == 9:
            topPanel = panel_userptr(topPanel)
            top_panel(topPanel)
            my_win = panel_window(topPanel)
            starty, startx = getbegyx(my_win)
        elif (ch == KEY_LEFT):                                              # KEY_XY won't work on vscode, run it on your terminal
            if startx - 1 > 0:
                startx -= 1
                move_panel(topPanel,starty, startx)
        elif (ch == KEY_RIGHT) and (startx + width  <  COLS - 1):
                startx += 1
                move_panel(topPanel,starty, startx)
        elif (ch == KEY_UP   ) and (starty - 1 > 0):
                starty -= 1
                move_panel(topPanel,starty, startx)
        elif (ch == KEY_DOWN ) and (starty + height < LINES - 1):
                starty += 1
                move_panel(topPanel,starty, startx)
        
        update_panels()
        doupdate()

    endwin()
