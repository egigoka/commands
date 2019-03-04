#! python3
# -*- coding: utf-8 -*-
"""Internal module to check some environment properties
"""
import sys  # static module
import platform  # static module
__version__ = "2.2.1"


class OS:  # pylint: disable=too-few-public-methods
    """Class with some environment properties
    """
    sys_version_info = sys.version_info
    is_python3 = sys.version_info >= (3, 0)
    python_version_major = sys.version_info.major # int of major python version
    python_commandline_version = ""
    if is_python3:
        python_commandline_version = "3" # string of addable "3" to commandline apps if python is 3rd version

    nt_family = False
    unix_family = False

    windows = False
    macos = False
    linux = False

    windows_version = None  # only on Windows, integer of major version of Windows

    display = None  # didn't work yet
    cyrillic_support = None  # boolean variable of cyrrilic output support

    if sys.platform == "linux" or sys.platform == "linux2":
        linux = True
    elif sys.platform == "win32" or sys.platform == "cygwin":
        windows = True
        windows_version = sys.getwindowsversion().major
    elif sys.platform == "darwin":
        macos = True

    if platform.python_implementation == "PyPy":
        python_implementation = "pypy"
    else:
        python_implementation = "cpython"

    if windows:
        nt_family = True
    elif macos or linux:
        unix_family = True

    try:
        if linux:
            from Xlib.display import Display
        display = True
    except ImportError:
        display = False
        print("Your system haven't display -_-")

    @staticmethod
    def running_in_repl():
        try:
            sys.ps1  # pylint: disable = pointless-statement, no-member
            sys.ps2  # pylint: disable = pointless-statement, no-member
            return True
        except AttributeError:
            return False

    try:
        #if windows:
        #cyr_line = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
        cyr_line = "йЙ"
        if windows and sys.version_info < (3, 6):
            try:
                import win_unicode_console  # pylint: disable=import-error
                win_unicode_console.enable()
            except:  # pylint: disable=bare-except
                pass
        for cyr_symbol in cyr_line:
            print(cyr_symbol * 2, end="\r")
        print("  ", end="\r")
        cyrillic_support = True
    except UnicodeEncodeError as err:
        print(err)
        cyrillic_support = False
        # print (err)
        print("Your system doesn't properly work with cyrillic -_-")
