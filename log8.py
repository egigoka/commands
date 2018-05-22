#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"

def plog(logfile, logstring="some shit happened", customtime=None, quiet=False, backup=True):
    from .file8 import File
    from .time8 import Time
    from .const8 import newline
    if not quiet:
        print(logstring)
    File.create(logfile)
    if backup:
        File.backup(logfile, quiet=True)
    file = open(logfile, "a")
    if customtime:
        file.write(Time.rustime(customtime) + " " + str(logstring) + newline)
    else:
        file.write(Time.rustime() + " " + str(logstring) + newline)
    file.close()
