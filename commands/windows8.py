#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions
"""
__version__ = "0.2.2"


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

    @classmethod
    def create_user(cls, username, password):
        """Creates user using net user command
        :param username: string
        :param password: string
        :return: None
        """
        import subprocess
        from .console8 import Console
        try:
            output = Console.get_output(f"net user {username} {password} /ADD")
            if "The command completed successfully." in output:
                return
            else:
                raise OSError(f"User {username} failed to create. {output}")
        except subprocess.CalledProcessError as output:
            return cls.create_user(username, password)

    @classmethod
    def remove_user(cls, username):  # remove only users from json file
        """Removes user using net user command
        :param username: string
        :param password: string
        :return: None
        """
        import subprocess
        import time
        from .console8 import Console
        try:
            output = Console.get_output(f"net user {username} /DELETE")
            time.sleep(0.1)
            if "The command completed successfully." in output:
                return
            else:
                raise OSError(f"User {username} failed to remove. {output}")
        except subprocess.CalledProcessError as output:
            return cls.remove_user(username)