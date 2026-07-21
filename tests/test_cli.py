# Consolidated tests for commands/cli.py (unit)

# ---- from test_cli9.py ----


import pytest
from commands import CLI


def test_cli_import():
    assert CLI is not None


def test_cli_callable(monkeypatch):
    cli = CLI(default_answer="y")
    # Replace get_y_n to avoid interactive input
    monkeypatch.setattr(CLI, "get_y_n", lambda question, default=None: True)
    assert cli("question?")


def test_cli_get_y_n_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert CLI.get_y_n("q?", default="y")




def test_cli_get_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")
    assert CLI.get_int("number?") == 42


def test_cli_get_ints(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1 2 3")
    assert CLI.get_ints("numbers?", 3) == [1, 2, 3]


def test_cli_wait_update():
    out = CLI.wait_update(verbose=False)
    assert out in {"|", "/", "-", "\\"}


def test_cli_progressbar():
    bar = CLI.progressbar(5, 10, done_repr="5", total_repr="10")
    assert "5" in bar and "10" in bar


def test_cli_progressbar_reverse_and_overflow(monkeypatch):
    monkeypatch.setattr(CLI, "wait_update_pos", 0)
    bar = CLI.progressbar(15, 10, reverse=True)
    assert isinstance(bar, str)




# ---- from test_cli_comprehensive.py ----


import pytest
from unittest.mock import patch, Mock
from commands.cli import CLI


class TestCLIWaitUpdate:
    """Tests for CLI.wait_update method"""

    def test_wait_update_position_0(self):
        """Test wait_update at position 0 to cover lines 122-123"""
        CLI.wait_update_pos = 0
        result = CLI.wait_update(verbose=False)
        assert result == "|"
        assert CLI.wait_update_pos == 1

    def test_wait_update_position_1(self):
        """Test wait_update at position 1 to cover lines 124-125"""
        CLI.wait_update_pos = 1
        result = CLI.wait_update(verbose=False)
        assert result == "/"
        assert CLI.wait_update_pos == 2

    def test_wait_update_position_2(self):
        """Test wait_update at position 2 to cover lines 126-127"""
        CLI.wait_update_pos = 2
        result = CLI.wait_update(verbose=False)
        assert result == "-"
        assert CLI.wait_update_pos == 3

    def test_wait_update_position_3(self):
        """Test wait_update at position 3 to cover lines 128-130"""
        CLI.wait_update_pos = 3
        result = CLI.wait_update(verbose=False)
        # Should return backslash and reset position
        assert result == "\\"
        assert CLI.wait_update_pos == 0

    def test_wait_update_verbose_true(self):
        """Test wait_update with verbose=True to cover lines 133-134"""
        CLI.wait_update_pos = 0

        with patch('commands.print.Print') as mock_print:
            result = CLI.wait_update(verbose=True)
            assert result == "|"
            # Print.rewrite should be called
            assert mock_print.rewrite.called

    def test_wait_update_full_cycle(self):
        """Test full cycle of wait_update"""
        CLI.wait_update_pos = 0

        results = []
        for _ in range(5):
            results.append(CLI.wait_update(verbose=False))

        # Should cycle through: |, /, -, \, | (back to start)
        assert results == ["|", "/", "-", "\\", "|"]


class TestCLIGetIntegerAliases:
    """Tests for CLI integer getter aliases"""

    @patch('builtins.input')
    def test_get_integer_alias(self, mock_input):
        """Test get_integer alias to cover line 105"""
        mock_input.return_value = "42"
        result = CLI.get_integer("Enter number: ")
        assert result == 42

    @patch('builtins.input')
    def test_get_integers_alias(self, mock_input):
        """Test get_integers alias to cover line 109"""
        mock_input.return_value = "10 20 30"
        result = CLI.get_integers("Enter numbers: ", count_of_ints=3)
        assert result == [10, 20, 30]


class TestCLIGetDate:
    """Tests for CLI.get_date method error handling"""





    @patch('builtins.input')
    def test_get_date_empty_input_no_always_return(self, mock_input):
        """Test get_date with empty input and always_return_date=False"""
        mock_input.return_value = ""

        result = CLI.get_date("test_date", always_return_date=False)

        # Should return None when empty and not required
        assert result is None


class TestCLIProgressbarEdgeCases:
    """Additional tests for progressbar edge cases"""

    def test_progressbar_reverse_overflow(self):
        """Test progressbar with reverse=True and overflow"""
        result = CLI.progressbar(done=150, total=100, reverse=True)
        # Should handle overflow gracefully
        assert isinstance(result, str)

    def test_progressbar_zero_total(self):
        """Test progressbar with zero total"""
        # Should not crash with zero division
        result = CLI.progressbar(done=10, total=0)
        assert isinstance(result, str)


class TestCLIGetIntsEdgeCases:
    """Additional tests for get_ints edge cases"""

    @patch('builtins.input')
    def test_get_ints_multiline_input(self, mock_input):
        """Test get_ints with multiline input"""
        # get_ints asks once and expects space-separated values
        mock_input.return_value = "10 20 30"

        result = CLI.get_ints("Numbers: ", count_of_ints=3)
        assert len(result) == 3
        assert result == [10, 20, 30]

    @patch('builtins.input')
    def test_get_ints_with_spaces(self, mock_input):
        """Test get_ints with various spacing"""
        mock_input.return_value = "  10   20    30  "

        result = CLI.get_ints("Numbers: ", count_of_ints=3)
        assert result == [10, 20, 30]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_cli_get_y_n_edges.py ----


import pytest

from commands.cli import CLI
from commands.os import OS


def test_cli_get_y_n_get_key_returns_none_uses_default(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")

    assert CLI.get_y_n("Q", default="y") is True
    out = capsys.readouterr().out
    assert "Q (y/n)?" in out




def test_cli_get_y_n_translate_mismatch_prints(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "x")
    monkeypatch.setattr("commands.keyboard.Keyboard.translate_string", staticmethod(lambda s: "y"))

    assert CLI.get_y_n("Q") is True
    out = capsys.readouterr().out
    assert " > y" in out


def test_cli_get_y_n_reads_windows_key(monkeypatch):
    import sys
    import types

    keys = iter(["\xe0", "y"])
    msvcrt = types.ModuleType("msvcrt")
    msvcrt.getwch = lambda: next(keys)
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setitem(sys.modules, "msvcrt", msvcrt)
    monkeypatch.setattr(sys, "stdin", types.SimpleNamespace(isatty=lambda: True))

    assert CLI.get_y_n("Q") is True


def test_cli_get_y_n_reads_unix_key(monkeypatch):
    import sys
    import types

    restored = []
    termios = types.ModuleType("termios")
    termios.TCSADRAIN = 1
    termios.tcgetattr = lambda _fd: "old"
    termios.tcsetattr = lambda *args: restored.append(args)
    tty = types.ModuleType("tty")
    tty.setraw = lambda _fd: None
    stdin = types.SimpleNamespace(isatty=lambda: True, fileno=lambda: 42, read=lambda _count: "n")
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setitem(sys.modules, "termios", termios)
    monkeypatch.setitem(sys.modules, "tty", tty)
    monkeypatch.setattr(sys, "stdin", stdin)

    assert CLI.get_y_n("Q") is False
    assert restored == [(42, 1, "old")]


def test_cli_progressbar_windows_branch(monkeypatch):
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr("commands.console.Console.width", classmethod(lambda cls: 20))
    bar = CLI.progressbar(1, 2)
    assert isinstance(bar, str)


# ---- from test_cli_input_flow.py ----


import datetime

import pytest

from commands.cli import CLI


def test_cli_multiline_input(monkeypatch):
    inputs = iter(["line1", "line2"])

    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)
    result = CLI.multiline_input("prompt?")
    assert result == "line1\nline2"


def test_cli_get_date_optional(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    class FakeTime:
        @staticmethod
        def datetime():
            return datetime.datetime(2024, 1, 1, 12, 0, 0)

    monkeypatch.setattr("commands.time.Time", FakeTime)
    assert CLI.get_date("test", always_return_date=False) is None


def test_cli_get_date_retry_and_success(monkeypatch):
    responses = iter(["3213", "0102"])

    def fake_input(_):
        return next(responses)

    class FakeTime:
        @staticmethod
        def datetime():
            return datetime.datetime(2024, 1, 1, 12, 0, 0)

    monkeypatch.setattr("commands.time.Time", FakeTime)
    monkeypatch.setattr("builtins.input", fake_input)
    result = CLI.get_date("event", always_return_date=True)
    assert result == datetime.datetime(2024, 2, 1, 0, 0)
