# Consolidated tests for commands/process.py (negative)

# ---- from test_process_negative.py ----

# Placeholder for future tests.
import pytest
from commands.process import Process

def test_process_kill_invalid_os(monkeypatch):
    from commands.process import Process
    from commands.os import OS

    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", False)
    with pytest.raises(NotImplementedError):
        Process.kill("python")

def test_process_kill_target_without_target():
    from commands.process import Process
    p = Process()
    with pytest.raises(ValueError):
        p.kill_target()

def test_process_kill_unsupported_os_raises(monkeypatch):
    from commands.os import OS

    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr(OS, "_windows", False)

    with pytest.raises(NotImplementedError):
        Process.kill("x")
