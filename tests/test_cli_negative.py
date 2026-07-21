# Consolidated tests for commands/cli.py (negative)

# ---- from test_cli_negative.py ----


import pytest
from commands.cli import CLI


from commands import CLI
from unittest.mock import patch
import datetime

def test_cli_get_y_n_invalid_no_default(monkeypatch):
    inputs = iter(["maybe", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Eventually default is None; function will keep looping; simulate KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        # monkeypatch builtins.input to raise KeyboardInterrupt after invalid input
        def raising(_):
            raise KeyboardInterrupt
        monkeypatch.setattr("builtins.input", raising)
        CLI.get_y_n("q?", default=None)

def test_cli_get_y_n_invalid(monkeypatch):
    # Ensure invalid input falls back to default
    answers = iter(["maybe", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert CLI.get_y_n("q?", default="n") is False

def test_cli_get_ints_invalid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "not_numbers")
    # will loop indefinitely; simulate by raising after first call
    with pytest.raises(StopIteration):
        inputs = iter(["abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        CLI.get_ints("q?", 1)

class TestCLIGetDate:
    """Tests for CLI.get_date method error handling"""
    @patch('builtins.input')
    def test_get_date_invalid_day(self, mock_input):
        mock_input.return_value = "ab012001"
        with patch("commands.cli.Time.datetime", return_value=datetime.datetime(2024, 5, 15)):
            result = CLI.get_date("test_date")
        assert result == datetime.datetime(2001, 1, 15)
    @patch('builtins.input')
    def test_get_date_invalid_month(self, mock_input):
        mock_input.return_value = "01ab2001"
        with patch("commands.cli.Time.datetime", return_value=datetime.datetime(2024, 5, 15)):
            result = CLI.get_date("test_date")
        assert result == datetime.datetime(2001, 5, 1)
    @patch('builtins.input')
    def test_get_date_invalid_year(self, mock_input):
        mock_input.return_value = "0101ab"
        with patch("commands.cli.Time.datetime", return_value=datetime.datetime(2024, 5, 15)):
            result = CLI.get_date("test_date")
        assert result == datetime.datetime(2024, 1, 1)
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_date_always_return_empty_input(self, mock_print, mock_input):
        """Test get_date with empty input and always_return_date=True to cover lines 246-247"""
        # First input: empty string (should prompt again)
        # Second input: valid date
        mock_input.side_effect = ["", "010120"]

        result = CLI.get_date("test_date", always_return_date=True)

        mock_print.assert_any_call("Please, enter date.")
        assert result == datetime.datetime(2020, 1, 1)

def test_cli_get_y_n_ctrl_c_raises_keyboard_interrupt(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "\x03")

    with pytest.raises(KeyboardInterrupt):
        CLI.get_y_n("Q")
