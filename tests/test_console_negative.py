# Consolidated tests for commands/console.py (negative)

# ---- from test_console_negative.py ----

# Placeholder for future tests.
import pytest
import sys
from commands.console import Console
from commands.os import OS
import builtins
import itertools
import os
from unittest.mock import patch, Mock, MagicMock
import types

class TestConsoleCoverage:
    """Tests to improve coverage for console9.py"""
    @staticmethod
    def _py_cmd(code: str):
        return [sys.executable, "-c", code]

    def test_get_output_empty_commands(self):
        """Test Console.get_output with empty commands (lines 201-202)"""
        with pytest.raises(IndexError):
            Console.get_output([])
    def test_get_output_decoding_universal_newlines_conflict(self):
        """Test Console.get_output with both decoding and universal_newlines (lines 245-246)"""
        with pytest.raises(TypeError):
            Console.get_output(*self._py_cmd("print('test')"), decoding="utf-8", universal_newlines=True)
def test_console_get_output_decoding_conflict():
    with pytest.raises(TypeError):
        Console.get_output("echo test", decoding="utf-8", universal_newlines=True)

def test_console_get_output_invalid_decoding_combo(monkeypatch):
    from commands.os import OS
    monkeypatch.setattr(OS, "_windows", False)
    with pytest.raises(TypeError):
        Console.get_output("echo hi", decoding="utf-8", universal_newlines=True)

def test_console_fit_returns_empty_when_width_non_positive():
    assert Console.fit("x", 0) == ""

def test_console_height_no_stty(monkeypatch):
    # Force unix_family True and make get_output return empty to raise IndexError
    from commands.os import OS
    monkeypatch.setattr(OS, "_windows", False, raising=False)
    monkeypatch.setattr(OS, "_unix_family", True)
    monkeypatch.setattr("commands.console.Console.get_output", lambda *a, **k: "")
    with pytest.raises(IndexError):
        Console.height()

def test_console__resolve_commands_raises():
    c = Console()
    with pytest.raises(ValueError):
        c.run()

def test_console_get_output_invalid_decoding_and_universal(monkeypatch):
    with pytest.raises(TypeError):
        Console.get_output("echo test", decoding="utf-8", universal_newlines=True)

def test_console_get_output_empty(monkeypatch):
    with pytest.raises(IndexError):
        Console.get_output([])


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"interval": 0}, "interval"),
        ({"fade_duration": 0}, "fade_duration"),
        ({"fade_steps": 0}, "fade_steps"),
    ],
)
def test_console_watch_rejects_nonpositive_timing(kwargs, message):
    with pytest.raises(ValueError, match=message):
        Console.watch(lambda: "ok", **kwargs)
