#! python3
# -*- coding: utf-8 -*-
"""Internal module to check some environment properties."""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING, cast
if TYPE_CHECKING:
    import os
    import platform
    import shutil
    import socket
    import sys
    from typing import Any, Iterable, Iterator, List, Mapping

from .module import LazyModule, LazyProperty
__version__ = "3.7.1"
if not TYPE_CHECKING:
    sys = LazyModule("sys")
    platform = LazyModule("platform")
    socket = LazyModule("socket")
    os = LazyModule("os")
    shutil = LazyModule("shutil")
Dir = LazyProperty(".dir", "Dir")
Print = LazyProperty(".print", "Print")

xlib_display = LazyModule("Xlib.display", optional=True)
win_unicode_console = LazyModule("win_unicode_console", optional=True)
ping3 = LazyModule("ping3")


class OS:  # pylint: disable=too-few-public-methods
    """Class with some environment properties."""

    def __init__(self) -> None:
        self._python_version_major: Optional[int] = None
        self._python_commandline_version: Optional[str] = None
        self._sys_platform: Optional[str] = None
        self._windows: Optional[bool] = None
        self._windows_version: Optional[int] = None
        self._linux: Optional[bool] = None
        self._name: Optional[str] = None
        self._macos: Optional[bool] = None
        self._architecture: Optional[str] = None
        self._python_implementation: Optional[str] = None
        self._nt_family: Optional[bool] = None
        self._unix_family: Optional[bool] = None
        self._display: Optional[bool] = None
        self._running_in_repl: Optional[bool] = None
        self._cyrillic_support: Optional[bool] = None
        self._hostname: Optional[str] = None
        self._cwd: Optional[str] = None

    def __call__(self) -> Optional[str]:
        """Return current working directory for quick REPL access."""
        return self.cwd

    @property
    def python_version_major(self) -> int:
        """Return the major Python version."""
        if self._python_version_major is None:
            self._python_version_major = sys.version_info.major
        return self._python_version_major

    @property
    def sys_platform(self) -> str:
        """Return the current sys.platform value."""
        if self._sys_platform is None:
            self._sys_platform = sys.platform
        return self._sys_platform

    @property
    def windows(self) -> bool:
        """Return True if running on Windows."""
        if self._windows is None:
            self._windows = self.sys_platform == "win32" or self.sys_platform == "cygwin"
        return self._windows

    @property
    def windows_version(self) -> Optional[int]:
        """Return the Windows major version if available."""
        if self._windows_version is None:
            if not self.windows:
                raise AttributeError("windows_version is only available on Windows")
            get_windows_version = getattr(sys, "getwindowsversion", None)
            if not callable(get_windows_version):
                raise AttributeError("sys.getwindowsversion is not available")
            self._windows_version = get_windows_version().major  # pylint: disable=not-callable
        return self._windows_version

    @property
    def linux(self) -> bool:
        """Return True if running on Linux."""
        if self._linux is None:
            self._linux = self.sys_platform == "linux" or self.sys_platform == "linux2"
        return self._linux

    @property
    def macos(self) -> bool:
        """Return True if running on macOS."""
        if self._macos is None:
            self._macos = self.sys_platform == "darwin"
        return self._macos

    @property
    def name(self) -> str:
        """Return a normalized OS name string."""
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
    def architecture(self) -> str:
        """Return the system architecture string."""
        if self._architecture is None:
            self._architecture = platform.architecture()[0]
        return self._architecture

    @property
    def python_implementation(self) -> str:
        """Return the Python implementation name."""
        if self._python_implementation is None:
            impl_attr = platform.python_implementation
            impl = impl_attr() if callable(impl_attr) else impl_attr
            if impl == "PyPy":
                self._python_implementation = "pypy"
            else:
                self._python_implementation = "cpython"
        return self._python_implementation

    @property
    def nt_family(self) -> bool:
        """Return True if the OS is in the NT family."""
        if self._nt_family is None:
            self._nt_family = self.windows
        return self._nt_family

    @property
    def unix_family(self) -> bool:
        """Return True if the OS is in the Unix family."""
        if self._unix_family is None:
            self._unix_family = self.macos or self.linux
        return self._unix_family

    @property
    def display(self) -> bool:
        """Return True if a display is available."""
        if self._display is None:
            if self.linux:
                try:
                    __import__("Xlib.display", fromlist=["Display"])
                    self._display = True
                except ImportError:
                    self._display = False
            else:
                self._display = False
        return self._display

    @property
    def running_in_repl(self) -> bool:
        """Return True if running inside a REPL."""
        if self._running_in_repl is None:
            if hasattr(sys, "ps1") and hasattr(sys, "ps2"):
                self._running_in_repl = True
            else:
                self._running_in_repl = False
        return self._running_in_repl

    @property
    def cyrillic_support(self) -> bool:
        """Detect whether console supports Cyrillic output."""
        if self._cyrillic_support is None:
            self._cyrillic_support = False
            try:
                # if windows:
                # cyr_line = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
                cyr_line = "йЙ"
                if self.windows and sys.version_info < (3, 6):
                    try:
                        if win_unicode_console:
                            win_unicode_console.enable()
                    except Exception:  # pylint: disable=bare-except
                        pass
                for cyr_symbol in cyr_line:
                    print(cyr_symbol * 2 + "\r", end="")
                print("  \r", end="")
                self._cyrillic_support = True
            except (UnicodeEncodeError, PermissionError):
                pass
        return self._cyrillic_support

    @property
    def hostname(self) -> str:
        """Return the current hostname."""
        if self._hostname is None:
            self._hostname = socket.gethostname()
        return self._hostname

    @property
    def cwd(self) -> str:
        """Return the current working directory."""
        if self._cwd is None:
            self._cwd = os.getcwd()
        return self._cwd

    def chdir(self, path: str) -> str:
        """Change working directory and update cached cwd."""
        os.chdir(path)
        self._cwd = os.getcwd()
        return self._cwd

    @classmethod
    def walk(
        cls,
        top: str,
        topdown: bool = True,
        onerror: Optional[Any] = None,
        follow_links: bool = False
    ) -> Iterator[Any]:
        """Walk a directory tree, yielding paths."""
        if not Dir.exist(top):
            raise FileNotFoundError(f"Directory {top} doesn't exist")
        return os.walk(top=top, topdown=topdown, onerror=onerror, followlinks=follow_links)

    @classmethod
    def system(cls, command: str, verbose: bool = False) -> int:
        """Run a system command and return the exit code."""
        if verbose:
            Print.colored(command, "blue")

        return os.system(command)

    @staticmethod
    def ping(*args: Any, **kwargs: Any) -> Any:
        """Ping a host using ping3."""
        return ping3.ping(*args, **kwargs)

    @property
    def args(self) -> List[str]:
        """Return command-line arguments."""
        return list(sys.argv)

    @property
    def env(self) -> Mapping[str, str]:
        """Return environment variables mapping."""
        return os.environ

    @classmethod
    def where(cls, *args: Any, **kwargs: Any) -> Optional[str]:
        """Locate a command in PATH."""
        return cast(Optional[str], shutil.which(*args, **kwargs))

    @classmethod
    def exit(cls, __status: Any) -> None:
        """Exit the process with the provided status."""
        sys.exit(__status)


OS = OS()  # type: ignore[assignment,misc]
