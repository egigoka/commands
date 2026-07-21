# Consolidated tests for commands/windows.py (unit)

# ---- from test_windows9.py ----


import pytest


import os
import sys
from commands import Windows

def test_windows9_import():
    from commands import Windows
    assert Windows is not None


# ---- from test_windows_env.py ----


import types

import pytest

from commands.windows import Windows


def test_windows_getenv_sets_default(monkeypatch):
    class DummyKey:
        def __init__(self): pass
    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        HKEY_LOCAL_MACHINE = "system"
        KEY_READ = "read"
        KEY_ALL_ACCESS = "all"
        REG_EXPAND_SZ = "reg"
        def OpenKey(self, *args, **kwargs):
            return DummyKey()
        def QueryValueEx(self, key, name):
            return ("VAL", None)
        def CloseKey(self, key): pass
        def SetValueEx(self, *a, **k): pass
    monkeypatch.setattr("commands.windows.Windows.winreg_imported", False)
    monkeypatch.setattr(Windows, "winreg", DummyWinreg(), raising=False)
    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    assert Windows.getenv("NAME") == "VAL"
    # system scope path
    assert Windows.getenv("NAME", scope="system") == "VAL"
    with pytest.raises(AssertionError):
        Windows.getenv("NAME", scope="bad")

def test_windows_getenv_handles_missing(monkeypatch):
    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        KEY_READ = "read"
        def OpenKey(self, *a, **k): return object()
        def QueryValueEx(self, key, name):
            raise OSError("missing")
    # provide WindowsError alias for module
    import commands.windows as win_module
    monkeypatch.setattr(win_module, "WindowsError", OSError, raising=False)
    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    assert Windows.getenv("NAME") == ""


def test_windows_setenv(monkeypatch):
    class DummyKey:
        def __init__(self): pass
    called = {}
    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        HKEY_LOCAL_MACHINE = "system"
        KEY_READ = "read"
        KEY_ALL_ACCESS = "all"
        REG_EXPAND_SZ = "reg"
        def OpenKey(self, *args, **kwargs):
            called["open"] = args
            return DummyKey()
        def QueryValueEx(self, key, name):
            return ("VAL", None)
        def CloseKey(self, key):
            called["close"] = True
        def SetValueEx(self, key, name, *args, **kwargs):
            called["set"] = (key, name, args, kwargs)
    class DummyConsole:
        @staticmethod
        def get_output(*args, **kwargs):
            called["console"] = args
            return "ok"
    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    res = Windows.setenv("NAME", "VALUE")
    assert called["set"][1] == "NAME"
    assert res == "ok"
    called.clear()
    res = Windows.setenv("NAME", "VALUE", scope="system")
    assert called["open"][0] == "system"
    assert "CurrentControlSet" in called["open"][1]
    assert res == "ok"


def test_windows_power_shell_policy(monkeypatch):
    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False):
            return "policy\n", ""
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    assert Windows.get_powershell_execution_policy() == "policy"


def test_windows_dump_auditpol_handles_subprocess(monkeypatch):
    called = {}
    monkeypatch.setattr("commands.time.Time.dotted", lambda: "stamp")
    monkeypatch.setattr("commands.file.File.write", lambda path, data: called.update({"path": path, "data": data}))
    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            return "audit"
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    Windows.dump_auditpol(filename="out.txt", category="*", fast_name="fast", verbose=False)
    assert "auditpol_stamp--fast.txt" in called["path"]


# ---- from test_windows_extra.py ----


import types

import pytest

from commands.windows import Windows




def test_windows_get_cmd_code_page_failure(monkeypatch):
    import subprocess

    class DummyPopen:
        def __init__(self, *a, **k):
            pass

        def communicate(self):
            return b"", b"err"

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopen())
    assert Windows.get_cmd_code_page() == "Error getting current codepage"


def test_windows_get_cmd_code_page_parsing(monkeypatch):
    import subprocess

    class DummyPopen:
        def __init__(self, *a, **k):
            pass

        def communicate(self):
            return b"Active code page: 65001\r\n", b""

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopen())
    from commands import str as str_module
    monkeypatch.setattr(str_module.Str, "substring", staticmethod(lambda data, before, after=None: "65001"))
    assert Windows.get_cmd_code_page() == 65001


