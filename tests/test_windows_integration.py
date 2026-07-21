# Consolidated tests for commands/windows.py (integration)

# ---- from test_windows_integration.py ----

# Placeholder for future tests.
import os
import sys
import types
import pytest
from commands.windows import Windows
from commands import Windows

def test_file_hide_verbose_prints(monkeypatch, tmp_path, capsys):
    from commands.file import File

    target = tmp_path / "hidden.txt"
    target.write_text("data")
    File.hide(target, verbose=True)
    captured = capsys.readouterr()
    assert "is hidden now" in captured.out.lower()

class TestWindowsMissingCoverage:
    """Tests to cover missing lines in windows.py"""
    def test_dump_auditpol_with_fast_name(self, monkeypatch, tmp_path):
        """Test dump_auditpol with fast_name parameter (line 244)"""
        import commands.console

        def mock_get_output(command):
            return "audit policy output"

        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))

        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        Windows.dump_auditpol(fast_name="custom")

        # Check that file was created with fast_name in it
        files = list(tmp_path.glob("auditpol_*--custom.txt"))
        assert len(files) == 1
    def test_dump_auditpol_verbose(self, monkeypatch, tmp_path, capsys):
        """Test dump_auditpol with verbose=True (line 253)"""
        import commands.console

        def mock_get_output(command):
            return "audit policy output"

        monkeypatch.setattr(commands.console.Console, 'get_output', staticmethod(mock_get_output))
        monkeypatch.chdir(tmp_path)

        Windows.dump_auditpol(filename="test_audit.txt", verbose=True)

        captured = capsys.readouterr()
        assert "Audit politics saved to" in captured.out
        assert "test_audit.txt" in captured.out
