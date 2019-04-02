#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions
"""
__version__ = "0.3.7"


class Windows:
    """Class to work with Windows-specific functions
    """
    @staticmethod
    def lock():
        """Locking windows workstation, doesn't work with Windows 10
        <br>`return` None
        """
        from .os9 import OS
        if OS.windows_version and (OS.windows_version != 10):
            import ctypes
            ctypes.windll.LockWorkStation()  # todo fix Windows 10
        else:
            raise OSError("Locking work only on Windows < 10")

    @staticmethod
    def set_cmd_code_page(code_page):
        import os
        import subprocess
        subprocess.Popen(f"chcp {code_page}".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        os.system("set PYTHONIOENCODING = utf - 8")
        return code_page

    @staticmethod
    def get_cmd_code_page():
        import subprocess
        from .str9 import Str
        out, err = subprocess.Popen("chcp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if err:
            return "Error getting current codepage"
        try:
            out = Str.substring(out.lower(), "active code page:").strip()
            return out
        except KeyError:
            return "Cannot get current codepage"

    @classmethod
    def fix_unicode_encode_error(cls, safe=False):
        """Fix UnicodeConsoleError on old versions of Python
        <br>`return` None
        """
        previous_codepage = cls.get_cmd_code_page()
        try:
            code_page = cls.set_cmd_code_page(65001)
            print("йЙ", end="\n")
            print("  ", end="\n")
            return code_page
        except:
            from .print9 import Print
            Print.debug(previous_codepage)
            if previous_codepage >= 0:
                cls.set_cmd_code_page(previous_codepage)
                from .os9 import OS
                OS.cyrillic_support = False
                return previous_codepage
            if not safe:
                raise UnicodeEncodeError(f"Cannot use codepage 65001, returning to {previous_codepage}, you can set other by Windows.set_cmd_code_page")
            return code_page

    @staticmethod
    def user_exists(self, username):
        """
        <br>`param username` string
        <br>`return` boolean, existance of local user
        """
        import subprocess
        from .console9 import Console
        try:
            Console.get_output(f"net user {username}")
            return True
        except subprocess.CalledProcessError:
            return False

    def _user(self, username, password=None, create=False, remove=False, retry_cnt=0):
        """Creates or removes user user using net user command
        <br>`param username` string
        <br>`param password` string
        <br>`param create` boolean, True for create user
        <br>`param remove` boolean, True for remove user
        <br>`param retry_cnt` int, internally used to not raise RecursionError
        <br>`return` None
        """
        import subprocess
        from .console9 import Console
        retry_times = 5

        if not isinstance(username, str):
            raise TypeError(f"Username must be string, got {username}, of {type(username)}")

        try:
            if create:
                if self.user_exists(username):
                    raise OSError(f"User {username} already exists.")
                if not password:
                    raise ValueError("Password can't be empty")
                command = f"net user {username} {password} /ADD"
            elif remove:
                if not self.user_exists(username):
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
                return self._user(username, password, create, remove, retry_cnt)
            else:
                if create:
                    raise OSError(f"User {username} failed to create.")
                elif remove:
                    raise OSError(f"User {username} failed to remove.")

    def create_user(self, username, password):
        """Creates user using net user command
        <br>`param username` string
        <br>`param password` string
        <br>`return` None
        """
        return self._user(username=username, password=password, create=True)

    def remove_user(self, username):  # remove only users from json file
        """Removes user using net user command
        <br>`param username` string
        <br>`return` None
        """
        return self._user(username=username, remove=True)

    @staticmethod
    def dump_auditpol(filename=None, category="*", fastname=None, quiet=False):
        from .file9 import File
        from .console9 import Console
        from .time9 import Time
        import subprocess
        if not filename:
            filename = f"auditpol_{Time.dotted()}.txt"
        if fastname:
            filename = f"auditpol_{Time.dotted()}--{fastname}.txt"
        try:
            output = Console.get_output(f"auditpol /get /category:{category}")
        except subprocess.CalledProcessError:
            raise OSError("Try to run under elevated commandline")
        File.write(filename, output)
        if not quiet:
            print(f"Audit politics saved to {filename}")