def test_windows_fix_unicode_encode_error_safe(monkeypatch):
    # Force lockfile behavior through File.exist
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: True))
    from commands.os import OS
    monkeypatch.setattr(OS, "_cyrillic_support", True)
    result = Windows.fix_unicode_encode_error(safe=True)
    assert result is not None


def test_windows_user_exists_calls_console(monkeypatch):
    calls = []

    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            calls.append(cmd)
            raise RuntimeError("bad")

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    try:
        Windows.user_exists("name")
    except RuntimeError:
        pass
    assert calls and "net user name" in calls[0]
    assert calls and "net user name" in calls[0]


def test_windows_get_cmd_code_page_debug_and_keyerror_fallback(monkeypatch):
    import subprocess

    printed = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: printed.append(a))

    class DummyPopenOk:
        def __init__(self, *a, **k):
            pass

        def communicate(self):
            return b"Active code page: 65001\r\n", b""

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopenOk())
    assert Windows.get_cmd_code_page(debug=True) == 65001
    assert printed

    class DummyPopenBad:
        def __init__(self, *a, **k):
            pass

        def communicate(self):
            return b"no code page here\r\n", b""

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopenBad())
    assert Windows.get_cmd_code_page(debug=False) == "Cannot get current codepage"


# ---- from test_windows_get_global_ip_paths.py ----


import types

from commands.windows import Windows


def test_windows_change_wallpaper(monkeypatch):
    calls = []

    class DummyUser32:
        @staticmethod
        def SystemParametersInfoA(*args):
            calls.append(("A", args))
        @staticmethod
        def SystemParametersInfoW(*args):
            calls.append(("W", args))

    class DummyWindll:
        user32 = DummyUser32()

    import ctypes
    monkeypatch.setattr(ctypes, "windll", DummyWindll, raising=False)
    Windows.change_wallpaper("img")
    assert ("A", (20, 0, "img", 0)) in calls
    assert ("W", (20, 0, "img", 3)) in calls




# ---- from test_windows_getenv_system_scope.py ----


from commands.windows import Windows


def test_windows_getenv_system_scope(monkeypatch):
    class DummyWinreg:
        HKEY_CURRENT_USER = "user"
        HKEY_LOCAL_MACHINE = "system"
        KEY_READ = "read"
        def OpenKey(self, *a, **k): return object()
        def QueryValueEx(self, key, name): return ("VALSYS", None)
    monkeypatch.setattr("commands.windows.Windows.import_winreg", classmethod(lambda cls: DummyWinreg()))
    assert Windows.getenv("NAME", scope="system") == "VALSYS"


# ---- from test_windows_instance.py ----


import pytest
from commands.windows import Windows






def test_windows_remote_factory(monkeypatch):
    captured = {}
    class DummyRS:
        def __init__(self, hostname, username, password, port=None, transport=None):
            captured.update({"hostname": hostname, "username": username, "password": password, "port": port, "transport": transport})
    monkeypatch.setattr(Windows, "RemoteSystem", DummyRS)
    r = Windows.remote("h", "u", "p", port=1234, transport="ssl")
    assert captured["hostname"] == "h"


# ---- from test_windows_locking_and_registry.py ----


import pytest

from commands.windows import Windows




def test_windows_lock_calls_ctypes_non_windows10(monkeypatch):
    import types

    class DummyOS:
        windows_version = 7

    called = {"cnt": 0}

    def lock_workstation():
        called["cnt"] += 1

    monkeypatch.setattr("commands.os.OS", DummyOS)
    monkeypatch.setattr("ctypes.windll", types.SimpleNamespace(LockWorkStation=lock_workstation), raising=False)
    Windows.lock()
    assert called["cnt"] == 1


def test_windows_import_winreg_sets_flag(monkeypatch):
    called = {}
    class DummyWinreg:
        KEY_READ = "read"
    class DummyOS:
        pass
    monkeypatch.setattr(Windows, "winreg_imported", False)
    monkeypatch.setattr("commands.os.OS", DummyOS)
    monkeypatch.setitem(__import__("sys").modules, "winreg", DummyWinreg)
    res = Windows.import_winreg()
    assert res is DummyWinreg
    assert Windows.winreg_imported is True


# ---- from test_windows_powershell_policy.py ----


import pytest

from commands.windows import Windows




def test_windows_powershell_policy_set_success(monkeypatch):
    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False):
            return "ok", ""

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    assert Windows.set_powershell_execution_policy("RemoteSigned") == "ok"


