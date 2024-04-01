# TODO

# DISCUSS

- __CCHAR__: why do we let users pass in the number (ord) of the ascii character? CCHAR gets only either called by user, or called within the code with strings, not integers. Moreover ord of bytestring and ord of string return the same value, so I think we should just return ord or raise a custom error if ord fails, and avoid type checking
 
- __PDC_LEAVEOK__: change leaveok so that it actually behaves like ncurses, not sure why we need to use PDC_LEAVEOK, and do we actually need curscr at all? This can still be called by the user anyway, so that is the need? I suggest we make a function that returns curscr and let eveything else depend on scr_id instead. Is it not how curses functions are designed to start with anyway? Also, curscr is in ncurses too!

actually, don't use this gimmicky variable but only rely on leaveok

- (done) wgetch and mvwgetch now return error if the return key = -1. Upon inspecting halfdelay, it looks like -1 corresponds to the value for error when waiting time

# note

to get numbers that are originally passed as pointers, so something like this

    a = ctypes.c_short()
    b = ctypes.c_short()
    fun(ctypes.byref(a), ctypes.byref(b))
    return (a.value, b.value)