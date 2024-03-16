# TODO

# DISCUSS

- Turning wch and wstr into ch and str and keep those. Strings in python have utf-8 encoding anyway, it does not makes much sense to keep every standard library. The official curses module for Python only supports addch and addstr (https://docs.python.org/3/library/curses.html#module-curses)

- change cursyncup to wcursyncup
- change noutrefresh to wnoutrefresh
- in general, change some names to be more faithful to python.curses and more consistent to prefix=w <-> affect input-specified windows

- (done) added wrapper

- why do we let users pass in the number of the ascii character? CCHAR gets only either called by user, or called with strings within the code. Moreover ord of bytestring and ord of string return the same value, so I think we should just return ord or raise a custom error if ord fails, and not do type checking

- (done) check if NCURSES or PDCURSES outside of functions, not inside as the system never changes at runtime. It is also safer in case the user changes the values of PDCURSES or NCURSES.
 
- what is the need of raising an exception when importing ctypes as failing will raise the same exact exception type?

- either split this into mvwgetkey or remove all unnecessary mv before and make everything into one function optional positional arguments.

- (done) convert value == 1 to bool(value) to be more pythonic

- change leaveok so that it actually behaves like ncurses, not sure why the original author made all these shenanigans, do we actually need curscr at all? so we could just make a function that returns curscr and let eveything depend on scr_id instead.

- make it easier for users to find attributes (for example print them with a specific function or add them to the wiki)

- (done) add some missing functions such as is_scrollok or is_leaveok, they are cross-platform

# note

to get numbers that are originally passed as pointers, so something like this

    a = ctypes.c_short()
    b = ctypes.c_short()
    fun(ctypes.byref(a), ctypes.byref(b))
    return (a.value, b.value)