def test_windows_run_powershell_reuses_policy(monkeypatch):
    calls = []
    monkeypatch.setattr("commands.random.Random.string", staticmethod(lambda length: "abc"))
    monkeypatch.setattr("commands.file.File.write", lambda path, data: calls.append(("write", path, data)))
    monkeypatch.setattr("commands.file.File.delete", lambda path: calls.append(("delete", path)))
    monkeypatch.setattr("commands.windows.Windows.get_powershell_execution_policy",
                        classmethod(lambda cls: "RemoteSigned"))
    monkeypatch.setattr("commands.windows.Windows.set_powershell_execution_policy",
                        classmethod(lambda cls, policy: calls.append(("policy", policy))))

    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False, create_cmd_subprocess=False):
            calls.append(("cmd", cmd))
            return "ok", ""

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    out = Windows.run_powershell("Write-Host 'hi'")
    assert out == "ok"
    assert ("policy", "RemoteSigned") not in calls  # no change when already RemoteSigned


# ---- from test_windows_remote_system.py ----


import pytest

from commands.windows import Windows


def test_windows_remote_system_ps_and_cmd(monkeypatch):
    calls = []

    class DummySession:
        def __init__(self, *a, **k):
            pass

        def run_ps(self, script):
            calls.append(("ps", script))
            return type("Out", (), {"std_err": "#< CLIXML\r\nERROR", "std_out": b"ok", "status_code": 0})()

        def run_cmd(self, program, args):
            calls.append(("cmd", program, args))
            return type("Out", (), {"std_err": b"err", "std_out": b"out", "status_code": 1})()

    monkeypatch.setitem(__import__("sys").modules, "winrm", type("W", (), {"Session": lambda *a, **k: DummySession()}))

    rs = Windows.RemoteSystem("h", "u", "p")
    out, err, code = rs.ps("echo hi")
    assert out == "ok" and err == "ERROR" and code == 0

    out, err, code = rs.cmd("dir", "a")
    assert out == "out" and err == "err" and code == 1


def test_windows_remote_system_fix_run_ps_wraps_run_cmd(monkeypatch):
    import sys

    class DummyOut:
        def __init__(self, std_out=b"ok", std_err=b"ERR", status_code=0):
            self.std_out = std_out
            self.std_err = std_err
            self.status_code = status_code

    calls = []

    class DummySession:
        def __init__(self, *a, **k):
            pass

        def run_cmd(self, command, args=None):
            calls.append((command, args))
            return DummyOut(std_out=b"ok", std_err=b"ERR", status_code=0)

        def _clean_error_msg(self, msg):
            return "#< CLIXML\r\n" + msg

    sys.modules["winrm"] = type("W", (), {"Session": DummySession})

    rs = Windows.RemoteSystem("h", "u", "p")
    out, err, code = rs.ps("Write-Host hi")
    assert out == "ok"
    assert err == "ERR"
    assert code == 0
    assert calls and "powershell -encodedcommand" in calls[0][0]


def test_windows_instance_connect_and_methods(monkeypatch):
    class DummyRemote:
        def __init__(self, *a, **k):
            pass

        def ps(self, script):
            return ("out", "err", 0)

        def cmd(self, program, *args):
            return ("out2", "err2", 1)

    monkeypatch.setattr(Windows, "RemoteSystem", DummyRemote)
    w = Windows()
    w.connect("h", "u", "p")
    assert w.remote
    assert w.ps("echo")[0] == "out"
    assert w.cmd("dir")[0] == "out2"
    with pytest.raises(ValueError):
        Windows().ps("no remote")


# ---- from test_windows_remote_system_edge.py ----


import types

import pytest

from commands.windows import Windows


def test_remote_system_winrm_fix_and_error(monkeypatch):
    calls = {}

    class DummyWinrmSession:
        def __init__(self, *a, **k):
            pass

    def fake_run_ps(self, script):
        calls.setdefault("ps", []).append(script)
        # first call raise to test CLIXML path
        return type("Out", (), {"std_err": "#< CLIXML\r\nERR", "std_out": b"ok", "status_code": 1})()

    def fake_run_cmd(self, program, args):
        calls.setdefault("cmd", []).append((program, args))
        return type("Out", (), {"std_err": b"", "std_out": b"done", "status_code": 0})()

    class DummyWinrm:
        def __init__(self):
            self.Session = lambda *a, **k: type("Sess", (), {"run_ps": fake_run_ps, "run_cmd": fake_run_cmd})()

    monkeypatch.setitem(__import__("sys").modules, "winrm", DummyWinrm())
    rs = Windows.RemoteSystem("h", "u", "p")
    out, err, code = rs.ps("script")
    assert err == "ERR" and code == 1
    out2, err2, code2 = rs.cmd("prog", "arg1")
    assert out2 == "done" and err2 == "" and code2 == 0


