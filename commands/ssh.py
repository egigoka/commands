#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with ssh."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty
__version__ = "0.1.1"
OS = LazyProperty(".os", "OS")
Str = LazyProperty(".str", "Str")

paramiko = LazyModule("paramiko")
newline = "\n"


class Ssh:
    """Class with functions to work with ssh."""

    def __init__(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        safe: bool = False
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.safe = safe

    def _credentials(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[str, str, str]:
        host = host or self.host
        username = username or self.username
        password = password or self.password
        if not host or not username or password is None:
            raise ValueError("host, username and password must be set")
        return host, username, password

    def command(
        self,
        command: str,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        safe: Optional[bool] = None
    ) -> str:
        """Run a command using stored SSH credentials when provided."""
        host, username, password = self._credentials(host, username, password)
        if safe is None:
            safe = self.safe
        return self.get_output(host=host, username=username, password=password, command=command, safe=safe)

    __call__ = command

    @classmethod
    def get_output(
        cls,
        host: str,
        username: str,
        password: str,
        command: str,
        safe: bool = False
    ) -> str:
        """Return output from a command run on an SSH server.

        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param command` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string, output from 'command' execution
        """
        # todo authorisation by key.
        if OS.python_implementation == "pypy":
            raise OSError("paramiko doesn't supported by PyPy")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add unknown hosts
        ssh.connect(host, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)  # pylint: disable=unused-variable
        if (ssh_stderr.read() != b'') and not safe:
            raise IOError("ssh_stderr = " + str(ssh_stderr))
        ssh.close()
        return str(ssh_stdout.read(), 'utf8')

    @classmethod
    def get_avg_load_lin(
        cls,
        host: str,
        username: str,
        password: str,
        safe: bool = False
    ) -> List[str]:
        """Get Linux load averages from uptime output.

        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string with average loads of SSH linux server.
        """
        output = cls.get_output(host=host, username=username, password=password, command="uptime", safe=safe)
        substring = Str.substring(output, before="load average: ", after=newline)
        return str(substring).split(", ")

    @classmethod
    def get_uptime_lin(
        cls,
        host: str,
        username: str,
        password: str,
        safe: bool = False
    ) -> str:
        """Get Linux uptime from uptime output.

        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string with uptime of SSH linux server.
        """
        output = cls.get_output(host=host, username=username, password=password, command="uptime", safe=safe)
        output = Str.substring(output, before=" up ", after=", ")
        return str(output)

    def avg_load(self, safe: Optional[bool] = None) -> List[str]:
        """Shortcut for get_avg_load_lin using stored credentials."""
        host, username, password = self._credentials()
        if safe is None:
            safe = self.safe
        return self.get_avg_load_lin(host=host, username=username, password=password, safe=safe)

    def uptime(self, safe: Optional[bool] = None) -> str:
        """Shortcut for get_uptime_lin using stored credentials."""
        host, username, password = self._credentials()
        if safe is None:
            safe = self.safe
        return self.get_uptime_lin(host=host, username=username, password=password, safe=safe)
