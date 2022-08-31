#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with ssh
"""
__version__ = "0.1.1"


class Ssh:
    """Class with functions to work with ssh
    """
    @staticmethod
    def get_output(host, username, password, command, safe=False):
        """Return output from command, run on SSH server. Support only username`password authorisation.
        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param command` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string, output from 'command' execution
        """
        # todo authorisation by key.
        from .os9 import OS
        if OS.python_implementation != "pypy":
            import paramiko
        else:
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
    def get_avg_load_lin(cls, host, username, password, safe=False):
        """Shit, I know
        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string with average loads of SSH linux server.
        """
        from .str9 import Str
        from .const9 import newline
        output = cls.get_output(host=host, username=username, password=password, command="uptime", safe=safe)
        output = Str.substring(output, before="load average: ", after=newline)
        output = output.split(", ")
        return output

    @classmethod
    def get_uptime_lin(cls, host, username, password, safe=False):
        """
        <br>`param host` string, host or IP
        <br>`param username` string
        <br>`param password` string
        <br>`param safe` boolean, do not crash if connection unsuccessful
        <br>`return` string with uptime of SSH linux server.
        """
        from .str9 import Str
        output = cls.get_output(host=host, username=username, password=password, command="uptime", safe=safe)
        output = Str.substring(output, before=" up ", after=", ")
        return output
