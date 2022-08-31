#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions
"""
__version__ = "0.7.4"


class Windows:
    """Class to work with Windows-specific functions
    """

    class RemoteSystem:
        def __init__(self, hostname, username, password, port=None, transport="ntlm"):
            import winrm
            # FIX winrm #

            def fix_run_ps(self, script):
                from base64 import b64encode
                encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
                rs = self.run_cmd('powershell -encodedcommand {0}'.format(encoded_ps))
                if len(rs.std_err):
                    rs.std_err = self._clean_error_msg(rs.std_err.decode('utf-8'))
                return rs

            winrm.Session.run_ps = fix_run_ps

            # END FIX winrm #

            if port is None:
                port = 5986 if transport == 'ssl' else 5985

            self.session = winrm.Session(fr"{hostname}:{port}", auth=(username, password), transport=transport)

        def ps(self, script):
            output = self.session.run_ps(script)
            if output.std_err.startswith("#< CLIXML\r\n"):
                output.std_err = output.std_err[len("#< CLIXML\r\n"):]

            out = output.std_out.decode()
            err = output.std_err
            return out, err, output.status_code

        def cmd(self, program, *args):
            from commands.list9 import List
            args = List.to_strings(args)
            output = self.session.run_cmd(program, args)

            out = output.std_out.decode()
            err = output.std_err.decode()
            return out, err, output.status_code


    @staticmethod
    def lock():
        """Locking Windows workstation, doesn't work with Windows 10
        <br>`return` None
        """
        from .os9 import OS
        if OS.windows_version and (OS.windows_version != 10):
            import ctypes
            ctypes.windll.LockWorkStation()  # todo fix Windows 10
        else:
            raise OSError("Locking work only on Windows < 10")

    @classmethod
    def set_cmd_code_page(cls, code_page):
        import os
        import subprocess
        subprocess.Popen(f"chcp {code_page}".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        os.system("set PYTHONIOENCODING = utf - 8")
        cls.get_cmd_code_page()  # it's fucking magick, don't touch
        return code_page

    @staticmethod
    def get_cmd_code_page(debug=False):
        import subprocess
        out, err = subprocess.Popen("chcp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if err:
            return "Error getting current codepage"
        try:
            from .str9 import Str
            if debug:
                print(out)
            out = Str.substring(out, ": ", "\r\n")
            if debug:
                print(out)
            return int(out)
        except KeyError:
            return "Cannot get current codepage"

    @classmethod
    def fix_unicode_encode_error(cls, safe=False):
        """Fix UnicodeConsoleError on old versions of Python
        <br>`return` int, current code_page number
        """
        from .path9 import Path
        from .file9 import File
        from .print9 import Print
        lockfile = Path.combine(Path.commands(), ".windows_codepage_lock")
        if File.exist(lockfile):
            cp = cls.get_cmd_code_page()
            if not safe:
                raise IOError(f"Cannot use codepage 65001, continue using {cp}, "
                              f"you can set other by Windows.set_cmd_code_page")
            return cp
        previous_codepage = cls.get_cmd_code_page()
        try:
            if previous_codepage != 65001:
                cls.set_cmd_code_page(65001)
            import os
            with Print.s_print_lock:
                command = r'''python3 -c "print('йЙ\r', end='')"'''
            Print("йЙ\r", end="")
            Print("  \r", end="")
            os.system(command)
            Print("  \r", end="")
            return cls.get_cmd_code_page()
        except Exception:
            if int(previous_codepage) >= 0:
                if previous_codepage != 65001:
                    cls.set_cmd_code_page(previous_codepage)
                else:
                    cls.set_cmd_code_page(437)
                Print("  \r", end="")
                from .os9 import OS
                OS._cyrillic_support = False
                File.create(lockfile)
                if not safe:
                    raise IOError(f"Cannot use codepage 65001, returning to {previous_codepage}, "
                                  f"you can set other by Windows.set_cmd_code_page")
                return previous_codepage

    @staticmethod
    def user_exists(username):
        """
        <br>`param username` string
        <br>`return` boolean, existence of local user
        """
        import subprocess
        from .console9 import Console
        try:
            Console.get_output(f"net user {username}")
            return True
        except subprocess.CalledProcessError:
            return False

    def _user(self, username, password=None, create=False, remove=False, retry_cnt=0):
        """Creates or removes user using net user command
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
            else:
                raise NotImplementedError
            output = Console.get_output(command)
            if "The command completed successfully." in output:
                return
            else:
                if create:
                    raise OSError(f"User {username} failed to create. {output}")
                elif remove:
                    raise OSError(f"User {username} failed to remove. {output}")
        except subprocess.CalledProcessError:
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
    def dump_auditpol(filename=None, category="*", fast_name=None, quiet=False):
        from .file9 import File
        from .console9 import Console
        from .time9 import Time
        import subprocess
        if not filename:
            filename = f"auditpol_{Time.dotted()}.txt"
        if fast_name:
            filename = f"auditpol_{Time.dotted()}--{fast_name}.txt"
        try:
            output = Console.get_output(f"auditpol /get /category:{category}")
        except subprocess.CalledProcessError:
            raise OSError("Try to run under elevated commandline")
        File.write(filename, output)
        if not quiet:
            print(f"Audit politics saved to {filename}")

    winreg_imported = False

    @classmethod
    def import_winreg(cls):
        if not cls.winreg_imported:
            from .os9 import OS
            import winreg
            cls.winreg = winreg
            cls.winreg_imported = True
        return cls.winreg

    @classmethod
    def getenv(cls, name, scope="user"):
        winreg = cls.import_winreg()
        assert scope in ('user', 'system'), "Houston we've got a problem"
        if scope == 'user':
            root = winreg.HKEY_CURRENT_USER
            subkey = 'Environment'
        else:
            root = winreg.HKEY_LOCAL_MACHINE
            subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        key = winreg.OpenKey(root, subkey, 0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, name)
        except WindowsError:
            value = ''
        return value

    @classmethod
    def setenv(cls, name, value, scope="user"):
        # Note: for 'system' scope, you must run this as Administrator
        from .console9 import Console
        from .path9 import Path
        winreg = cls.import_winreg()
        assert scope in ('user', 'system'), "Houston we've got a problem"
        if scope == 'user':
            root = winreg.HKEY_CURRENT_USER
            subkey = 'Environment'
        else:
            root = winreg.HKEY_LOCAL_MACHINE
            subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        key = winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
        winreg.CloseKey(key)
        # For some strange reason, calling SendMessage from the current process
        # doesn't propagate environment changes at all.
        return Console.get_output(Path.python(), "-c", "import win32api, win32con; "
                                                       "assert win32api.SendMessage(win32con.HWND_BROADCAST, "
                                                       "win32con.WM_SETTINGCHANGE, 0, 'Environment')")

    @staticmethod
    def get_powershell_execution_policy():
        from .console9 import Console
        powershell_fix_command = f'''powershell -command "& {{&'Get-ExecutionPolicy'}}"'''
        out, err = Console.get_output(powershell_fix_command, return_merged=False)
        if err:
            raise OSError(err)
        return out.strip()

    @staticmethod
    def set_powershell_execution_policy(policy_name):
        from .console9 import Console
        powershell_fix_command = f'''powershell -command "& {{&'Set-ExecutionPolicy' {policy_name}}}"'''
        # "Set-ExecutionPolicy {policy_name}"
        out, err = Console.get_output(powershell_fix_command, return_merged=False)
        if err:
            raise OSError(err)
        return out

    @classmethod
    def run_powershell(cls, ps1_script):
        from .random9 import Random
        from .file9 import File
        from .console9 import Console

        temp_ps1_file = Random.string(10)+".ps1"

        old_policy = cls.get_powershell_execution_policy()
        if old_policy != "RemoteSigned":
            cls.set_powershell_execution_policy("RemoteSigned")

        File.write(temp_ps1_file, ps1_script)
        out, err = Console.get_output(fr'powershell .\"{temp_ps1_file}"', return_merged=False,
                                      create_cmd_subprocess=True)
        File.delete(temp_ps1_file)

        if old_policy != "RemoteSigned":
            cls.set_powershell_execution_policy(old_policy)

        if err:
            raise OSError(err)

        return out

    @staticmethod
    def change_wallpaper(image_path):
        import ctypes
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 0)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
