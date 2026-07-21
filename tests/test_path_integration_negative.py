# Consolidated tests for commands/path.py (integration_negative)

# ---- from test_path_integration_negative.py ----

# Placeholder for future tests.
import pytest
import os
import tempfile
from commands.path import Path
import types
from commands.os import OS

class TestPathNegative:
    """Negative tests for Path module"""
    def test_set_working_nonexistent(self):
        """Should handle nonexistent directory"""
        original = os.getcwd()
        try:
            with pytest.raises(FileNotFoundError):
                Path.set_working("/this/path/does/not/exist/123456789", verbose=False)
        finally:
            os.chdir(original)
