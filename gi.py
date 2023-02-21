#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
import os
from commands import *
from commands.git9 import Git

__version__ = "1.4.1"


def safe_run(command):
    Print.colored(command, "magenta")
    try:
        out, err = Console.get_output(command, return_merged=False)
        if err:
            Print.colored(err, "red")
            return False
        else:
            return True
    except Exception as err:
        Print.colored(err, "red")
        return False


# CHANGING VERSION
VERSION_CHANGE = "--no-version-change" not in OS.args

version_prefix = '__version__ = "'
version_suffix = '"'
version_path = Path.combine(Path.working(), "commands", "_version.py")  # path to version file
version_text = File.read(version_path)  # text from version file
__version__ = Str.substring(version_text, version_prefix, version_suffix)  # get version from plane text
last_int = Str.get_integers(__version__)[-1]  # get only integer of alpha version
if last_int < 0:
	last_int = -last_int
old_version = version_prefix + __version__ + version_suffix  # old string, that currently in file

if VERSION_CHANGE:
	new_version = version_prefix + Str.rreplace(__version__, last_int, last_int+1, 1) + version_suffix  # new string to replace old version
	new_version_text = version_text.replace(old_version, new_version)  # replacing
	if OS.windows:  # for not annoying git message about mess with LF and CRLF
	    new_version_text = new_version_text.replace(newline, newline2)
	File.write(version_path, new_version_text, mode="w")  # write result to file

	Print.colored("uploadin", new_version_text, "grey", "on_white")  # print to notice difference

	version_string = new_version.lstrip(version_prefix).rstrip(version_suffix)
else:
	version_string = old_version.lstrip(version_prefix).rstrip(version_suffix)
# CHANGING VERSION END

ARGUMENTS = list(sys.argv)
ARGUMENTS.pop(0)
STRING = "small update (default message)"
try:
    TEST = ARGUMENTS[0]
    del TEST
    STRING = ""
    for arg in ARGUMENTS:
        STRING += arg + " "
    STRING = STRING.rstrip(" ")
except IndexError:
    INPUT_STRING = input("Enter a description or press Enter to default message: ")
    if INPUT_STRING:
        STRING = INPUT_STRING
Git.update(STRING, verbose=True)

try:
    if OS.windows:
        safe_run(r".\update_commands.bat")
    elif OS.unix_family:
        safe_run("chmod +X ./update_commands.sh")
        safe_run("sh ./update_commands.sh")
except Exception as e:
    print(e)

# updating doc
cwd = os.getcwd()
path = Path.combine("..", "egigoka.github.io")

# downloading last version
os.chdir(path)
safe_run("git fetch --all")
safe_run("git reset --hard origin/master")

# updating doc
os.chdir(cwd)
if OS.windows:
    if not safe_run("pydoc3"):
        Print.colored("pydoc3.py not in PATH or PATHEXT", "red")
elif OS.unix_family:
    if not OS.where("pdoc3"):
        Print.colored("pdoc3 not in PATH", "red")
else:
    raise NotImplementedError("OS is not supported now")
safe_run(fr"pdoc3 --html commands --force --output-dir {path}")

# upload doc
os.chdir(path)
safe_run("git add .")
safe_run(f'git commit -m "updating documentation for commands to v {version_string}"')
safe_run("git push")
os.chdir(cwd)