def test_windows_remote_system_cmd_args(monkeypatch):
    recorded = {}
    class DummySession:
        def run_ps(self, script):
            return type("Out", (), {"std_err": b"", "std_out": b"", "status_code": 0})()
        def run_cmd(self, program, args):
            recorded["prog"] = program
            recorded["args"] = args
            return type("Out", (), {"std_err": b"", "std_out": b"ok", "status_code": 0})()
    class DummyWinrm:
        def __init__(self):
            class Session:
                run_ps = None
                def __init__(self, *a, **k):
                    pass
            self.Session = Session
    dummy_winrm = DummyWinrm()
    monkeypatch.setitem(__import__("sys").modules, "winrm", dummy_winrm)
    # inject new Session class with run_ps attribute writable
    dummy_winrm.Session.run_ps = lambda self, script: None
    dummy_winrm.Session.run_cmd = DummySession().run_cmd
    out, err, code = Windows.RemoteSystem("h", "u", "p").cmd("prog", "a", "b")
    assert recorded["args"] == ["a", "b"]
    assert out == "ok" and err == ""


# ---- from test_windows_remote_user_actions.py ----


import pytest

from commands.windows import Windows


def test_windows_remote_connect_sets_remote(monkeypatch):
    class DummyRemote:
        def __init__(self, *a, **k):
            self.args = (a, k)
        def ps(self, script): return ("ps", script)
        def cmd(self, program, *args): return ("cmd", program, args)

    monkeypatch.setattr(Windows, "RemoteSystem", DummyRemote)
    w = Windows()
    remote = w.connect("h", "u", "p")
    assert isinstance(remote, DummyRemote)
    assert w.ps("echo") == ("ps", "echo")
    assert w.cmd("dir", "/a") == ("cmd", "dir", ("/a",))
    # missing remote raises
    with pytest.raises(ValueError):
        Windows().cmd("dir")


def test_windows_remote_shortcut_factory(monkeypatch):
    class DummyRemote:
        def __init__(self, *a, **k): pass
    monkeypatch.setattr(Windows, "RemoteSystem", DummyRemote)
    inst = Windows.remote("h", "u", "p")
    assert isinstance(inst, DummyRemote)




# ---- from test_windows_set_cmd_page.py ----


import pytest

from commands.windows import Windows


def test_windows_set_cmd_code_page(monkeypatch):
    calls = []
    import subprocess
    class DummyPopen:
        def __init__(self, *a, **k):
            calls.append(("popen", a, k))
        def communicate(self):
            return b"Active code page: 437\r\n", b""
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopen(*a, **k))
    monkeypatch.setattr("os.system", lambda cmd: calls.append(("system", cmd)))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", lambda debug=False: 437)
    assert Windows.set_cmd_code_page(65001) == 65001
    assert calls[0][0] == "popen"


def test_windows_set_cmd_code_page_error(monkeypatch):
    import subprocess
    class DummyPopen:
        def __init__(self, *a, **k): pass
        def communicate(self):
            return b"", b"err"
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopen(*a, **k))
    monkeypatch.setattr("os.system", lambda cmd: None)
    res = Windows.set_cmd_code_page(437)
    assert res == 437


# ---- from test_windows_unicode_lockfile.py ----


import pytest

from commands.windows import Windows


def test_windows_fix_unicode_lockfile_safe(monkeypatch):
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/tmp/lock"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: True))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: 65001))
    assert Windows.fix_unicode_encode_error(safe=True) == 65001




def test_windows_fix_unicode_success_path(monkeypatch):
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/tmp/lock"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: False))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: 65001))
    monkeypatch.setattr("commands.windows.Windows.set_cmd_code_page", classmethod(lambda cls, cp: cp))
    monkeypatch.setattr("os.system", lambda cmd: 0)
    monkeypatch.setattr("commands.print.Print.multithread_safe", lambda *a, **k: None)
    assert Windows.fix_unicode_encode_error(safe=False) == 65001


