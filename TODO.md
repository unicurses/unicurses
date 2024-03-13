# TODO

# DISCUSS

- Turning wch and wstr into ch and str and keep those. Strings in python have utf-8 encoding anyway, it does not makes much sense to keep every standard library. The official curses module for Python only supports addch and addstr (https://docs.python.org/3/library/curses.html#module-curses)

- change cursyncup to wcursyncup

- (done) added wrapper

- why do we let users pass in the number of the ascii character? CCHAR gets only either called by user, or called with strings within the code. Moreover ord of bytestring and ord of string return the same value, so I think we should just return ord or raise a custom error if ord fails, and not do type checking

- (done) check if NCURSES or PDCURSES outside of functions, not inside  as the system never changes at runtime.

- what is the need of raising an exception when importing ctypes as failing will raise the same exact exception type?