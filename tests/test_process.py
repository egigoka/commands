# Consolidated tests for commands/process.py (unit)

# ---- from test_process9.py ----


import pytest


def test_process9_import():
    from commands import Process
    assert Process is not None


def test_process_instance_helper(monkeypatch):
    from commands.process import Process
    from commands.console import Console

    called = []
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: called.append((a, k)))

    p = Process(target="python")
    p.kill_target()
    assert called


def test_process_kill_windows_pid(monkeypatch):
    from commands.process import Process
    from commands.console import Console
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    recorded = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: recorded.update({"args": a, "kwargs": k}))

    Process.kill(1234)
    assert recorded["args"][0] == "taskkill /f /pid 1234"


def test_process_kill_windows_exe(monkeypatch):
    from commands.process import Process
    from commands.console import Console
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    captured = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: captured.update({"args": a, "kwargs": k}))

    Process.kill("notepad")
    assert captured["args"][0] == "taskkill /f /im notepad.exe"


def test_process_kill_unix(monkeypatch):
    from commands.process import Process
    from commands.console import Console
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)
    sent = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: sent.update({"args": a, "kwargs": k}))

    Process.kill("python")
    assert sent["args"][0] == "killall python"




def test_process_call_sets_target(monkeypatch):
    from commands.process import Process
    from commands.console import Console
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: None)

    p = Process()
    p("sleep")
    assert p.target == "sleep"




# ---- from test_process_more_coverage.py ----


import pytest

from commands.process import Process


def test_process_call_without_arg_kills_target(monkeypatch):
    called = {}

    def fake_kill(cls, target):
        called["target"] = target
        return "ok"

    monkeypatch.setattr(Process, "kill", classmethod(fake_kill))

    p = Process("abc")
    assert p() == "ok"
    assert called["target"] == "abc"


def test_process_kill_unix_pid_uses_kill(monkeypatch):
    from commands.os import OS

    monkeypatch.setattr(OS, "_unix_family", True)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr("commands.console.Console.get_output", lambda cmd, **_k: cmd)

    out = Process.kill("123")
    assert out == "kill 123"




# ---- from test_process_start_more.py ----


from commands.process import Process


def test_process_start_calls_console_get_output(monkeypatch):
    captured = {}

    def fake_get_output(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return "ok"

    monkeypatch.setattr("commands.console.Console.get_output", fake_get_output)

    out = Process.start("echo hi", pureshell=True, print_std=True, timeout=1)
    assert out == "ok"
    assert captured["cmd"] == "echo hi"
    assert captured["kwargs"]["pure_shell"] is True
    assert captured["kwargs"]["print_std"] is True
    assert captured["kwargs"]["timeout"] == 1


def test_process_start_single_arg_sequence(monkeypatch):
    captured = {}

    def fake_get_output(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return "ok"

    monkeypatch.setattr("commands.console.Console.get_output", fake_get_output)

    Process.start(["echo", "hi"], pure_shell=False)
    assert captured["cmd"] == ["echo", "hi"]
    assert captured["kwargs"]["pure_shell"] is False
