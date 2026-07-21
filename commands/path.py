#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with path strings."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import os
    import string
    import sys
    import tempfile
    from typing import Any, Optional, Tuple, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value
from .module import LazyModule, LazyProperty
__version__ = "2.8.0"
if not TYPE_CHECKING:
    os = LazyModule("os")
    string = LazyModule("string")
    sys = LazyModule("sys")
    tempfile = LazyModule("tempfile")
OS = LazyProperty(".os", "OS")
Console = LazyProperty(".console", "Console")
Str = LazyProperty(".str", "Str")
Print = LazyProperty(".print", "Print")
File = LazyProperty(".file", "File")

backslash = LazyProperty(".const", "backslash")


class Path:
    """Class with functions to work with path strings."""

    _path: Optional[str]

    def __init__(self, *paths: Any) -> None:
        self._path = None
        if paths:
            self._path = self.combine(*paths)

    @property
    def string(self) -> Optional[str]:
        """Return the stored path string."""
        return self._path

    def append(self, *paths: Any) -> "Path":
        """Append path parts to the stored path."""
        if self._path is None and paths:
            self._path = self.combine(*paths)
        elif paths:
            self._path = self.combine(self._path, *paths)
        return self

    def __truediv__(self, other: Any) -> "Path":
        """Return a new Path by joining with another part."""
        return Path(self._path, other)

    def __str__(self) -> str:
        """Return the path as a string."""
        return str(self._path)

    def __repr__(self) -> str:
        """Return the debug representation of the path."""
        return f"Path({self._path})"

    @classmethod
    def full(cls, path: Any) -> str:
        """Return an absolute path for the given input.

        <br>`param path` string, partial path
        <br>`return` string, full path
        """
        return str(os.path.abspath(path))

    @classmethod
    def get_real_path(cls, __file__: Any) -> str:
        """Use for storing settings paths.

        <br>`return` string, path of input filepath
        """
        return str(os.path.realpath(__file__))

    @classmethod
    def commands(cls) -> str:
        """Use for locating command module paths.

        <br>`return` string, path of this module
        """
        return os.path.dirname(cls.get_real_path(__file__))

    @classmethod
    def working(cls) -> str:
        """Return the current working directory.

        <br>`return` string, path to working directory
        """
        return os.getcwd()

    @classmethod
    def combine(cls, path_first_path: Any, *paths: Any) -> str:  # todo add support for \\? on Windows
        """Create a full path string from parts.

        <br>`param path_first_path` string, first part of path
        <br>`param paths` strings, path shards to create full path string
        <br>`return` string, path that can be used in shell or whatever
        """
        # Convert pathlib objects (WindowsPath, PosixPath) to strings
        path_first_path = str(path_first_path)
        is_windows = getattr(OS, "_windows", None)
        if is_windows is None:
            is_windows = bool(getattr(OS, "windows", False))
        sep = str(backslash)
        looks_windows = path_first_path.startswith(sep) or (
            len(path_first_path) >= 2 and path_first_path[1] == ':'
        )
        if is_windows or looks_windows:
            sep = str(backslash)
            if path_first_path == sep:  # support for smb windows paths like \\ip_or_pc\dir\
                path = sep * 2
                for path_part in paths:
                    part = str(path_part).strip(sep)
                    if path == sep * 2:
                        path = path + part
                    else:
                        path = path.rstrip(sep) + sep + part
                return str(path)
            elif path_first_path == "~":
                path = cls.home()
            elif len(path_first_path) == 2 and path_first_path[0] in string.ascii_letters and path_first_path[1] == ':':
                path = path_first_path + sep
            else:
                path = path_first_path
            for path_part in paths:
                path = path.rstrip(sep) + sep + str(path_part).lstrip(sep)
            return str(path)

        if path_first_path == "~":
            path = cls.home()
        elif path_first_path == "/":  # explicit absolute path on Unix
            path = "/"
        else:
            # Keep it relative - don't add root slash implicitly
            path = path_first_path
        for path_part in paths:
            path = os.path.join(str(path), str(path_part))
        return str(path)

    @classmethod
    def home(cls) -> str:
        """Return the user's home directory."""
        return str(os.path.expanduser("~"))

    @classmethod
    def get_parent(cls, path: Any) -> str:
        """Return the parent folder of a path.

        <br>`param path` string (with path)
        <br>`return` string (parent path to input one)
        """
        return str(os.path.split(path)[0])

    @classmethod
    def set_working(cls, path: Any, verbose: bool = False) -> None:
        """Change the current working directory.

        If verbose is enabled, prints directory.
        <br>`param path` string, path to new working directory
        <br>`param verbose` boolean, suppress print to console
        <br>`return` None
        """
        os.chdir(path)
        if verbose:
            Print.debug("os.getcwd()  # current directory is", os.getcwd())

    @classmethod
    def add_before_extension(cls, filepath: str, infix: Any) -> str:
        """Insert text before a filename extension.

        <br>`param path`
        <br>`param infix`
        <br>`return`
        """
        extension = File.get_extension(filepath)
        filepath_without_extension = filepath.rstrip(extension)
        return filepath_without_extension + str(infix) + str(extension)

    @classmethod
    def python(cls) -> str:
        """Return the current Python executable path."""
        return str(sys.executable)

    @classmethod
    def temp(cls) -> str:
        """Return a temporary directory path."""
        if getattr(OS, "macos", False):
            return "/tmp"
        if getattr(OS, "linux", False):
            return "/tmp"
        if getattr(OS, "windows", False):
            return str(tempfile.gettempdir())
        return str(tempfile.gettempdir())

    @classmethod
    def safe__file__(cls, __file__: Any) -> str:
        """Return a real path for __file__."""
        return str(os.path.realpath(__file__))

    @classmethod
    def separator(cls) -> str:
        """Return the OS path separator."""
        return str(os.sep)

    @classmethod
    def split(cls, path: Any) -> Tuple[str, str]:
        """Split a path into directory and basename."""
        return os.path.split(path)
