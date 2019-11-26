#! python3
# -*- coding: utf-8 -*-
"""Internal module to check some environment properties
"""
__version__ = "3.1.0"


class OS:  # pylint: disable=too-few-public-methods
    """Class with some environment properties
    """
    @property
    def is_python3(self):
        try:
            return self._is_python3
        except AttributeError:
            import sys
            self._is_python3 = sys.version_info >= (3, 0)
            return self._is_python3

    @property
    def python_version_major(self):
        try:
            return self._python_version_major
        except AttributeError:
            import sys
            self._python_version_major = sys.version_info.major
            return self._python_version_major

    @property
    def python_commandline_version(self):
        try:
            return self._python_commandline_version
        except AttributeError:
            self._python_commandline_version =  ""
            if self.is_python3:
                self._python_commandline_version = "3"
            return self._python_commandline_version

    @property
    def sys_platfrom(self):
        try:
            return self._sys_platfrom
        except AttributeError:
            import sys
            self._sys_platfrom = sys.platform
            return self._sys_platfrom

    @property
    def windows(self):
        try:
            return self._windows
        except AttributeError:
            self._windows = self.sys_platfrom == "win32" or self.sys_platfrom == "cygwin"
            return self._windows

    @property
    def windows_version(self):
        try:
            return self._windows_version
        except AttributeError:
            import sys
            self._windows_version = sys.getwindowsversion().major
            return self._windows_version

    @property
    def linux(self):
        try:
            return self._linux
        except AttributeError:
            self._linux = self.sys_platfrom == "linux" or self.sys_platfrom == "linux2"
            return self._linux

    @property
    def macos(self):
        try:
            return self._macos
        except AttributeError:
            self._macos = self.sys_platfrom == "darwin"
            return self._macos

    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            if self.sys_platfrom == "linux" or self.sys_platfrom == "linux2":
                self._name = "linux"
            elif self.sys_platfrom == "win32" or self.sys_platfrom == "cygwin":
                self._name = "windows"
            elif self.sys_platfrom == "darwin":
                self._name = "macos"
            else:
                self._name = "unknown"
            return self._name

    @property
    def architecture(self):
        try:
            return self._architecture
        except AttributeError:
            import platform
            self._architecture = platform.architecture()[0]
            return self._architecture

    @property
    def python_implementation(self):
        try:
            return self._python_implementation
        except AttributeError:
            import platform
            if platform.python_implementation == "PyPy":
                self._python_implementation = "pypy"
            else:
                self._python_implementation = "cpython"
            return self._python_implementation


    @property
    def nt_family(self):
        try:
            return self._nt_family
        except AttributeError:
            self._nt_family = self.windows
            return self._nt_family


    @property
    def unix_family(self):
        try:
            return self._unix_family
        except AttributeError:
            self._unix_family = self.macos or self.linux
            return self._unix_family


    @property
    def display(self):
        try:
            return self._display
        except AttributeError:
            try:
                if self.linux:
                    from Xlib.display import Display
                self._display = True
            except ImportError:
                self._display = False
            return self._display


    @property
    def running_in_repl(self):
        try:
            return self._running_in_repl
        except AttributeError:
            try:
                import sys
                sys.ps1  # pylint: disable = pointless-statement, no-member
                sys.ps2  # pylint: disable = pointless-statement, no-member
                self._running_in_repl = True
            except AttributeError:
                self._running_in_repl = False
            return self._running_in_repl


    @property
    def cyrillic_support(self):
        try:
            return self._cyrillic_support
        except AttributeError:
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
        try:
            return self._hostname
        except AttributeError:
            import socket
            self._hostname = socket.gethostname()
            return self._hostname

    @staticmethod
    def walk(top, topdown=True, onerror=None, followlinks=False):
        import os
        return os.walk(top=top, topdown=topdown, onerror=onerror, followlinks=followlinks)


OS = OS()