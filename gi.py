#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
from commands import *
from commands.git8 import Git
from commands.print8 import Print

# CHANGING VERSION
version_prefix = '__version__ = "'
version_suffix = '"'
version_path = Path.extend(Path.working(), "commands", "_version.py")  # path to version file
version_text = File.read(version_path)  # text from version file
__version__ = Str.substring(version_text, version_prefix, version_suffix)  # get version from plane text
alphanumber = Str.get_integers(__version__)[-1]  # get only integer of alpha version
old_version = version_prefix + __version__ + version_suffix  # old string, that currently in file
new_version = version_prefix + __version__.replace("-alpha"+str(alphanumber),"-alpha"+str(alphanumber+1))+version_suffix  # new string to replace old version
new_version_text = version_text.replace(old_version, new_version)  # replacing
File.write(version_path, new_version_text, mode="w")  # write result from file

Print.colored("uploadin",  new_version.lstrip(version_prefix).rstrip(version_suffix), "grey", "on_white")  # print to notice difference
# CHANGING VERSION END


ARGUMENTS = list(sys.argv)
ARGUMENTS.pop(0)
STRING = "small update (default message)"
try:
    ARGUMENTS[0]  # pylint: disable=pointless-statement
    STRING = ""
    for arg in ARGUMENTS:
        STRING += arg + " "
    STRING = STRING.rstrip(" ")
except IndexError:
    INPUT_STRING = input("Enter a description or press Enter to default message: ")
    if INPUT_STRING:
        STRING = INPUT_STRING
Git.update(STRING)