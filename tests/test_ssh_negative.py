# Consolidated tests for commands/ssh.py (negative)

# ---- from test_ssh_negative.py ----

# Placeholder for future tests.
import pytest
from commands.ssh import Ssh
from unittest.mock import Mock, patch, MagicMock
import types

def test_ssh_credentials_missing():
    s = Ssh()
    with pytest.raises(ValueError):
        s.command("ls")

def test_ssh_avg_load_missing_credentials():
    s = Ssh()
    with pytest.raises(ValueError):
        s.avg_load()

def test_ssh_uptime_missing_credentials():
    s = Ssh()
    with pytest.raises(ValueError):
        s.uptime()

def test_ssh_get_output_raises_on_pypy(monkeypatch):
    from commands.os import OS
    monkeypatch.setattr(OS, "_python_implementation", "pypy")
    with pytest.raises(OSError):
        Ssh.get_output("h", "u", "p", "cmd")
