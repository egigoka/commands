# Consolidated tests for commands/os.py (integration_negative)

# ---- from test_os_integration_negative.py ----

# Placeholder for future tests.
import pytest
import sys
from commands.os import OS
import os
import tempfile
from unittest.mock import patch, Mock
import types

class TestOSWalk:
    """Tests for OS.walk method"""
    def test_walk_nonexistent_directory(self):
        """Test walk with non-existent directory to cover line 186"""
        with pytest.raises(FileNotFoundError, match="doesn't exist"):
            list(OS.walk("/nonexistent/path/that/doesnt/exist"))
