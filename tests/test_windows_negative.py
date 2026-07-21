# Consolidated tests for commands/windows.py (negative)

# ---- from test_windows_coverage_gaps.py ----


import os
import sys
import types

import pytest


import subprocess













# ---- from test_windows_getenv_setenv_errors.py ----


import pytest

from commands.windows import Windows


def test_windows_getenv_missing_key(monkeypatch):
    class DummyKey:
        pass

    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        KEY_READ = "read"

        def OpenKey(self, root, subkey, idx, access):
            return DummyKey()

        def QueryValueEx(self, key, name):
            raise OSError("missing")

    import commands.windows as windows_module
    monkeypatch.setattr(windows_module, "WindowsError", OSError, raising=False)
    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    assert Windows.getenv("NAME") == ""


def test_windows_setenv_assert(monkeypatch):
    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        HKEY_LOCAL_MACHINE = "system"
        KEY_READ = "read"
        KEY_ALL_ACCESS = "all"
        REG_EXPAND_SZ = "reg"

        def OpenKey(self, *args, **kwargs):
            return object()

        def SetValueEx(self, *a, **k):
            pass

        def CloseKey(self, *a, **k):
            pass

    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    with pytest.raises(AssertionError):
        Windows.setenv("NAME", "VAL", scope="bad")


# ---- from test_windows_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
"""Tests for missing coverage in windows.py module"""
import os
import sys
import types
import pytest
from commands import Windows


class TestWindowsMissingCoverage:
    """Tests to cover missing lines in windows.py"""




    def test_user_already_exists_error(self, monkeypatch):
        """Test _user raises error when user already exists (line 194)"""
        def mock_user_exists(self, username):
            return True

        monkeypatch.setattr(Windows, 'user_exists', mock_user_exists)

        win = Windows()
        with pytest.raises(OSError, match="already exists"):
            win._user("existinguser", "pass", create=True)

    def test_user_doesnt_exist_error(self, monkeypatch):
        """Test _user raises error when removing non-existent user (line 200)"""
        def mock_user_exists(self, username):
            return False

        monkeypatch.setattr(Windows, 'user_exists', mock_user_exists)

        win = Windows()
        with pytest.raises(OSError, match="already doesn't exists"):
            win._user("nonexistent", remove=True)

    def test_user_not_implemented_error(self, monkeypatch):
        """Test _user raises NotImplementedError (line 203)"""
        def mock_user_exists(self, username):
            return False

        monkeypatch.setattr(Windows, 'user_exists', mock_user_exists)

        win = Windows()
        with pytest.raises(NotImplementedError):
            win._user("user", create=False, remove=False)

    def test_user_failed_to_create_error(self, monkeypatch):
        """Test _user raises error when creation fails (lines 209-210)"""
        def mock_user_exists(self, username):
            return False

        def mock_get_output(command):
            return "Some error occurred"

        monkeypatch.setattr(Windows, 'user_exists', mock_user_exists)

        import commands.console
        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))

        win = Windows()
        with pytest.raises(OSError, match="failed to create"):
            win._user("newuser", "pass", create=True)

    def test_user_failed_to_remove_error(self, monkeypatch):
        """Test _user raises error when removal fails (line 211)"""
        def mock_user_exists(self, username):
            return True

        def mock_get_output(command):
            return "Some error occurred"

        monkeypatch.setattr(Windows, 'user_exists', mock_user_exists)

        import commands.console
        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))

        win = Windows()
        with pytest.raises(OSError, match="failed to remove"):
            win._user("user", remove=True)




    def test_get_powershell_policy_error(self, monkeypatch):
        """Test get_powershell_execution_policy error handling (line 311)"""
        import commands.console

        def mock_get_output(command, return_merged=True):
            return ("", "Permission denied")

        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))

        with pytest.raises(OSError, match="Permission denied"):
            Windows.get_powershell_execution_policy()

    def test_set_powershell_policy_error(self, monkeypatch):
        """Test set_powershell_execution_policy error handling (line 322)"""
        import commands.console

        def mock_get_output(command, return_merged=True):
            return ("", "Access denied")

        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))

        with pytest.raises(OSError, match="Access denied"):
            Windows.set_powershell_execution_policy("RemoteSigned")

    def test_windows_lock_missing_windll(self, monkeypatch):
        """Test lock when ctypes.windll is unavailable (line 125)."""
        import ctypes
        from commands.os import OS

        monkeypatch.setattr(OS, "_windows_version", 7, raising=False)
        monkeypatch.setattr(OS, "_windows", True, raising=False)
        monkeypatch.setattr(ctypes, "windll", None, raising=False)

        with pytest.raises(OSError, match="ctypes.windll is not available"):
            Windows.lock()


    def test_remote_system_requires_winrm(self, monkeypatch):
        """Test RemoteSystem raises when winrm is unavailable (line 95)."""
        class DummyWinRM:
            def __bool__(self):
                return False

        import commands.windows as windows_module

        monkeypatch.setattr(windows_module, "winrm", DummyWinRM())

        with pytest.raises(ImportError, match="install pywinrm"):
            Windows.RemoteSystem("host", "user", "pass")

    def test_import_winreg_missing_module(self, monkeypatch):
        """Test import_winreg raises when winreg isn't available (line 327)."""
        class DummyWinreg:
            def _load(self):
                return None

        import commands.windows as windows_module

        monkeypatch.setattr(windows_module, "winreg", DummyWinreg())
        monkeypatch.setattr(Windows, "winreg_imported", False)
        monkeypatch.setattr(Windows, "winreg", None)

        with pytest.raises(ImportError, match="winreg is not available"):
            Windows.import_winreg()

    def test_change_wallpaper_missing_windll(self, monkeypatch):
        """Test change_wallpaper when ctypes.windll is unavailable (line 446)."""
        import ctypes

        monkeypatch.setattr(ctypes, "windll", None, raising=False)
        with pytest.raises(OSError, match="ctypes.windll is not available"):
            Windows.change_wallpaper("wallpaper.bmp")

