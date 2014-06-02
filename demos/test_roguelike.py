from unicurses import *

RAW_LEVEL_MAP = ['                              ',
                 '                              ',
                 '                              ',
                 '                              ',
                 '          ###############     ',
                 '         ##            ##     ',
                 '   ######               #     ',
                 '   #                    #     ',
                 '   #              `  `  #     ',
                 '   #############        #     ',
                 '               #  `  `  #     ',
                 '               #        #     ',
                 '               ##########     ']

LEVEL_MAP = []

PLAYER_X = -1
PLAYER_Y = -1
START_X = 10
START_Y = 7
HP = 10
TURN = 1

OBJ_PLAYER = '@'
OBJ_WALL = '#'
OBJ_STATUE = '`'
MSG = ""

def load_level_map():
    global LEVEL_MAP
    LEVEL_MAP = []
    for i in range(len(RAW_LEVEL_MAP)):
        LEVEL_MAP.append( [] )
        for j in range(len(RAW_LEVEL_MAP[i])):
            LEVEL_MAP[i].append(RAW_LEVEL_MAP[i][j])

def render_game_map():
    # render the map
    for i in range(len(LEVEL_MAP)):
            for j in range(len(LEVEL_MAP[i])):
                obj = LEVEL_MAP[i][j]
                if obj == OBJ_WALL:
                    attron(COLOR_PAIR(2))
                    mvaddstr(i, j, obj)
                    attroff(COLOR_PAIR(2))
                elif obj == OBJ_STATUE:
                    attron(COLOR_PAIR(3) | A_BOLD)
                    mvaddstr(i, j, obj)
                    attroff(COLOR_PAIR(3) | A_BOLD)
    # render the player
    mvaddch(PLAYER_Y, PLAYER_X, CCHAR(OBJ_PLAYER))

def render_status_bar():
    attron(A_BOLD)
    mvaddstr(21, 0, MSG)
    attron(COLOR_PAIR(1))
    mvaddstr(22, 0, str.format("The Unnamed Adventurer -- Turn: {0}, HP: ", TURN))
    clrtoeol()
    if HP > 3: addstr(HP)
    attroff(COLOR_PAIR(1))
    if HP <= 3:
        attron(COLOR_PAIR(4))
        addstr(HP)
        attroff(COLOR_PAIR(4))
    attroff(A_BOLD)
    
def move_player(nx, ny):
    global TURN, PLAYER_X, PLAYER_Y, HP, MSG
    TURN += 1
    lookahead = LEVEL_MAP[ny][nx]
    if lookahead == OBJ_WALL:
        HP -= 2
        MSG = "You bang your head against the wall!"
    elif lookahead == OBJ_STATUE:
        HP -= 1
        MSG = "You bang your head against the statue!"
    else:
        MSG = ""
        PLAYER_X = nx
        PLAYER_Y = ny

def fight():
    global MSG, HP, TURN, LEVEL_MAP
    TURN += 1
    MSG = "You kick in all directions around you... "
    test_squares = [LEVEL_MAP[PLAYER_Y-1][PLAYER_X-1],
                    LEVEL_MAP[PLAYER_Y-1][PLAYER_X],
                    LEVEL_MAP[PLAYER_Y-1][PLAYER_X+1],
                    LEVEL_MAP[PLAYER_Y][PLAYER_X-1],
                    LEVEL_MAP[PLAYER_Y][PLAYER_X],
                    LEVEL_MAP[PLAYER_Y][PLAYER_X+1],
                    LEVEL_MAP[PLAYER_Y+1][PLAYER_X-1],
                    LEVEL_MAP[PLAYER_Y+1][PLAYER_X],
                    LEVEL_MAP[PLAYER_Y+1][PLAYER_X+1]]

    for i in range(len(test_squares)):
        if test_squares[i] == OBJ_WALL:
            MSG += "you hit the wall! Ouch!"
            HP -= 2
            break
        if test_squares[i] == OBJ_STATUE:
            MSG += "you smash the statue to pieces!"
            if i==0: LEVEL_MAP[PLAYER_Y-1][PLAYER_X-1] = ' '
            if i==1: LEVEL_MAP[PLAYER_Y-1][PLAYER_X] = ' '
            if i==2: LEVEL_MAP[PLAYER_Y-1][PLAYER_X+1] = ' '
            if i==3: LEVEL_MAP[PLAYER_Y][PLAYER_X-1] = ' '
            if i==4: LEVEL_MAP[PLAYER_Y][PLAYER_X] = ' '
            if i==5: LEVEL_MAP[PLAYER_Y][PLAYER_X+1] = ' '
            if i==6: LEVEL_MAP[PLAYER_Y+1][PLAYER_X-1] = ' '
            if i==7: LEVEL_MAP[PLAYER_Y+1][PLAYER_X] = ' '
            if i==8: LEVEL_MAP[PLAYER_Y+1][PLAYER_X+1] = ' '

# the main loop

stdscr = initscr()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)

start_color()
init_pair(1, COLOR_YELLOW, COLOR_BLACK) # used for the status bar
init_pair(2, COLOR_CYAN, COLOR_BLACK) # used for the walls
init_pair(3, COLOR_RED, COLOR_BLACK) # used for the statues
init_pair(4, COLOR_RED, COLOR_BLACK) # used for low hit points

PLAYER_X = START_X
PLAYER_Y = START_Y
load_level_map()

while HP > 0:
    clear()
    render_game_map()
    render_status_bar()

    k = getch()
    if k == KEY_LEFT:
        move_player(PLAYER_X - 1, PLAYER_Y)
    elif k == KEY_RIGHT:
        move_player(PLAYER_X + 1, PLAYER_Y)
    elif k == KEY_UP:
        move_player(PLAYER_X, PLAYER_Y - 1)
    elif k == KEY_DOWN:
        move_player(PLAYER_X, PLAYER_Y + 1)
    elif k == CCHAR('f'):
        fight()

    refresh()

clear()
move(0, 0)
attron(A_BOLD)
addstr("You died a horrible death of boredom being stuck in a small dungeon with\n")
addstr("nothing but four statues... Your total score: ")
attron(COLOR_PAIR(1))
addstr(TURN)
attroff(COLOR_PAIR(1) | A_BOLD)
refresh()
getch()
clear()
refresh()
endwin()
print("Be seeing you...")
