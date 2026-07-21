# Consolidated tests for commands/bash.py (negative)

# ---- from test_bash_negative.py ----

# Placeholder for future tests.
import pytest
from commands.bash import Bash

class TestBashRun:
    """Tests for command execution."""
    def test_run_empty_command_raises(self):
        """Running without a command raises ValueError."""
        with pytest.raises(ValueError, match="No command to run"):
            Bash().run()
    def test_call_empty_command_raises(self):
        """Calling without a command raises ValueError."""
        with pytest.raises(ValueError, match="No command to run"):
            Bash()()
