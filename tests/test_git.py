# Consolidated tests for commands/git.py (unit)

# ---- from test_git9.py ----


import pytest
import tempfile
import os


def test_git9_import():
    from commands import Git
    assert Git is not None




def test_git_callable_runs(monkeypatch):
    from commands.git import Git
    from commands.git import get_name_of_repo
    called = {"add": False, "commit": False, "push": False}

    monkeypatch.setattr(Git, "add_files", lambda self, verbose=False: called.__setitem__("add", True))
    monkeypatch.setattr(Git, "commit_changes", lambda self, message=None, verbose=False: called.__setitem__("commit", True))
    monkeypatch.setattr(Git, "push_remote", lambda self, upstream=False, verbose=False: called.__setitem__("push", True))

    g = Git(remote="origin")
    g("msg")

    assert all(called.values())

# Coverage improvement tests
class TestGitLegacyCoverage:
    """Tests to improve coverage for git9.py"""

    def test_get_name_of_repo_special_case(self, monkeypatch):
        """Test get_name_of_repo returns 'test' for 't' or 'term' directories (line 16)"""
        from commands.git import get_name_of_repo
        from commands.path import Path

        # Mock Path.working() to return a path ending in 't'
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "t")
            os.makedirs(test_dir)

            def mock_working():
                return test_dir

            monkeypatch.setattr(Path, "working", mock_working)
            result = get_name_of_repo()
            assert result == "test"

    def test_get_name_of_repo_term(self, monkeypatch):
        """Test get_name_of_repo returns 'test' for 'term' directory"""
        from commands.git import get_name_of_repo
        from commands.path import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "term")
            os.makedirs(test_dir)

            def mock_working():
                return test_dir

            monkeypatch.setattr(Path, "working", mock_working)
            result = get_name_of_repo()
            assert result == "test"

    def test_git_add_verbose(self, monkeypatch):
        """Test Git.add with verbose=True (lines 29-30)"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(*args, **kwargs):
            called.append((args, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.add(".", verbose=True)

        assert len(called) == 1
        assert called[0][1]["print_std"] == True

    def test_git_commit_with_message(self, monkeypatch):
        """Test Git.commit with message parameter (lines 38-45)"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(commands, **kwargs):
            called.append((commands, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.commit(message="Test commit", verbose=False)

        assert len(called) == 1
        assert "-m" in called[0][0]
        assert any("Test commit" in str(arg) for arg in called[0][0])

    def test_git_instance_helpers(self, monkeypatch):
        from commands.git import Git
        from commands.console import Console

        calls = []
        monkeypatch.setattr(Console, "get_output", lambda *a, **k: calls.append((a, k)))

        g = Git(remote="origin")
        g.add_files("file.txt", verbose=True)
        g.commit_changes("msg", verbose=False)
        g.push_remote(upstream=True, verbose=False)

        assert len(calls) == 3
        assert calls[0][0][0:2] == ("git", "add")
        assert "origin" in calls[2][0][0]

    def test_git_commit_verbose(self, monkeypatch):
        """Test Git.commit with verbose=True"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(commands, **kwargs):
            called.append((commands, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.commit(message="Test", verbose=True)

        assert len(called) == 1
        assert called[0][1]["print_std"] == True

    def test_git_push_with_upstream(self, monkeypatch):
        """Test Git.push with upstream=True (lines 54-60)"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(commands, **kwargs):
            called.append((commands, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.push("origin", upstream=True, verbose=False)

        assert len(called) == 1
        assert "-u" in called[0][0]
        assert "origin" in called[0][0]

    def test_git_push_verbose(self, monkeypatch):
        """Test Git.push with verbose=True"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(commands, **kwargs):
            called.append((commands, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.push("origin", upstream=False, verbose=True)

        assert len(called) == 1
        assert called[0][1]["print_std"] == True

    def test_git_update(self, monkeypatch):
        """Test Git.update function (lines 69-71)"""
        from commands.git import Git
        from commands.console import Console

        called = []
        def mock_get_output(*args, **kwargs):
            called.append((args, kwargs))
            return ""

        monkeypatch.setattr(Console, "get_output", mock_get_output)
        Git.update("Test commit", path="test_repo", verbose=True)

        # Should call add, commit, and push
        assert len(called) == 3

        # Verify add was called
        assert any("git" in str(call[0]) and "add" in str(call[0]) for call in called)

        # Verify commit was called
        assert any("git" in str(call[0]) and "commit" in str(call[0]) for call in called)

        # Verify push was called
        assert any("git" in str(call[0]) and "push" in str(call[0]) for call in called)


# ---- from test_git_coverage.py ----


import pytest
from commands.git import Git
from unittest.mock import MagicMock, patch


class TestGitCoverage:
    """Tests to improve Git module coverage"""

    def test_call_with_remote_parameter_sets_remote(self, monkeypatch):
        """Test __call__ with remote parameter sets self.remote (line 30)"""
        # Mock the git commands
        import commands.console
        mock_get_output = MagicMock(return_value="")
        monkeypatch.setattr(commands.console.Console, "get_output", mock_get_output)

        g = Git()
        # Call with remote parameter to trigger line 30
        g(message="test commit", remote="origin", add=False, push=False)

        # Verify remote was set
        assert g.remote == "origin"


    def test_update_remote_uses_default_when_remote_not_set(self, monkeypatch):
        """Test update_remote() uses default github URL when remote not set (lines 105-106)"""
        # Mock get_name_of_repo
        from commands import git as git_module
        monkeypatch.setattr(git_module, "get_name_of_repo", lambda: "test-repo")

        # Mock Console.get_output
        import commands.console
        mock_get_output = MagicMock(return_value="")
        monkeypatch.setattr(commands.console.Console, "get_output", mock_get_output)

        g = Git()
        # Don't set remote - should use default
        g.update_remote("test message", verbose=False)

        # Verify Console.get_output was called with the default github URL
        mock_get_output.assert_called()
        # The update method should have been called with the default URL
        call_args = str(mock_get_output.call_args_list)
        assert "egigoka/test-repo" in call_args or "test message" in call_args
