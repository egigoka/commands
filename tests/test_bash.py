# Consolidated tests for commands/bash.py (unit)

# ---- from test_bash9.py ----


import pytest
from commands.bash import Bash


class TestBashEscape:
    """Tests for escape functionality."""

    def test_escape_simple_string(self):
        """Simple strings without special chars stay unquoted."""
        # shlex.quote only quotes when necessary
        assert Bash("hello").escape() == "hello"

    def test_escape_with_spaces(self):
        """Strings with spaces are properly quoted."""
        result = Bash("hello world").escape()
        assert result == "'hello world'"

    def test_escape_with_special_chars(self):
        """Special shell characters are escaped."""
        result = Bash("test; rm -rf /").escape()
        # shlex.quote wraps in single quotes
        assert result == "'test; rm -rf /'"

    def test_escape_with_single_quotes(self):
        """Single quotes inside string are handled."""
        result = Bash("it's").escape()
        # shlex escapes single quotes by ending quote, adding escaped quote, starting new quote
        assert result == "'it'\"'\"'s'"

    def test_escape_with_argument(self):
        """escape() can take an explicit argument."""
        b = Bash("stored")
        result = b.escape("other")
        # Simple string, no quoting needed
        assert result == "other"

    def test_escape_argument_with_spaces(self):
        """escape() with argument containing spaces."""
        b = Bash("stored")
        result = b.escape("hello world")
        assert result == "'hello world'"

    def test_escape_empty_string(self):
        """Empty string produces empty quotes."""
        result = Bash("").escape()
        assert result == "''"

    def test_escape_unicode(self):
        """Unicode characters are preserved."""
        result = Bash("Привет мир 你好").escape()
        # Has spaces, so quoted
        assert result == "'Привет мир 你好'"

    def test_escape_backslash(self):
        """Backslashes are properly escaped."""
        result = Bash("path\\file").escape()
        assert result == "'path\\file'"


class TestBashRun:
    """Tests for command execution."""

    def test_run_simple_command(self, monkeypatch):
        """run() executes the stored command."""
        from commands import console
        called = {}
        monkeypatch.setattr(console.Console, "get_output",
                            lambda *a, **k: called.update({"args": a, "kwargs": k}) or "output")

        result = Bash("echo hello").run()
        assert called["args"][0] == "echo hello"
        assert result == "output"

    def test_call_is_alias_for_run(self, monkeypatch):
        """__call__ is an alias for run()."""
        from commands import console
        called = {}
        monkeypatch.setattr(console.Console, "get_output",
                            lambda *a, **k: called.update({"args": a, "kwargs": k}) or "output")

        result = Bash("echo hello")()
        assert called["args"][0] == "echo hello"
        assert result == "output"

    def test_run_with_pure_shell_false(self, monkeypatch):
        """pure_shell parameter is passed through."""
        from commands import console
        called = {}
        monkeypatch.setattr(console.Console, "get_output",
                            lambda *a, **k: called.update({"args": a, "kwargs": k}) or "output")

        Bash("echo hello").run(pure_shell=False)
        assert called["kwargs"]["pure_shell"] is False




class TestBashAppend:
    """Tests for command building with append()."""

    def test_append_single_arg(self):
        """append() adds escaped argument."""
        b = Bash("grep")
        b.append("pattern")
        # Simple arg, no quoting needed
        assert b.command == "grep pattern"

    def test_append_multiple_args(self):
        """append() handles multiple arguments."""
        b = Bash("grep")
        b.append("-r", "pattern", "/path")
        # Simple args, no quoting needed
        assert b.command == "grep -r pattern /path"

    def test_append_with_spaces(self):
        """append() escapes spaces in arguments."""
        b = Bash("grep")
        b.append("hello world")
        assert b.command == "grep 'hello world'"

    def test_append_chainable(self):
        """append() returns self for chaining."""
        b = Bash("cmd")
        result = b.append("a").append("b")
        assert result is b
        assert b.command == "cmd a b"

    def test_append_to_empty(self):
        """append() works on empty command."""
        b = Bash()
        b.append("ls", "-la")
        assert b.command == "ls -la"

    def test_append_special_chars(self):
        """append() escapes special characters."""
        b = Bash("echo")
        b.append("$HOME")
        assert "$HOME" in b.command
        # Should be quoted to prevent expansion
        assert "'" in b.command

    def test_append_mixed_args(self):
        """append() handles mix of simple and complex args."""
        b = Bash("grep")
        b.append("-r", "hello world", "/path")
        assert b.command == "grep -r 'hello world' /path"


class TestBashSplit:
    """Tests for command splitting."""

    def test_split_simple(self):
        """split() parses simple commands."""
        parts = Bash("ls -la /tmp").split()
        assert parts == ["ls", "-la", "/tmp"]

    def test_split_quoted(self):
        """split() handles quoted strings."""
        parts = Bash("grep 'hello world' file.txt").split()
        assert parts == ["grep", "hello world", "file.txt"]

    def test_split_empty(self):
        """split() on empty returns empty list."""
        parts = Bash("").split()
        assert parts == []

    def test_split_double_quotes(self):
        """split() handles double-quoted strings."""
        parts = Bash('echo "hello world"').split()
        assert parts == ["echo", "hello world"]


class TestBashInit:
    """Tests for initialization."""

    def test_init_with_command(self):
        """Init stores the command."""
        b = Bash("ls -la")
        assert b.command == "ls -la"

    def test_init_empty(self):
        """Init with no args creates empty command."""
        b = Bash()
        assert b.command == ""

    def test_init_default_is_empty_string(self):
        """Default command is empty string, not None."""
        b = Bash()
        assert b.command == ""
        assert isinstance(b.command, str)
