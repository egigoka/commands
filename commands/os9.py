#! python3
# -*- coding: utf-8 -*-
"""Internal module to check some environment properties
"""
__version__ = "3.7.0"


class OS:  # pylint: disable=too-few-public-methods
    """Class with some environment properties
    """

    def __init__(self):
        self._is_python3 = None
        self._python_version_major = None
        self._python_commandline_version = None
        self._sys_platform = None
        self._windows = None
        self._windows_version = None
        self._linux = None
        self._name = None
        self._macos = None
        self._architecture = None
        self._python_implementation = None
        self._nt_family = None
        self._unix_family = None
        self._display = None
        self._running_in_repl = None
        self._cyrillic_support = None
        self._hostname = None

    @property
    def is_python3(self):
        if self._is_python3 is None:
            import sys
            self._is_python3 = sys.version_info >= (3, 0)
        return self._is_python3

    @property
    def python_version_major(self):
        if self._python_version_major is None:
            import sys
            self._python_version_major = sys.version_info.major
        return self._python_version_major

    @property
    def python_commandline_version(self):
        if self._python_commandline_version is None:
            self._python_commandline_version = ""
            if self.is_python3:
                self._python_commandline_version = "3"
        return self._python_commandline_version

    @property
    def sys_platform(self):
        if self._sys_platform is None:
            import sys
            self._sys_platform = sys.platform
        return self._sys_platform

    @property
    def windows(self):
        if self._windows is None:
            self._windows = self.sys_platform == "win32" or self.sys_platform == "cygwin"
        return self._windows

    @property
    def windows_version(self):
        if self._windows_version is None:
            import sys
            self._windows_version = sys.getwindowsversion().major
        return self._windows_version

    @property
    def linux(self):
        if self._linux is None:
            self._linux = self.sys_platform == "linux" or self.sys_platform == "linux2"
        return self._linux

    @property
    def macos(self):
        if self._macos is None:
            self._macos = self.sys_platform == "darwin"
        return self._macos

    @property
    def name(self):
        if self._name is None:
            if self.sys_platform == "linux" or self.sys_platform == "linux2":
                self._name = "linux"
            elif self.sys_platform == "win32" or self.sys_platform == "cygwin":
                self._name = "windows"
            elif self.sys_platform == "darwin":
                self._name = "macos"
            else:
                self._name = "unknown"
        return self._name

    @property
    def architecture(self):
        if self._architecture is None:
            import platform
            self._architecture = platform.architecture()[0]
        return self._architecture

    @property
    def python_implementation(self):
        if self._python_implementation is None:
            import platform
            if platform.python_implementation == "PyPy":
                self._python_implementation = "pypy"
            else:
                self._python_implementation = "cpython"
        return self._python_implementation

    @property
    def nt_family(self):
        if self._nt_family is None:
            self._nt_family = self.windows
        return self._nt_family

    @property
    def unix_family(self):
        if self._unix_family is None:
            self._unix_family = self.macos or self.linux
        return self._unix_family

    @property
    def display(self):
        if self._display is None:
            try:
                if self.linux:
                    from Xlib.display import Display
                self._display = True
            except ImportError:
                self._display = False
        return self._display

    @property
    def running_in_repl(self):
        if self._running_in_repl is None:
            import sys
            if hasattr(sys, "ps1") and hasattr(sys, "ps2"):
                self._running_in_repl = True
            else:
                self._running_in_repl = False
        return self._running_in_repl

    @property
    def cyrillic_support(self):
        if self._cyrillic_support is None:
            self._cyrillic_support = False
            try:
                # if windows:
                # cyr_line = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
                cyr_line = "йЙ"
                import sys
                if self.windows and sys.version_info < (3, 6):
                    try:
                        import win_unicode_console  # pylint: disable=import-error
                        win_unicode_console.enable()
                    except:  # pylint: disable=bare-except
                        pass
                for cyr_symbol in cyr_line:
                    print(cyr_symbol * 2 + "\r", end="")
                print("  \r", end="")
                self._cyrillic_support = True
            except (UnicodeEncodeError, PermissionError) as err:
                pass
        return self._cyrillic_support

    @property
    def hostname(self):
        if self._hostname is None:
            import socket
            self._hostname = socket.gethostname()
        return self._hostname

    @staticmethod
    def walk(top, topdown=True, onerror=None, followlinks=False):
        import os
        from .dir9 import Dir
        if not Dir.exist(top):
            raise FileNotFoundError(f"Directory {top} doesn't exist")
        return os.walk(top=top, topdown=topdown, onerror=onerror, followlinks=followlinks)

    @staticmethod
    def system(command: str, verbose: bool = False):
        import os

        if verbose:
            from .print9 import Print
            Print.colored(command, "blue")

        return os.system(command)

    @property
    def args(self):
        import sys
        return sys.argv

    @property
    def env(self):
        import os
        return os.environ

    @staticmethod
    def where(*args, **kwargs):
        import shutil
        return shutil.which(*args, **kwargs)

    @staticmethod
    def exit(__status):
        import sys
        sys.exit(__status)


OS = OS()
