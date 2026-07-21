# Consolidated tests for commands/macos.py (unit)

# ---- from test_coverage_macos_extra.py ----


#! python3
# -*- coding: utf-8 -*-
"""Extra coverage for macOS runs."""
import os
import sys
import types
import tempfile

from commands import Dir, File, OS, Path






def test_os_name_linux_branch(monkeypatch):
    monkeypatch.setattr(OS, "_name", None, raising=False)
    monkeypatch.setattr(OS, "_sys_platform", "linux", raising=False)
    assert OS.name == "linux"


def test_path_temp_non_macos(monkeypatch):
    monkeypatch.setattr(OS, "_macos", False, raising=False)
    assert Path.temp() == tempfile.gettempdir()


# ---- from test_macos9.py ----


import pytest


def test_macos9_import():
    from commands import macOS
    assert macOS is not None




def test_macos_callable_sets_message(monkeypatch):
    from commands.macos import macOS
    called = {}
    monkeypatch.setattr(macOS, "notification", lambda *a, **k: called.update({"args": a, "kwargs": k}))
    m = macOS(message="hi")
    m()
    assert called["args"][0] == "hi"


def test_macos_instance_helper(monkeypatch):
    from commands.macos import macOS
    from commands.os import OS
    calls = []
    monkeypatch.setattr(OS, "_macos", True)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_linux", False)
    monkeypatch.setattr(macOS, "notification", lambda *a, **k: calls.append((a, k)))

    m = macOS("hello")
    m.notify(debug=True)
    assert calls


# ---- from test_macos_instance_extra.py ----


import pytest
from commands.macos import macOS


def test_macos_osascript_escape():
    s = 'He said "hi"'
    escaped = macOS.OSAScript.quotes_escape(s)
    assert '\\"' in escaped or '\\\\\"' in escaped


def test_macos_notification_builds_command(monkeypatch):
    cmds = {}
    import commands.macos as mod
    mod.Str = type("S", (), {"to_quotes": staticmethod(lambda x: f'"{x}"')})
    import commands.os as os_mod
    monkeypatch.setattr(os_mod.OS, "system", lambda cmd: cmds.update({"cmd": cmd}))
    macOS.notification("msg", title="title", subtitle="sub", sound="snd", debug=True)
    assert "osascript" in cmds.get("cmd", "") or "command=" in cmds.get("cmd", "")


# ---- from test_macos_more.py ----


import pytest

from commands.macos import macOS


def test_macos_instance_call_updates_fields_and_calls_notification(monkeypatch):
    captured = {}

    def fake_notification(message, title="python3", subtitle=None, sound=None, debug=False):
        captured.update(
            {
                "message": message,
                "title": title,
                "subtitle": subtitle,
                "sound": sound,
                "debug": debug,
            }
        )

    monkeypatch.setattr(macOS, "notification", staticmethod(fake_notification))
    notifier = macOS("hi")
    notifier("msg", title="t", subtitle="s", sound="snd", debug=True)
    assert captured == {
        "message": "msg",
        "title": "t",
        "subtitle": "s",
        "sound": "snd",
        "debug": True,
    }


def test_macos_get_list_of_sounds_verbose(monkeypatch):
    calls = {}

    monkeypatch.setattr("commands.dir.Dir.list_of_files", staticmethod(lambda p: [p + "/a"]))
    monkeypatch.setattr("commands.path.Path.combine", staticmethod(lambda *p: "/".join(p)))

    def fake_debug(*args, **kwargs):
        calls["debug"] = args

    monkeypatch.setattr("commands.print.Print.debug", fake_debug)
    out = macOS.get_list_of_sounds(verbose=True)
    assert "/".join(["System", "Library", "Sounds"]) + "/a" in out
    assert "/".join(["~", "Library", "Sounds"]) + "/a" in out
    assert "debug" in calls


def test_macos_symlink_calls_ln(monkeypatch):
    captured = {}

    def fake_start(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

    monkeypatch.setattr("commands.process.Process.start", staticmethod(fake_start))
    macOS.symlink("/real", "/link")
    assert captured["args"][0] == "ln"
    assert captured["args"][1] == "-s"
