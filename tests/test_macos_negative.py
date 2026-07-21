# Consolidated tests for commands/macos.py (negative)

# ---- from test_macos_negative.py ----

# Placeholder for future tests.
import os
import sys
import types
import tempfile
from commands import Dir, File, OS, Path
import pytest
from commands.macos import macOS

def test_macos_callable_requires_message():
    from commands.macos import macOS
    m = macOS()
    with pytest.raises(ValueError):
        m()
