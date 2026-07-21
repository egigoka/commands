# Consolidated tests for commands/git.py (negative)

# ---- from test_git_negative.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.git import Git
from unittest.mock import MagicMock, patch

def test_git_callable_requires_message():
    from commands.git import Git
    g = Git(remote="origin")
    with pytest.raises(ValueError):
        g()

class TestGitCoverage:
    """Tests to improve Git module coverage"""
    def test_push_remote_raises_when_remote_not_set(self):
        """Test push_remote() raises ValueError when remote not set (line 101)"""
        g = Git()
        # Don't set remote
        with pytest.raises(ValueError, match="Remote path is not set"):
            g.push_remote()
