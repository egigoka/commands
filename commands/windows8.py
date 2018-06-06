#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions
"""
__version__ = "0.1.2"


class Windows:
    """Class to work with Windows-specific functions
    """
    @staticmethod
    def lock():
        """Locking windows workstation, doesn't work with Windows 10
        :return: None
        """
        from .os8 import OS
        if OS.windows_version and (OS.windows_version != 10):
            import ctypes
            ctypes.windll.LockWorkStation()  # todo fix Windows 10
        else:
            raise OSError("Locking work only on Windows < 10")

    @staticmethod
    def fix_unicode_encode_error(quiet=""):
        """Fix UnicodeConsoleError on old versions of Python
        :param quiet: boolean, suppress print to console
        :return: None
        """
        import os
        if quiet:
            quiet = " > null"
        os.system("chcp 65001" + quiet)
        os.system("set PYTHONIOENCODING = utf - 8")
