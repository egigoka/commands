#! python3
# -*- coding: utf-8 -*-
__version__ = "0.1.0"


class Windows:
    @staticmethod
    def lock():  # locking screen, work only on Windows < 10
        from .os8 import OS
        if OS.windows_version and (OS.windows_version != 10):
            import ctypes
            ctypes.windll.LockWorkStation()  # todo fix Windows 10
        else:
            raise OSError("Locking work only on Windows < 10")

    @staticmethod
    def fix_unicode_encode_error(quiet=""):
            import os
            if quiet:
                quiet = " > null"
            os.system("chcp 65001" + quiet)
            os.system("set PYTHONIOENCODING = utf - 8")