def test_windows_fix_unicode_exception_safe_returns_previous_codepage(monkeypatch):
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/tmp/lock"))
    monkeypatch.setattr("commands.file.File.exist", staticmethod(lambda path: False))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", classmethod(lambda cls: 437))
    monkeypatch.setattr("commands.windows.Windows.set_cmd_code_page", classmethod(lambda cls, cp: cp))
    monkeypatch.setattr("commands.file.File.create", lambda path: None)
    monkeypatch.setattr("commands.print.Print.multithread_safe", lambda *a, **k: None)
    monkeypatch.setattr("os.system", lambda cmd: (_ for _ in ()).throw(RuntimeError("fail")))
    assert Windows.fix_unicode_encode_error(safe=True) == 437




# ---- from test_windows_user_exists_retry.py ----


import subprocess

from commands.windows import Windows


def test_windows_user_exists_success(monkeypatch):
    class DummyConsole:
        calls = []
        @classmethod
        def get_output(cls, cmd):
            cls.calls.append(cmd)
            return "ok"
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    assert Windows.user_exists("someone") is True


def test_windows_user_exists_called_process(monkeypatch):
    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            raise subprocess.CalledProcessError(1, cmd)
    monkeypatch.setattr("commands.console.Console", DummyConsole)
    assert Windows.user_exists("someone") is False


# ---- from test_windows_user_ops.py ----


import pytest

from commands.windows import Windows








def test_windows_user_create_success(monkeypatch):
    w = Windows()
    monkeypatch.setattr("commands.windows.Windows.user_exists", lambda self, name=None: False)

    class DummyConsole:
        @staticmethod
        def get_output(cmd):
            return "The command completed successfully."

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    assert w._user(username="name", password="pwd", create=True) is None








def test_windows_run_powershell_success(monkeypatch):
    calls = {"policies": []}
    monkeypatch.setattr("commands.random.Random.string", staticmethod(lambda length: "tempfile"))
    monkeypatch.setattr("commands.file.File.write", lambda path, data: calls.setdefault("write", (path, data)))
    monkeypatch.setattr("commands.file.File.delete", lambda path: calls.setdefault("delete", path))
    monkeypatch.setattr("commands.windows.Windows.get_powershell_execution_policy",
                        classmethod(lambda cls: "Restricted"))
    monkeypatch.setattr("commands.windows.Windows.set_powershell_execution_policy",
                        classmethod(lambda cls, policy: calls["policies"].append(policy)))

    class DummyConsole:
        @staticmethod
        def get_output(cmd, return_merged=False, create_cmd_subprocess=False):
            calls["cmd"] = cmd
            return "ok", ""

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    out = Windows.run_powershell("Write-Host 'hi'")
    assert out == "ok"
    assert calls["write"][0] == "tempfile.ps1"
    assert calls["delete"] == "tempfile.ps1"
    # Policies should be set to RemoteSigned then restored
    assert calls["policies"] == ["RemoteSigned", "Restricted"]

def test_console_auto_decoding_unix_family_branch(monkeypatch):
    from commands.console import Console
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", False, raising=False)
    monkeypatch.setattr(OS, "_unix_family", True, raising=False)

    out = Console.get_output(sys.executable, "-c", "print('utf8-branch')", auto_decoding=True)
    assert "utf8-branch" in out.lower()

def test_os_name_linux_branch(monkeypatch):
    from commands.os import OS

    monkeypatch.setattr(OS, "_name", None, raising=False)
    monkeypatch.setattr(OS, "_sys_platform", "linux", raising=False)
    assert OS.name == "linux"

def test_file_get_mime_non_windows_import_magic(monkeypatch, tmp_path):
    from commands.file import File
    from commands.os import OS

    class DummyMagic:
        @staticmethod
        def from_file(_path, mime=True):
            return "text/plain"

    monkeypatch.setattr(OS, "_windows", False, raising=False)
    monkeypatch.setitem(sys.modules, "magic", DummyMagic)

    target = tmp_path / "t.txt"
    target.write_text("data")
    assert File.get_mime(target) == "text/plain"

