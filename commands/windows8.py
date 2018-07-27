#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions
"""
__version__ = "0.2.4"


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
    def user_exists(cls, username):
        """
        :param username: string
        :return: boolean, existance of local user
        """
        import subprocess
        from .console8 import Console
        try:
            Console.get_output(f"net user {username}")
            return True
        except subprocess.CalledProcessError:
            return False

    @classmethod
    def _user(cls, username, password=None, create=False, remove=False, retry_cnt=0):
        """Creates or removes user user using net user command
        :param username: string
        :param password: string
        :param create: boolean, True for create user
        :param remove: boolean, True for remove user
        :param retry_cnt: int, internally used to not raise RecursionError
        :return: None
        """
        import subprocess
        from .console8 import Console
        retry_times = 5
        try:
            if create:
                if cls.user_exists(username):
                    raise OSError(f"User {username} already exists.")
                if not password:
                    raise ValueError("Password can't be empty")
                command = f"net user {username} {password} /ADD"
            elif remove:
                if not cls.user_exists(username):
                    raise OSError(f"User {username} already doesn't exists.")
                command = f"net user {username} /DELETE"
            output = Console.get_output(command)
            if "The command completed successfully." in output:
                return
            else:
                if create:
                    raise OSError(f"User {username} failed to create. {output}")
                elif remove:
                    raise OSError(f"User {username} failed to remove. {output}")
        except subprocess.CalledProcessError as output:
            if retry_cnt < retry_times:
                retry_cnt += 1
                return cls._user(username, password, create, remove, retry_cnt)
            else:
                if create:
                    raise OSError(f"User {username} failed to create.")
                elif remove:
                    raise OSError(f"User {username} failed to remove.")

    @classmethod
    def create_user(cls, username, password):
        """Creates user using net user command
        :param username: string
        :param password: string
        :return: None
        """
        return cls._user(username=username, password=password, create=True)

    @classmethod
    def remove_user(cls, username):  # remove only users from json file
        """Removes user using net user command
        :param username: string
        :return: None
        """
        return cls._user(username=username, remove=True)