#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Ssh:
    @staticmethod
    def get_output(host, username, password, command, safe=False):
        """Return output from command, runned on SSH server. Support only username:password autorisation.
        """
        # todo authorisation by key.
        from .os8 import OS
        if OS.python_implementation != "pypy":
            import paramiko
        else:
            raise OSError("paramiko doesn't supported by PyPy")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically add unknown hosts
        ssh.connect(host, username=username, password=password)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uptime")
        if (ssh_stderr.read() != b'') and not safe:
            raise IOError("ssh_stderr = " + str(ssh_stderr))
        ssh.close()
        return str(ssh_stdout.read(), 'utf8')

    @classmethod
    def get_avg_load_lin(cls, host, username, password, safe=False):
        """Return list of average loads from SSH linux server. Shit, I know
        """
        from .str8 import Str
        from .const8 import newline
        output = cls.get_output(host=host, username=username, password=password, command="uprime", safe=safe)
        output = Str.substring(output, before="load average: ", after=newline)
        output = output.split(", ")
        return output

    @classmethod
    def get_uptime_lin(cls, host, username, password, safe=False):  #
        """
        :param host:
        :param username:
        :param password:
        :param safe:
        :return: string with uptime of SSH linux server.
        """
        from .str8 import Str
        output = cls.get_output(host=host, username=username, password=password, command="uprime", safe=safe)
        output = Str.substring(output, before=" up ", after=", ")
        return output