def test_windows_lock_version_guard(monkeypatch):
    from commands.os import OS
    monkeypatch.setattr(OS, "_windows_version", 10)
    with pytest.raises(OSError):
        Windows.lock()

def test_windows_dump_auditpol_missing_permissions(monkeypatch):
    import subprocess
    monkeypatch.setattr("commands.time.Time.dotted", lambda: "stamp")
    monkeypatch.setattr("commands.file.File.write", lambda path, data: None)
    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            raise subprocess.CalledProcessError(1, cmd)
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError, match="elevated commandline"):
        Windows.dump_auditpol(filename="out.txt", category="*", fast_name=None, verbose=False)

def test_windows_instance_requires_remote_for_ps():
    w = Windows()
    with pytest.raises(ValueError):
        w.ps("echo hi")

def test_windows_instance_requires_remote_for_cmd():
    w = Windows()
    with pytest.raises(ValueError):
        w.cmd("dir")

def test_windows_lock_fails_windows10(monkeypatch):
    class DummyOS:
        _windows_version = 10
        windows_version = 10
    monkeypatch.setattr("commands.os.OS", DummyOS)
    with pytest.raises(OSError):
        Windows.lock()

def test_windows_powershell_policy_set_error(monkeypatch):
    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False):
            return "", "error"

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError):
        Windows.set_powershell_execution_policy("Bypass")

def test_windows_fix_unicode_restore_on_error(monkeypatch):
    calls = {}
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/lockfile"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: False))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: 65001))
    monkeypatch.setattr("commands.windows.Windows.set_cmd_code_page", classmethod(lambda cls, cp: calls.setdefault("cp", cp)))
    class DummyPrint:
        s_print_lock = None
        @staticmethod
        def __call__(*a, **k): pass
    monkeypatch.setattr("commands.print.Print", DummyPrint())
    # force exception after setting cyrillic support change
    monkeypatch.setattr("os.system", lambda cmd: (_ for _ in ()).throw(RuntimeError("bad")))
    monkeypatch.setattr("commands.file.File.create", lambda path: calls.setdefault("lock", path))
    from commands.os import OS
    OS._cyrillic_support = True
    with pytest.raises(IOError):
        Windows.fix_unicode_encode_error(safe=False)
    # Should have attempted to restore code page
    assert calls.get("cp") in (437, 65001)
    assert calls.get("lock") == "/lockfile"

def test_windows_fix_unicode_lockfile_unsafe_raises(monkeypatch):
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/tmp/lock"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: True))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: 866))
    with pytest.raises(IOError):
        Windows.fix_unicode_encode_error(safe=False)

def test_windows_fix_unicode_restore_on_exception(monkeypatch):
    calls = {}

    def fake_set(cp):
        calls.setdefault("set", []).append(cp)
    def fake_get():
        return 437

    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/tmp/lock"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: False))
    monkeypatch.setattr("commands.file.File.create", lambda path: calls.setdefault("lock", path))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: fake_get()))
    monkeypatch.setattr("commands.windows.Windows.set_cmd_code_page", classmethod(lambda cls, cp: fake_set(cp)))
    import types
    class DummyPrint:
        s_print_lock = types.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda self, *a: None)
        def __call__(self, *a, **k): pass
    monkeypatch.setattr("commands.print.Print", DummyPrint())
    # make os.system raise inside try
    monkeypatch.setattr("os.system", lambda cmd: (_ for _ in ()).throw(RuntimeError("fail")))
    with pytest.raises(IOError):
        Windows.fix_unicode_encode_error(safe=False)
    assert 437 in calls["set"]
    assert calls["lock"] == "/tmp/lock"

def test_windows_user_invalid_username_type():
    w = Windows()
    with pytest.raises(TypeError):
        w._user(username=123, password="p", create=True)

def test_windows_user_create_missing_password(monkeypatch):
    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: False)
    with pytest.raises(ValueError):
        w._user(username="name", password=None, create=True)

def test_windows_user_remove_missing(monkeypatch):
    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: False)
    with pytest.raises(OSError):
        w._user(username="name", remove=True)

def test_windows_user_create_output_error(monkeypatch):
    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: False)

    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            return "unexpected output"

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError):
        w._user(username="name", password="pwd", create=True)

def test_windows_user_retry_on_called_process(monkeypatch):
    import subprocess
    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: False)

    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError):
        w._user(username="name", password="pwd", create=True)

def test_windows_user_remove_called_process_gives_final_error(monkeypatch):
    import subprocess

    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: True)

    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError):
        w._user(username="name", remove=True, retry_cnt=5)

def test_windows_run_powershell_error(monkeypatch):
    monkeypatch.setattr("commands.random.Random.string", staticmethod(lambda length: "tempfile"))
    monkeypatch.setattr("commands.file.File.write", lambda path, data: None)
    monkeypatch.setattr("commands.file.File.delete", lambda path: None)
    monkeypatch.setattr("commands.windows.Windows.get_powershell_execution_policy",
                        classmethod(lambda cls: "RemoteSigned"))
    monkeypatch.setattr("commands.windows.Windows.set_powershell_execution_policy",
                        classmethod(lambda cls, policy: None))

    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False, create_cmd_subprocess=False):
            return "", "err"

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    with pytest.raises(OSError):
        Windows.run_powershell("Write-Host 'fail'")
