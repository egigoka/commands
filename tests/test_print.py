# Consolidated tests for commands/print.py (unit)

# ---- from test_print9.py ----


import pytest
from commands.print import Print


def test_multithread_safe(capsys):
    Print.multithread_safe("Hello", "World")
    captured = capsys.readouterr()
    assert "Hello World" in captured.out


def test_call_works_as_multithread_safe(capsys):
    Print("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out


def test_prettify_dict():
    data = {"a": 1, "b": 2, "c": 3}
    result = Print.prettify(data, verbose=False)
    assert "{'a': 1" in result or "{'b': 2" in result or "{'c': 3" in result


def test_prettify_list():
    data = [1, 2, 3, 4, 5]
    result = Print.prettify(data, verbose=False)
    assert "[1, 2, 3, 4, 5]" in result


def test_prettify_nested():
    data = {"outer": {"inner": [1, 2, 3]}}
    result = Print.prettify(data, verbose=False)
    assert "outer" in result
    assert "inner" in result


def test_colored_basic():
    pytest.importorskip("termcolor")
    result = Print.colored("Test", "red", verbose=False)
    assert "Test" in result


def test_colored_with_highlight():
    pytest.importorskip("termcolor")
    result = Print.colored("Test", "red", "on_white", verbose=False)
    assert "Test" in result


def test_colored_reverse_order():
    pytest.importorskip("termcolor")
    result = Print.colored("Test", "on_white", "red", verbose=False)
    assert "Test" in result


def test_colored_multiple_strings():
    pytest.importorskip("termcolor")
    result = Print.colored("Hello", "World", "red", verbose=False)
    assert "Hello" in result
    assert "World" in result


def test_color_output_enabled():
    assert isinstance(Print.color_output_enabled, bool)


# Negative tests
def test_prettify_invalid_type():
    """Should handle non-pretty-printable types gracefully"""
    class CustomClass:
        pass

    obj = CustomClass()
    result = Print.prettify(obj, verbose=False)
    assert isinstance(result, str)


def test_colored_invalid_color():
    """Should handle invalid color names"""
    pytest.importorskip("termcolor")
    result = Print.colored("Test", "not_a_real_color", verbose=False)
    # Should return the text even if color is invalid
    assert "Test" in result


def test_print_prefix(capsys):
    prefixed = Print.prefix("[DBG]")
    prefixed("hello")
    captured = capsys.readouterr()
    assert "[DBG]" in captured.out and "hello" in captured.out


def test_print_prefix_multiple_args(capsys):
    """Test prefix with multiple arguments"""
    prefixed = Print.prefix("DEBUG", "2023")
    prefixed("message")
    captured = capsys.readouterr()
    assert "DEBUG 2023" in captured.out
    assert "message" in captured.out


def test_print_prefix_custom_sep(capsys):
    """Test prefix with custom separator"""
    prefixed = Print.prefix("A", "B", "C", sep="-")
    prefixed("test")
    captured = capsys.readouterr()
    assert "A-B-C" in captured.out
    assert "test" in captured.out


def test_debug_basic(capsys):
    """Test Print.debug method"""
    Print.debug("test string")
    captured = capsys.readouterr()
    assert "<<<Debug sheet:>>>" in captured.out
    assert "test string" in captured.out
    assert "<<<End of debug sheet>>>" in captured.out


def test_debug_multiple_strings(capsys):
    """Test Print.debug with multiple strings"""
    Print.debug("first", "second", "third")
    captured = capsys.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out
    assert "third" in captured.out
    assert "<<<Debug sheet:>>>" in captured.out


def test_debug_raw_mode(capsys):
    """Test Print.debug with raw=True"""
    Print.debug("test\nstring", raw=True)
    captured = capsys.readouterr()
    assert "<<<Debug sheet:>>>" in captured.out
    # Should show repr() output
    assert "test" in captured.out


def test_debug_bytes(capsys):
    """Test Print.debug with bytes"""
    Print.debug(b"byte string")
    captured = capsys.readouterr()
    assert "<<<Debug sheet:>>>" in captured.out
    assert "byte string" in captured.out


def test_rewrite_basic(capsys):
    """Test Print.rewrite method"""
    Print.rewrite("test message")
    captured = capsys.readouterr()
    assert "test message" in captured.out


def test_rewrite_multiple_strings(capsys):
    """Test Print.rewrite with multiple strings"""
    Print.rewrite("first", "second", "third")
    captured = capsys.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out
    assert "third" in captured.out


def test_rewrite_custom_sep(capsys):
    """Test Print.rewrite with custom separator"""
    Print.rewrite("a", "b", "c", sep="-")
    captured = capsys.readouterr()
    output = captured.out
    # Should have separator between strings
    assert "a" in output and "b" in output and "c" in output


def test_rewrite_fit_false(capsys):
    """Test Print.rewrite with fit=False"""
    Print.rewrite("message", fit=False)
    captured = capsys.readouterr()
    assert "message" in captured.out


# ---- from test_print_more_coverage.py ----


import os
import sys
import types

import pytest

from commands.print import Print
from commands.os import OS


def test_print_prettify_verbose_prints(capsys):
    Print.prettify({"a": 1}, verbose=True)
    out = capsys.readouterr().out
    assert "a" in out


def test_print_rewrite_windows_trims_width(monkeypatch, capsys):
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr("commands.console.Console.width", classmethod(lambda cls: 5))
    monkeypatch.setattr("commands.console.Console.fit", classmethod(lambda cls, *a, **k: ["x"]))
    Print.rewrite("abc", fit=True)
    assert capsys.readouterr().out == "    \rx\r"


def test_print_colored_no_color_env_returns_plain(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    Print._color_output_enabled = None

    termcolor = types.SimpleNamespace(
        COLORS={},
        HIGHLIGHTS={},
        colored=lambda s, **_k: f"COLOR({s})",
    )
    monkeypatch.setitem(sys.modules, "termcolor", termcolor)

    out = Print.colored("hi", verbose=False)
    assert out == "hi"


def test_print_colored_windows_inits_colorama(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    Print._color_output_enabled = None
    Print.colorama_inited = False
    monkeypatch.setattr(OS, "_windows", True)

    called = {"init": 0}
    monkeypatch.setitem(sys.modules, "colorama", types.SimpleNamespace(init=lambda: called.__setitem__("init", called["init"] + 1)))
    termcolor = types.SimpleNamespace(
        COLORS={},
        HIGHLIGHTS={},
        colored=lambda s, **_k: s,
    )
    monkeypatch.setitem(sys.modules, "termcolor", termcolor)

    Print.colored("x", "red", verbose=False)
    assert called["init"] == 1


def test_print_colored_keyerror_guard(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    Print._color_output_enabled = None

    class KeyErrorContainer(dict):
        def __contains__(self, item):
            raise KeyError(item)

    termcolor = types.SimpleNamespace(
        COLORS=KeyErrorContainer(),
        HIGHLIGHTS=KeyErrorContainer(),
        colored=lambda s, **_k: s,
    )
    monkeypatch.setitem(sys.modules, "termcolor", termcolor)

    assert Print.colored("hi", verbose=False) == "hi"
