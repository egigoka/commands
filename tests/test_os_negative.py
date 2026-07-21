# Consolidated tests for commands/os.py (negative)

# ---- from test_os_negative.py ----

# Placeholder for future tests.
import pytest
import sys
from commands.os import OS
import os
import tempfile
from unittest.mock import patch, Mock
import types

def _reset_os_cache():
    OS._python_version_major = None
    OS._python_commandline_version = None
    OS._sys_platform = None
    OS._windows = None
    OS._windows_version = None
    OS._linux = None
    OS._name = None
    OS._macos = None
    OS._architecture = None
    OS._python_implementation = None
    OS._nt_family = None
    OS._unix_family = None
    OS._display = None
    OS._running_in_repl = None
    OS._cyrillic_support = None
    OS._hostname = None
    OS._cwd = None

class TestOSWindowsVersion:
    """Tests for windows_version property"""
    def test_windows_version_on_non_windows(self, monkeypatch):
        """Test windows_version on non-Windows"""
        _reset_os_cache()
        monkeypatch.setattr(OS, "_windows", False)
        monkeypatch.setattr(OS, "_sys_platform", "linux")
        with pytest.raises(AttributeError):
            _ = OS.windows_version

def test_os_cyrillic_support_unicode_encode_error_path(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_sys_platform", "linux")
    monkeypatch.setattr(sys, "version_info", (3, 13, 0))

    def bad_print(*_a, **_k):
        raise UnicodeEncodeError("utf-8", "x", 0, 1, "bad")

    monkeypatch.setattr("builtins.print", bad_print)
    assert OS.cyrillic_support is False

def test_os_windows_version_missing_getwindowsversion(monkeypatch):
    _reset_os_cache()
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_sys_platform", "win32")
    monkeypatch.delattr(sys, "getwindowsversion", raising=False)

    with pytest.raises(AttributeError, match="getwindowsversion"):
        _ = OS.windows_version