def test_dir_copy_symlink_branch(monkeypatch, tmp_path):
    import os as os_module

    from commands.dir import Dir

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "link").write_text("not-a-symlink")

    removed = []
    symlinks = []

    monkeypatch.setattr(os_module.path, "islink", lambda p: str(p).endswith("link"))
    monkeypatch.setattr(os_module.path, "lexists", lambda _p: True)
    monkeypatch.setattr(os_module, "remove", lambda p: removed.append(p))
    monkeypatch.setattr(os_module, "readlink", lambda _p: "target")
    monkeypatch.setattr(os_module, "symlink", lambda target, name: symlinks.append((target, name)))

    class DummyStat:
        st_mode = 0o777

    monkeypatch.setattr(os_module, "lstat", lambda _p: DummyStat())

    def raise_lchmod(_p, _mode):
        raise OSError("lchmod not available")

    monkeypatch.setattr(os_module, "lchmod", raise_lchmod, raising=False)

    Dir.copy(str(src), str(dst), symlinks=True)
    assert removed
    assert symlinks

def test_archive_tar_filter_set_on_py312(monkeypatch):
    from commands.archive import Archive

    class DummyTar:
        def __init__(self):
            self.extract_kwargs = None
            self.extractall_kwargs = None

        def extract(self, *args, **kwargs):
            self.extract_kwargs = kwargs
            return "ok"

        def extractall(self, *args, **kwargs):
            self.extractall_kwargs = kwargs
            return "ok"

    dummy = DummyTar()
    monkeypatch.setattr(sys, "version_info", (3, 12, 0))
    arch = Archive("test.tar.gz", archive_type=Archive.MODE_TARGZ)
    assert arch._extract_single(dummy, "x", "out", archive_type=Archive.MODE_TARGZ) == "ok"
    assert arch._extract_all(dummy, "y", archive_type=Archive.MODE_TARGZ) == "ok"
    assert dummy.extract_kwargs.get("filter") == "data"
    assert dummy.extractall_kwargs.get("filter") == "data"

class TestWindowsMissingCoverage:
    """Tests to cover missing lines in windows.py"""
    def test_windows_init_with_remote_params(self, monkeypatch):
        """Test Windows.__init__ with remote parameters (line 16)"""
        # Mock winrm to avoid actual remote connection
        class MockWinRM:
            class Session:
                def __init__(self, *args, **kwargs):
                    pass
                @staticmethod
                def run_ps(script):
                    pass

        monkeypatch.setitem(sys.modules, "winrm", types.SimpleNamespace(Session=MockWinRM.Session))
        monkeypatch.setattr("winrm.Session", MockWinRM.Session, raising=False)

        # This should create a remote instance
        win = Windows(hostname="test.host", username="user", password="pass")
        assert win.remote is not None
    def test_windows_create_user_wrapper(self, monkeypatch):
        """Test create_user method (line 228)"""
        called_with = {}

        def mock_user(self, username=None, password=None, create=False, remove=False, retry_cnt=0):
            called_with['username'] = username
            called_with['password'] = password
            called_with['create'] = create
            return None

        monkeypatch.setattr(Windows, '_user', mock_user)

        win = Windows()
        win.create_user("testuser", "testpass")

        assert called_with['username'] == "testuser"
        assert called_with['password'] == "testpass"
        assert called_with['create'] is True
    def test_windows_remove_user_wrapper(self, monkeypatch):
        """Test remove_user method (line 235)"""
        called_with = {}

        def mock_user(self, username=None, password=None, create=False, remove=False, retry_cnt=0):
            called_with['username'] = username
            called_with['remove'] = remove
            return None

        monkeypatch.setattr(Windows, '_user', mock_user)

        win = Windows()
        win.remove_user("testuser")

        assert called_with['username'] == "testuser"
        assert called_with['remove'] is True
    def test_get_cmd_code_page_debug(self, monkeypatch, capsys):
        """Test get_cmd_code_page with debug=True (lines 111, 114)"""
        if os.name != 'nt':
            pytest.skip("Windows-only test")

        Windows.get_cmd_code_page(debug=True)

        captured = capsys.readouterr()
        # Debug mode should print output
        assert len(captured.out) > 0
    def test_fix_unicode_encode_error_returns_previous_codepage(self, monkeypatch):
        """Test fix_unicode_encode_error returns previous codepage (line 205)."""
        import os as os_module

        def bad_system(*_args, **_kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr(Windows, "get_cmd_code_page", staticmethod(lambda *_a, **_k: "Error getting current codepage"))
        monkeypatch.setattr(os_module, "system", bad_system)

        assert Windows.fix_unicode_encode_error(safe=True) == "Error getting current codepage"
