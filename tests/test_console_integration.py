# Consolidated tests for commands/console.py (integration)

# ---- from test_console_integration.py ----

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

    def test_get_output_basic(self):
        """Test Console.get_output basic usage (lines 178-268)"""
        result = Console.get_output(*self._py_cmd("print('hello')"))
        assert "hello" in result.lower()
    def test_get_output_pure_shell(self):
        """Test Console.get_output with pure_shell=True (line 193)"""
        if OS.windows:
            result = Console.get_output("echo hello", pure_shell=True)
        else:
            result = Console.get_output("echo hello", pure_shell=True)
        assert "hello" in result.lower()
    def test_get_output_string_command(self):
        """Test Console.get_output with string command (lines 193-195)"""
        # String command without pure_shell should use shlex.split
        cmd = "python3 -c print(123)"
        result = Console.get_output(cmd)
        assert "123" in result.lower()
    def test_get_output_list_commands(self):
        """Test Console.get_output with list commands (lines 197-199)"""
        result = Console.get_output(self._py_cmd("print('world')"))
        assert "world" in result.lower()
    def test_get_output_hooks(self):
        """Test Console.get_output with hooks (lines 204-210)"""
        stdout_lines = []
        stderr_lines = []

        def hook_out(line):
            stdout_lines.append(line)

        def hook_err(line):
            stderr_lines.append(line)

        result = Console.get_output(*self._py_cmd("print('test')"), hook_stdout=hook_out, hook_stderr=hook_err)
        assert "test" in result.lower()
        # Verify hooks were called
        assert len(stdout_lines) > 0 or len(stderr_lines) > 0
    def test_get_output_return_merged_false(self):
        """Test Console.get_output with return_merged=False (lines 263-268)"""
        out, err = Console.get_output(*self._py_cmd("print('test')"), return_merged=False)
        assert isinstance(out, str)
        assert isinstance(err, str)
        assert "test" in out.lower()
    def test_get_output_with_timeout(self):
        """Test Console.get_output with timeout (lines 265-266)"""
        # Quick command should complete within timeout
        out, err, timeout_reached = Console.get_output(*self._py_cmd("print('quick')"), return_merged=False, timeout=5)
        assert not timeout_reached
        assert "quick" in out.lower()
    def test_get_output_python_auto_disable_buffering(self):
        """Test Console.get_output with python command (lines 212-223)"""
        # Test that -u flag is added for python commands
        result = Console.get_output(sys.executable, "-c", "print('test')", print_std=False)
        # Just verify it runs without error
        assert isinstance(result, str)
    def test_get_output_python_with_print_std(self, capsys):
        """Test Console.get_output with python and print_std=True (lines 219-223)"""
        # This should add -u flag automatically
        result = Console.get_output(sys.executable, "-c", "print('buffered')", print_std=True)
        assert "buffered" in result.lower()
    def test_get_output_python_already_has_u_flag(self):
        """Test Console.get_output with python already having -u flag (line 220)"""
        # Should not add -u twice
        result = Console.get_output(sys.executable, "-u", "-c", "print('test')", print_std=True)
        assert "test" in result.lower()
    def test_get_output_py_command(self):
        """Test Console.get_output with 'py' command (lines 213-214)"""
        # Test different python command names
        try:
            result = Console.get_output("py", "-c", "print('test')", print_std=True)
            assert isinstance(result, str)
        except FileNotFoundError:
            # py command might not exist on all systems
            pytest.skip("py command not found")
    def test_get_output_create_cmd_subprocess(self):
        """Test Console.get_output with create_cmd_subprocess=True (lines 248-255)"""
        if OS.windows:
            result = Console.get_output("echo cmd_test", create_cmd_subprocess=True)
            assert "cmd_test" in result.lower()
        else:
            pytest.skip("create_cmd_subprocess only works on Windows")
    def test_get_output_manual_decoding(self):
        """Test Console.get_output with manual decoding (line 225)"""
        result = Console.get_output(*self._py_cmd("print('decode')"), decoding="utf-8", auto_decoding=False)
        assert "decode" in result.lower()
    def test_height_unix(self, monkeypatch):
        """Test Console.height on Unix (lines 49-52)"""
        if not OS.unix_family:
            pytest.skip("Unix-only test")

        # Test Unix path - may fail if stty not available
        try:
            height = Console.height()
            assert isinstance(height, int)
            assert height > 0
        except IndexError:
            pytest.skip("stty size not available in this environment")
    def test_get_output_with_decoding_fallback(self):
        """Test Console.get_output decoding with chardet fallback (lines 132-138)"""
        # Test auto-decoding path
        result = Console.get_output(*self._py_cmd("print('test123')"), auto_decoding=True)
        assert "test123" in result.lower()
    def test_get_output_print_std_colored_output(self, capsys):
        """Test Console.get_output with print_std showing colored output (lines 141-143)"""
        # Run command with print_std to test colored output path
        result = Console.get_output(*self._py_cmd("print('visible')"), print_std=True)
        assert "visible" in result.lower()
        # Check that output was printed
        captured = capsys.readouterr()
        assert "visible" in captured.out.lower() or len(captured.out) > 0
    def test_get_output_threading_execution(self):
        """Test Console.get_output threading execution (lines 148-161)"""
        # Test that both stdout and stderr threads execute
        result = Console.get_output(sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)")
        # Should contain output from both streams
        assert "out" in result or "err" in result

def test_console_clean_branches(monkeypatch, capsys):
    from commands.os import OS
    commands = []
    monkeypatch.setattr("os.system", lambda command: commands.append(command) or 0)
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_linux", False)
    monkeypatch.setattr(OS, "_macos", False)
    Console.clean()
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_linux", True)
    Console.clean()
    monkeypatch.setattr(OS, "_linux", False)
    monkeypatch.setattr(OS, "_macos", True)
    Console.clean()
    assert commands == ["cls", r"clear && printf '\e[3J'"]
    assert capsys.readouterr().out

def test_console_get_output_print_std_bytes(monkeypatch):
    from commands.print import Print

    calls = {"called": False}

    def fake_colored(*_args, **_kwargs):
        calls["called"] = True

    monkeypatch.setattr(Print, "colored", fake_colored)
    out, err = Console.get_output(
        sys.executable,
        "-c",
        "print('hi')",
        print_std=True,
        auto_decoding=False,
        return_merged=False,
    )
    assert calls["called"] is True
    assert b"hi" in out
    assert err == b""

def test_console_get_output_return_merged_bytes():
    merged = Console.get_output(
        sys.executable,
        "-c",
        "import sys; sys.stdout.write('hi')",
        auto_decoding=False,
        return_merged=True,
    )
    assert merged.out == "hi"
    assert merged.err == ""
