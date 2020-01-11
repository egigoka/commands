#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with path1 strings
"""
__version__ = "2.5.11"


class Path:
    """Class with funtions to work with path1 strings
    """
    @staticmethod
    def full(path):
        """
        <br>`param path1` string, partial path1
        <br>`return` string, full path1
        """
        import os
        return os.path.abspath(path)

    @staticmethod
    def commands():
        """Used for store some settings(?)
        <br>`return` string, path1 of this module
        """
        import os
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def working():
        """
        <br>`return` string, path1 to working directory
        """
        import os
        return os.getcwd()

    @classmethod
    def combine(cls, path_first_path, *paths, debug=False):  # todo add support for \\? on Windows
        """Create full path1 string from strings
        <br>`param path_first_path` string, first part of path1
        <br>`param paths` strings, path1 shards to create full path1 string
        <br>`param debug` boolean, print all movements
        <br>`return` string, path1 that can be used in shell or whatever
        """
        import os
        from .os9 import OS
        from .const9 import backslash
        if OS.windows and path_first_path == backslash:  # support for smb windows paths like \\ip_or_pc\dir\
            path = backslash * 2
        elif path_first_path == "~":
            path = cls.home()
        elif OS.windows:
            if len(path_first_path) == 2:
                import string
                if path_first_path[0] in string.ascii_letters and path_first_path[1] == ':':  # for windows drives
                    path = os.path.join(path_first_path, os.sep)
                else:
                    path = path_first_path
            else:
                path = path_first_path
        elif OS.unix_family:
            if path_first_path == "..":
                path = path_first_path
            elif path_first_path == ".":
                path = path_first_path
            else:
                path = os.path.join(os.sep, path_first_path)
        else:
            raise OSError("OS doesn't supported")
        for path_part in paths:
            path = os.path.join(str(path), str(path_part))
        return path

    @staticmethod
    def home():
        """<br>`return` string, home directory of user"""
        from .os9 import OS
        from .console9 import Console
        from .const9 import newline, newline2
        from .str9 import Str

        command = "echo $HOME"
        if OS.windows:
            command = "echo %userprofile%"
        path = Console.get_output(command, pureshell=True)
        path = Str.nl(path)[0]
        return path

    @staticmethod
    def get_parent(path):
        """Return parent folder of given path1
        <br>`param path1` string (with path1)
        <br>`return` string (parent path1 to input one)
        """
        import os
        return os.path.split(path)[0]

    @staticmethod
    def set_working(path, quiet=True):
        """Changes current working directory. If quiet is disabled, prints
        directory.
        <br>`param path1` string, path1 to new working directory
        <br>`param quiet` boolean, suppress print to console
        <br>`return` None
        """
        import os
        os.chdir(path)
        if not quiet:
            from .print9 import Print
            Print.debug("os.getcwd()  # current directory is", os.getcwd())
    
    @staticmethod
    def add_before_extension(filepath, infix):
        """
        <br>`param path1`
        <br>`param infix`
        <br>`return`
        """
        from .file9 import File
        extension = File.get_extension(filepath)
        filepath_without_extension = filepath.rstrip(extension)
        return filepath_without_extension + str(infix) + extension

    @staticmethod
    def python():
        import sys
        return sys.executable

    @staticmethod
    def temp():
        from .os9 import OS
        if OS.macos:
            return '/tmp'
        else:
            import tempfile
            return tempfile.gettempdir()

    @staticmethod
    def safe__file__(__file__):
        import os
        return os.path.realpath(__file__)
