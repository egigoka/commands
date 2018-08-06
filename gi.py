#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with git
"""
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
from commands import *
from commands.git8 import Git

# CHANGING VERSION
version_prefix = '__version__ = "'
version_suffix = '"'
version_path = Path.extend(Path.working(), "commands", "_version.py")
version_text = File.read(version_path)
__version__ = Str.substring(version_text, "")
alphanumber = Str.get_integers(__version__)[-2]
old_version = version_prefix + __version__ + version_suffix
new_version = version_prefix + __version__.replace("-alpha"+str(alphanumber),"-alpha"+str(alphanumber+1))+version_suffix
new_version_text = version_text.replace(old_version, new_version)
# Print.debug("version_text", version_text)
Print.debug("alphanumber", alphanumber)
Print.debug("__version__", __version__)
Print.debug("Str.get_integers(__version__)", Str.get_integers(__version__))
Print.debug("old_version", old_version)
Print.debug("new_version", new_version)
# Print.debug("new_version_text", new_version_text)
File.write(version_path, new_version_text, mode="w")
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