# Consolidated tests for commands/ssh.py (unit)

# ---- from test_ssh9.py ----


import pytest


def test_ssh9_import():
    from commands import Ssh
    assert Ssh is not None


# ---- from test_ssh_coverage.py ----


import pytest
from commands.ssh import Ssh


def test_ssh_import():
    from commands import Ssh as S
    assert S is not None
from unittest.mock import Mock, patch, MagicMock


class TestSshCoverage:
    """Tests to improve SSH module coverage"""

    def test_credentials_success(self):
        """Test _credentials returns values when all are set"""
        s = Ssh(host="localhost", username="user", password="pass")
        host, username, password = s._credentials()
        assert host == "localhost"
        assert username == "user"
        assert password == "pass"

    def test_command_with_safe_none_uses_instance_safe(self, monkeypatch):
        """Test command() defaults to instance safe when safe=None"""
        # Mock paramiko to avoid real SSH connection
        mock_ssh_client = MagicMock()
        mock_paramiko = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        mock_paramiko.AutoAddPolicy.return_value = Mock()

        # Setup stdout
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"output"
        mock_stderr = MagicMock()
        mock_stderr.read.return_value = b""
        mock_ssh_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        monkeypatch.setitem(__import__('sys').modules, 'paramiko', mock_paramiko)

        # Test with safe=True on instance, safe=None on method call
        s = Ssh(host="localhost", username="user", password="pass", safe=True)
        result = s.command("ls", safe=None)  # Should use self.safe=True
        assert result == "output"

    def test_avg_load_with_safe_none_uses_instance_safe(self, monkeypatch):
        """Test avg_load() defaults to instance safe when safe=None"""
        # Mock paramiko
        mock_ssh_client = MagicMock()
        mock_paramiko = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        mock_paramiko.AutoAddPolicy.return_value = Mock()

        # Setup stdout with uptime output
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"10:00:00 up 1 day, 2:30, load average: 0.5, 0.3, 0.2\n"
        mock_stderr = MagicMock()
        mock_stderr.read.return_value = b""
        mock_ssh_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        monkeypatch.setitem(__import__('sys').modules, 'paramiko', mock_paramiko)

        # Test with safe=False on instance, safe=None on method call
        s = Ssh(host="localhost", username="user", password="pass", safe=False)
        result = s.avg_load(safe=None)  # Should use self.safe=False
        assert result == ["0.5", "0.3", "0.2"]

    def test_uptime_with_safe_none_uses_instance_safe(self, monkeypatch):
        """Test uptime() defaults to instance safe when safe=None"""
        # Mock paramiko
        mock_ssh_client = MagicMock()
        mock_paramiko = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_ssh_client
        mock_paramiko.AutoAddPolicy.return_value = Mock()

        # Setup stdout with uptime output
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"10:00:00 up 1 day, 2:30, load average: 0.5\n"
        mock_stderr = MagicMock()
        mock_stderr.read.return_value = b""
        mock_ssh_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        monkeypatch.setitem(__import__('sys').modules, 'paramiko', mock_paramiko)

        # Test with safe=True on instance, safe=None on method call
        s = Ssh(host="localhost", username="user", password="pass", safe=True)
        result = s.uptime(safe=None)  # Should use self.safe=True
        assert result == "1 day"


# ---- from test_ssh_extra.py ----


import types

import pytest

from commands.ssh import Ssh


def test_ssh_get_output_success(monkeypatch):
    captured = {}

    class DummyStdout:
        def read(self):
            return b"ok"

    class DummyStderr:
        def __init__(self, data=b""):
            self._data = data
        def read(self):
            return self._data

    class DummySSHClient:
        def set_missing_host_key_policy(self, policy):
            captured["policy"] = policy
        def connect(self, host, username=None, password=None):
            captured["connect"] = (host, username, password)
        def exec_command(self, command):
            captured["command"] = command
            return None, DummyStdout(), DummyStderr()
        def close(self):
            captured["closed"] = True

    dummy_paramiko = types.SimpleNamespace(
        SSHClient=lambda: DummySSHClient(),
        AutoAddPolicy=lambda: "policy"
    )

    import sys
    monkeypatch.setitem(sys.modules, "paramiko", dummy_paramiko)
    from commands.os import OS
    monkeypatch.setattr(OS, "_python_implementation", "cpython")

    out = Ssh.get_output("h", "u", "p", "cmd")
    assert out == "ok"
    assert captured["connect"] == ("h", "u", "p")
    assert captured["command"] == "cmd"
    assert captured["closed"] is True


def test_ssh_get_output_safe(monkeypatch):
    class DummyStdout:
        def read(self):
            return b"ok"

    class DummyStderr:
        def read(self):
            return b"err"

    class DummySSHClient:
        def set_missing_host_key_policy(self, policy): pass
        def connect(self, host, username=None, password=None): pass
        def exec_command(self, command):
            return None, DummyStdout(), DummyStderr()
        def close(self): pass

    dummy_paramiko = types.SimpleNamespace(
        SSHClient=lambda: DummySSHClient(),
        AutoAddPolicy=lambda: None
    )
    import sys
    monkeypatch.setitem(sys.modules, "paramiko", dummy_paramiko)
    from commands.os import OS
    monkeypatch.setattr(OS, "_python_implementation", "cpython")

    # safe=True should suppress stderr raising
    assert Ssh.get_output("h", "u", "p", "cmd", safe=True) == "ok"
    # safe=False should raise
    with pytest.raises(IOError):
        Ssh.get_output("h", "u", "p", "cmd", safe=False)


def test_ssh_avg_load_and_uptime(monkeypatch):
    monkeypatch.setattr("commands.ssh.Ssh.get_output", lambda *a, **k: "09:00:00 up 1 day, 0 users, load average: 1.00, 0.50, 0.25\n")
    loads = Ssh.get_avg_load_lin("h", "u", "p")
    assert loads == ["1.00", "0.50", "0.25"]

    monkeypatch.setattr("commands.ssh.Ssh.get_output", lambda *a, **k: "10:00:00 up 3 days, 0 users, load average: 0.1, 0.2, 0.3\n")
    uptime = Ssh.get_uptime_lin("h", "u", "p")
    assert uptime == "3 days"


# ---- from test_ssh_instance.py ----


import pytest
from commands.ssh import Ssh
