# TODO

# DISCUSS

- Turning wch and wstr into ch and str and keep those. Strings in python have utf-8 encoding anyway, it does not makes much sense to keep every standard library. The official curses module for Python only supports addch and addstr (https://docs.python.org/3/library/curses.html#module-curses)

- change cursyncup to wcursyncup

- (done) added wrapper