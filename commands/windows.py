#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with Windows-specific functions."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, Tuple, Union

from .module import LazyModule, LazyProperty

__version__ = "0.7.4"

base64 = LazyModule("base64")
ctypes = LazyModule("ctypes")
os = LazyModule("os")
subprocess = LazyModule("subprocess")
winreg = LazyModule("winreg", optional=True)
winrm = LazyModule("winrm", optional=True)
Console = LazyProperty(".console", "Console")
File = LazyProperty(".file", "File")
List = LazyProperty(".list", "List")
OS = LazyProperty(".os", "OS")
Path = LazyProperty(".path", "Path")
Print = LazyProperty(".print", "Print")
Random = LazyProperty(".random", "Random")
Str = LazyProperty(".str", "Str")
Time = LazyProperty(".time", "Time")


class Windows:
    """Class to work with Windows-specific functions."""

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[int] = None,
        transport: str = "ntlm"
    ) -> None:
        """Optionally keep remote credentials for short calls."""
        self._remote: Optional["Windows.RemoteSystem"] = None
        if hostname and username and password:
            self._remote = self.RemoteSystem(hostname, username, password, port=port, transport=transport)

    def connect(
        self,
        hostname: str,
        username: str,
        password: str,
        port: Optional[int] = None,
        transport: str = "ntlm"
    ) -> "Windows.RemoteSystem":
        """Create and store a RemoteSystem session on this instance."""
        self._remote = self.RemoteSystem(hostname, username, password, port=port, transport=transport)
        return self._remote

    def ps(self, script: str) -> Tuple[str, str, int]:
        """Run PowerShell on a stored RemoteSystem."""
        if self._remote is None:
            raise ValueError("Remote system is not configured")
        return self._remote.ps(script)

    def cmd(self, program: str, *args: str) -> Tuple[str, str, int]:
        """Run cmd on a stored RemoteSystem."""
        if self._remote is None:
            raise ValueError("Remote system is not configured")
        return self._remote.cmd(program, *args)

    @classmethod
    def remote(
        cls,
        hostname: str,
        username: str,
        password: str,
        port: Optional[int] = None,
        transport: str = "ntlm"
    ) -> "Windows.RemoteSystem":
        """Create a RemoteSystem instance."""
        return cls.RemoteSystem(hostname, username, password, port=port, transport=transport)

    class RemoteSystem:
        """Remote Windows system wrapper."""

        def __init__(
            self,
            hostname: str,
            username: str,
            password: str,
            port: Optional[int] = None,
            transport: str = "ntlm"
        ) -> None:
            if not winrm:
                raise ImportError("please, install pywinrm")
            # FIX winrm #

            def fix_run_ps(self: Any, script: str) -> Any:
                encoded_ps = base64.b64encode(script.encode('utf_16_le')).decode('ascii')
                rs = self.run_cmd('powershell -encodedcommand {0}'.format(encoded_ps))
                if len(rs.std_err):
                    rs.std_err = self._clean_error_msg(rs.std_err.decode('utf-8'))
                return rs

            setattr(winrm.Session, "run_ps", fix_run_ps)

            # END FIX winrm #

            if port is None:
                port = 5986 if transport == 'ssl' else 5985

            self.session: Any = winrm.Session(fr"{hostname}:{port}", auth=(username, password), transport=transport)

        def ps(self, script: str) -> Tuple[str, str, int]:
            """Run a PowerShell script and return output, error, and status."""
            output = self.session.run_ps(script)
            if output.std_err.startswith("#< CLIXML\r\n"):
                output.std_err = output.std_err[len("#< CLIXML\r\n"):]

            out = output.std_out.decode()
            err = output.std_err
            return out, err, output.status_code

        def cmd(self, program: str, *args: str) -> Tuple[str, str, int]:
            """Run a command and return output, error, and status."""
            args_list = List.to_strings(args)
            output = self.session.run_cmd(program, args_list)

            out = output.std_out.decode()
            err = output.std_err.decode()
            return out, err, output.status_code


    @classmethod
    def lock(cls) -> None:
        """Lock the Windows workstation (not supported on Windows 10).

        <br>`return` None
        """
        windows_version = getattr(OS, "windows_version", None)
        if windows_version is not None and windows_version != 10:
            windll = getattr(ctypes, "windll", None)
            if windll is None:
                raise OSError("ctypes.windll is not available on this platform")
            windll.LockWorkStation()  # todo fix Windows 10
        else:
            raise OSError("Locking work only on Windows < 10")

    @classmethod
    def set_cmd_code_page(cls, code_page: int) -> int:
        """Set the Windows cmd code page and return it."""
        subprocess.Popen(f"chcp {code_page}".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        os.system("set PYTHONIOENCODING = utf - 8")
        cls.get_cmd_code_page()  # it's fucking magick, don't touch
        return code_page

    @classmethod
    def get_cmd_code_page(cls, debug: bool = False) -> Union[int, str]:
        """Get the current Windows cmd code page."""
        raw_out, err = subprocess.Popen(
            "chcp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        if err:
            return "Error getting current codepage"
        try:
            if debug:
                print(raw_out)
            parsed = Str.substring(raw_out, ": ", "\r\n")
            if debug:
                print(parsed)
            return int(str(parsed))
        except KeyError:
            return "Cannot get current codepage"

    @classmethod
    def fix_unicode_encode_error(cls, safe: bool = False) -> Union[int, str]:
        """Fix UnicodeConsoleError on older Python versions.

        <br>`return` int, current code_page number
        """
        lockfile = Path.combine(Path.commands(), ".windows_codepage_lock")
        if File.exist(lockfile):
            cp = cls.get_cmd_code_page()
            if not safe:
                raise IOError(f"Cannot use codepage 65001, continue using {cp}, "
                              f"you can set other by Windows.set_cmd_code_page")
            return cp
        previous_codepage = cls.get_cmd_code_page()
        try:
            if isinstance(previous_codepage, int) and previous_codepage != 65001:
                cls.set_cmd_code_page(65001)
            with Print.s_print_lock:
                command = r'''python3 -c "print('йЙ\r', end='')"'''
            Print("йЙ\r", end="")
            Print("  \r", end="")
            os.system(command)
            Print("  \r", end="")
            return cls.get_cmd_code_page()
        except Exception:
            if isinstance(previous_codepage, int) and previous_codepage >= 0:
                if previous_codepage != 65001:
                    cls.set_cmd_code_page(previous_codepage)
                else:
                    cls.set_cmd_code_page(437)
                Print("  \r", end="")
                OS._cyrillic_support = False
                File.create(lockfile)
                if not safe:
                    raise IOError(f"Cannot use codepage 65001, returning to {previous_codepage}, "
                                  f"you can set other by Windows.set_cmd_code_page")
                return previous_codepage
        return previous_codepage

    @classmethod
    def user_exists(cls, username: str) -> bool:
        """Check whether a local user exists.

        <br>`param username` string
        <br>`return` boolean, existence of local user
        """
        try:
            Console.get_output(f"net user {username}")
            return True
        except subprocess.CalledProcessError:
            return False

    def _user(
        self,
        username: str,
        password: Optional[str] = None,
        create: bool = False,
        remove: bool = False,
        retry_cnt: int = 0
    ) -> None:
        """Create or remove a local user with the net user command.

        <br>`param username` string
        <br>`param password` string
        <br>`param create` boolean, True for create user
        <br>`param remove` boolean, True for remove user
        <br>`param retry_cnt` int, internally used to not raise RecursionError
        <br>`return` None
        """
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

    def create_user(self, username: str, password: str) -> None:
        """Create a local user with the net user command.

        <br>`param username` string
        <br>`param password` string
        <br>`return` None
        """
        return self._user(username=username, password=password, create=True)

    def remove_user(self, username: str) -> None:  # remove only users from json file
        """Remove a local user with the net user command.

        <br>`param username` string
        <br>`return` None
        """
        return self._user(username=username, remove=True)

    @classmethod
    def dump_auditpol(
        cls,
        filename: Optional[str] = None,
        category: str = "*",
        fast_name: Optional[str] = None,
        verbose: bool = False
    ) -> None:
        """Dump audit policy to a file."""
        if not filename:
            filename = f"auditpol_{Time.dotted()}.txt"
        if fast_name:
            filename = f"auditpol_{Time.dotted()}--{fast_name}.txt"
        try:
            output = Console.get_output(f"auditpol /get /category:{category}")
        except subprocess.CalledProcessError:
            raise OSError("Try to run under elevated commandline")
        File.write(filename, output)
        if verbose:
            print(f"Audit politics saved to {filename}")

    winreg_imported = False
    winreg: Any = None

    @classmethod
    def import_winreg(cls) -> Any:
        """Import and cache the winreg module."""
        if not cls.winreg_imported:
            module = winreg._load()
            if module is None:
                raise ImportError("winreg is not available")
            cls.winreg = module
            cls.winreg_imported = True
        return cls.winreg

    @classmethod
    def getenv(cls, name: str, scope: str = "user") -> str:
        """Get a Windows environment variable from the registry."""
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
        except OSError:
            value = ''
        return str(value)

    @classmethod
    def setenv(cls, name: str, value: str, scope: str = "user") -> Any:
        """Set a Windows environment variable in the registry."""
        # Note: for 'system' scope, you must run this as Administrator
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
        return Console.get_output(
            Path.python(),
            "-c",
            "import win32api, win32con; "
            "assert win32api.SendMessage(win32con.HWND_BROADCAST, "
            "win32con.WM_SETTINGCHANGE, 0, 'Environment')"
        )

    @classmethod
    def get_powershell_execution_policy(cls) -> str:
        """Get the current PowerShell execution policy."""
        powershell_fix_command = f'''powershell -command "& {{&'Get-ExecutionPolicy'}}"'''
        out, err = Console.get_output(powershell_fix_command, return_merged=False)
        if err:
            raise OSError(err)
        return str(out).strip()

    @classmethod
    def set_powershell_execution_policy(cls, policy_name: str) -> str:
        """Set the PowerShell execution policy."""
        powershell_fix_command = f'''powershell -command "& {{&'Set-ExecutionPolicy' {policy_name}}}"'''
        # "Set-ExecutionPolicy {policy_name}"
        out, err = Console.get_output(powershell_fix_command, return_merged=False)
        if err:
            raise OSError(err)
        return str(out)

    @classmethod
    def run_powershell(cls, ps1_script: str) -> str:
        """Run a PowerShell script and return its output."""
        temp_ps1_file = Random.string(10) + ".ps1"

        old_policy = cls.get_powershell_execution_policy()
        if old_policy != "RemoteSigned":
            cls.set_powershell_execution_policy("RemoteSigned")

        File.write(temp_ps1_file, ps1_script)
        out, err = Console.get_output(
            fr'powershell .\"{temp_ps1_file}"',
            return_merged=False,
            create_cmd_subprocess=True
        )
        File.delete(temp_ps1_file)

        if old_policy != "RemoteSigned":
            cls.set_powershell_execution_policy(old_policy)

        if err:
            raise OSError(err)

        return str(out)

    @classmethod
    def change_wallpaper(cls, image_path: str) -> None:
        """Change the desktop wallpaper."""
        SPI_SETDESKWALLPAPER = 20
        windll = getattr(ctypes, "windll", None)
        if windll is None:
            raise OSError("ctypes.windll is not available on this platform")
        windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 0)
        windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
