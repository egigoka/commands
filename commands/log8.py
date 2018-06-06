#! python3
# -*- coding: utf-8 -*-
"""Internal module for logging
"""
__version__ = "0.0.5"


def plog(logfile, description, custom_time=None, quiet=False, backup=True):
    """Write string with time and description to file, also print it to console
    :param logfile: file where to write log
    :param description: string with description of event
    :param custom_time: int with unix_time, used to write to log with not current time
    :param quiet: boolean, suppress print to console
    :param backup: boolean, means to backup log before new event adding or not (too much backups can use all disk space)
    :return:
    """
    from .file8 import File
    from .time8 import Time
    from .const8 import newline
    if not quiet:
        print(description)
    File.create(logfile)
    if backup:
        File.backup(logfile, quiet=True)
    file = open(logfile, "a")
    if custom_time:
        file.write(Time.dotted(custom_time) + " " + str(description) + newline)
    else:
        file.write(Time.dotted() + " " + str(description) + newline)
    file.close()
