#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Path:
    @staticmethod
    def full(path):
        import os
        return os.path.abspath(path)

    @staticmethod
    def commands8():
        import os
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def working():
        import os
        return os.getcwd()

    @classmethod
    def extend(cls, *paths, debug=False):  # paths input strings of path pieces, return
        # d string with path, good for OS
        import os
        for path_part in paths:
            try:
                path = os.path.join(str(path), str(path_part))
            except NameError:  # first path piece is very important
                from .os8 import OS
                from .const8 import backslash
                from .print8 import Print
                if (OS.windows) and path_part == backslash:  # support for smb windows paths like \\ip_or_pc\dir\
                    path = backslash * 2
                elif (OS.windows) and (len(path_part) <= 3):
                    path = os.path.join(path_part, os.sep)
                elif OS.windows:
                    path = path_part
                    if debug: Print.debug("path", path, "path_part", path_part)
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
    def home():  # return path of home directory of current user. Not tested in
        # d linux.
        # todo test in lunux!
        from .os8 import OS
        from .console8 import Console
        from .const8 import newline, newline2
        if OS.windows:
            path = Console.get_output(r"echo %userprofile%")
            path = path.rstrip(newline2)
        else:
            path = Console.get_output("echo $HOME", split_lines=True)[0]
            path = path.rstrip(newline)
        return path

    @staticmethod
    def set_current(path, quiet=True):
        """changes current working directory. If quiet is disabled, prints
        directory.
        """
        import os
        os.chdir(path)
        if not quiet:
            from .print8 import Print
            Print.debug("os.getcwd()  # current directory is", os.getcwd())