# TODO

# DISCUSS

- Turning wch and wstr into ch and str and keep those. Strings in python have utf-8 encoding anyway, it does not makes much sense to keep every standard library. The official curses module for Python only supports addch and addstr (https://docs.python.org/3/library/curses.html#module-curses)

- change cursyncup to wcursyncup

- change noutrefresh to wnoutrefresh

- in general, change some names to be more faithful to python.curses and more consistent to prefix=w <-> affect input-specified windows

- (done) add wrapper

- __CCHAR__: why do we let users pass in the number (ord) of the ascii character? CCHAR gets only either called by user, or called within the code with strings, not integers. Moreover ord of bytestring and ord of string return the same value, so I think we should just return ord or raise a custom error if ord fails, and avoid type checking

- (done) check if NCURSES or PDCURSES outside of functions, not inside, as the system never changes at runtime. It is also safer in case the user changes the values of PDCURSES or NCURSES by mistake.
 
- why is it necessary to raise an exception when importing ctypes as failing will raise the same exact exception type?

- __wgetkey__: either split this into mvwgetkey or remove all unnecessary mv before and make everything into one function optional positional arguments

- (done) convert value == 1 to bool(value) to write more pythonically

- __PDC_LEAVEOK__: change leaveok so that it actually behaves like ncurses, not sure why we need to use PDC_LEAVEOK, and do we actually need curscr at all? This can still be called by the user anyway, so that is the need? I suggest we make a function that returns curscr and let eveything else depend on scr_id instead. Is it not how curses functions are designed to start with anyway? Also, curscr is in ncurses too!

- make it easier for users to find attributes - for example make a function that prints them or add them to the wiki

- (done) add some missing functions such as is_scrollok or is_leaveok, they are cross-platform anyway!

- (done) remove touchln because it is identical to touchline

- (done) added wunctrl

- color_content does not seemt to work

- some functions such as __erasewchar__ and __killwchar__ require a pointer to be passed. How about we "translate" this class of functions into functions that accept vectors as pointers, and store whatever they have to store into the first coordinate? This approach would make porting C code to Python really easy.

- make so that, if you only use one scr, you DON'T NEED to store stdscr anywhere

# note

to get numbers that are originally passed as pointers, so something like this

    a = ctypes.c_short()
    b = ctypes.c_short()
    fun(ctypes.byref(a), ctypes.byref(b))
    return (a.value, b.value)