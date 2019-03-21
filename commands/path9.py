#! python3
# -*- coding: utf-8 -*-
"""Internal module with funtions to work with path strings
"""
__version__ = "2.2.0"


class Path:
    """Class with funtions to work with path strings
    """
    @staticmethod
    def full(path):
        """
        `param path` string, partial path
        `return` string, full path
        """
        import os
        return os.path.abspath(path)

    @staticmethod
    def commands():
        """Used for store some settings(?)
        `return` string, path of this module
        """
        import os
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def working():
        """
        `return` string, path to working directory
        """
        import os
        return os.getcwd()

    @classmethod
    def combine(cls, *paths, debug=False):  # todo add support for \\? on Windows
        """Create full path string from strings
        `param paths` strings, path shards to create full path string
        `param debug` boolean, print all movements
        `return` string, path that can be used in shell or whatever
        """
        import os
        for path_part in paths:
            try:
                path = os.path.join(str(path), str(path_part))  # pylint: disable=used-before-assignment
            except NameError:  # first path piece is very important
                from .os9 import OS
                from .const9 import backslash
                from .print9 import Print
                if OS.windows and path_part == backslash:  # support for smb windows paths like \\ip_or_pc\dir\
                    path = backslash * 2
                elif (OS.windows) and (len(path_part) <= 3):  # todo bug with "." and ".."
                    path = os.path.join(path_part, os.sep)
                elif OS.windows:
                    path = path_part
                    if debug:
                        Print.debug("path", path, "path_part", path_part)
                elif OS.unix_family:
                    if path_part == "..":
                        path = path_part
                    elif path_part == ".":
                        path = path_part
                    elif path_part == "~":
                        path = cls.home()
                    else:
                        path = os.path.join(os.sep, path_part)
                else:
                    raise FileNotFoundError("path_part" + str(path_part) + "is not expected")
        return path

    @staticmethod
    def home():
        """
        `return` string, home directory of user
        """
        from .os9 import OS
        from .console9 import Console
        from .const9 import newline, newline2
        if OS.windows:
            path = Console.get_output("echo %userprofile%", pureshell=True)
            path = path.rstrip(newline2)
        else:
            from .str9 import Str
            path = Str.nl(Console.get_output("echo $HOME", pureshell=True))
            path = path.rstrip(newline)
        return path

    @staticmethod
    def get_parent(path):
        """Return parent folder of given path
        `param path` string (with path)
        `return` string (parent path to input one)
        """
        import os
        return os.path.split(path)[0]

    @staticmethod
    def set_working(path, quiet=True):
        """Changes current working directory. If quiet is disabled, prints
        directory.
        `param path` string, path to new working directory
        `param quiet` boolean, suppress print to console
        `return` None
        """
        import os
        os.chdir(path)
        if not quiet:
            from .print9 import Print
            Print.debug("os.getcwd()  # current directory is", os.getcwd())
    
    @staticmethod
    def add_before_extension(filepath, infix):
        """
        `param path`
        `param infix`
        `return`
        """
        from .file9 import File
        extension = File.get_extension(filepath)
        filepath_without_extension = filepath.rstrip(extension)
        return filepath_without_extension + str(infix) + extension
