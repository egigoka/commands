#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
import os
from commands import *
from commands.git9 import Git

__version__ = "1.2.0"

# CHANGING VERSION
version_prefix = '__version__ = "'
version_suffix = '"'
version_path = Path.combine(Path.working(), "commands", "_version.py")  # path to version file
version_text = File.read(version_path)  # text from version file
__version__ = Str.substring(version_text, version_prefix, version_suffix)  # get version from plane text
alphanumber = Str.get_integers(__version__)[-1]  # get only integer of alpha version
old_version = version_prefix + __version__ + version_suffix  # old string, that currently in file
new_version = version_prefix + __version__.replace("-alpha"+str(alphanumber),"-alpha"+str(alphanumber+1))+version_suffix  # new string to replace old version
new_version_text = version_text.replace(old_version, new_version)  # replacing
if OS.windows:  # for not annoying git message about mess with LF and CRLF
    new_version_text = new_version_text.replace(newline, newline2)
File.write(version_path, new_version_text, mode="w")  # write result to file

new_version_string = new_version.lstrip(version_prefix).rstrip(version_suffix)
Print.colored("uploadin", new_version_string, "grey", "on_white")  # print to notice difference
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
Git.update(STRING)

try:
    if OS.windows:
        os.system(r".\update_commands.bat")
    elif OS.unix_family:
        os.system("chmod +X ./update_commands.sh")
        os.system("./update_commands.sh")
except Exception as e:
    print(e)

# updating doc
def safe_run(command):
    print(command)
    out, err = Console.get_output(command, return_merged=False)
    if err:
        print(err)

cwd = os.getcwd()
path = Path.combine("..", "egigoka.github.io")

safe_run(fr"pdoc3 --html commands --force --output-dir {path}")
os.chdir(path)
safe_run("git add .")
safe_run(f'git commit -m "updating documentation for commands to v {new_version_string}"')
safe_run("git fetch --all")
safe_run("git push")
os.chdir(cwd)
