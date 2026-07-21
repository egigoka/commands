# Consolidated tests for commands/print.py (negative)

# ---- from test_print_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
"""Tests for missing coverage in print.py module"""
import pytest
from commands import Print


class TestPrintMissingCoverage:
    """Tests to cover missing lines in print.py"""

    def test_colored_verbose_mode(self, capsys):
        """Test Print.colored with verbose=True (line 148)"""
        Print.colored("test message", "green", verbose=True)

        captured = capsys.readouterr()
        assert "test message" in captured.out
