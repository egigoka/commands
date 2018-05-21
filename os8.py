#! python3
# -*- coding: utf-8 -*-
# http://python.su/forum/topic/15531/?page=1#post-93316
import sys  # static module
import platform  # static module
__version__ = "2.0.1"


class OS:
    sys_version_info = sys.version_info
    is_python3 = sys.version_info >= (3, 0)  # d boolean
    python_implementation = None # d string with name of python implementation: "cpython" or "pypy"
    python_version_major = sys.version_info.major # d int of major python version
    python_commandline_version = ""
    if is_python3:
        python_commandline_version = "3" # d string of addable "3" to commandline apps if python is 3rd version

    nt_family = False
    unix_family = False

    windows = False
    macos = False
    linux = False

    windows_version = None  # d only on Windows, integer of major version of Windows

    display = None  # d didn't work yet
    cyrillic_support = None  # d boolean variable of cyrrilic output support

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

    try:  # TODO make this work!
        if linux:
            from Xlib.display import Display
        display = True
    except ImportError:
        display = False
        print("Your system haven't display -_-")

    try:
        #if windows:
        #cyrline = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
        cyrline = "йЙ"
        if windows and sys.version_info < (3,6):
            try:
                import win_unicode_console
                win_unicode_console.enable()
            except:
                pass
        for cyrsybol in cyrline:
            print(cyrsybol*2, end="\r")
        print("  ", end="\r")
        cyrillic_support = True
    except UnicodeEncodeError as err:
        cyrillic_support = False
        # print (err)
        print ("Your system doesn't properly work with cyrrilic -_-")
