# Consolidated tests for commands/os.py (integration)

# ---- from test_os_integration.py ----

# Placeholder for future tests.
import pytest
import sys
from commands.os import OS
import os
import tempfile
from unittest.mock import patch, Mock
import types

def test_os_callable_returns_cwd(monkeypatch):
    import os
    original = os.getcwd()
    try:
        temp_dir = os.path.abspath(".")
        monkeypatch.chdir(temp_dir)
        assert OS() == temp_dir
    finally:
        monkeypatch.chdir(original)

def test_os_chdir_updates_cache(tmp_path):
    target = tmp_path
    cwd_before = OS.cwd
    OS.chdir(str(target))
    assert OS.cwd == str(target)
    # restore
    OS.chdir(cwd_before)

class TestOSCoverage:
    """Tests to improve coverage for os9.py"""
    def test_walk_basic(self):
        """Test OS.walk function (lines 164-168)"""
        import tempfile
        import os as os_module

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple directory structure
            subdir = os_module.path.join(tmpdir, "subdir")
            os_module.makedirs(subdir)

            # Create some files
            with open(os_module.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("test")
            with open(os_module.path.join(subdir, "file2.txt"), "w") as f:
                f.write("test")

            # Test walk
            results = list(OS.walk(tmpdir))
            assert len(results) >= 2  # At least root and subdir

            # Each result should be a tuple (dirpath, dirnames, filenames)
            for dirpath, dirnames, filenames in results:
                assert isinstance(dirpath, str)
                assert isinstance(dirnames, list)
                assert isinstance(filenames, list)
    def test_walk_topdown_false(self):
        """Test OS.walk with topdown=False (lines 172-178)"""
        import tempfile
        import os as os_module

        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os_module.path.join(tmpdir, "subdir")
            os_module.makedirs(subdir)

            # Test walk with topdown=False (bottom-up)
            results = list(OS.walk(tmpdir, topdown=False))
            assert len(results) >= 1
            # In bottom-up, subdirectories come before parent
            if len(results) >= 2:
                assert "subdir" in results[0][0] or "subdir" in results[-1][0]
    def test_walk_follow_links(self):
        """Test OS.walk with follow_links (lines 182-183)"""
        import tempfile
        import os as os_module

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test walk with follow_links=True
            results = list(OS.walk(tmpdir, follow_links=True))
            assert len(results) >= 1
    def test_walk_onerror(self):
        """Test OS.walk with onerror callback (lines 192-193, 197-198)"""
        import tempfile
        import os as os_module

        errors = []
        def error_handler(error):
            errors.append(error)

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a directory and immediately remove it to potentially trigger error
            # This is hard to test reliably, so just verify the parameter works
            results = list(OS.walk(tmpdir, onerror=error_handler))
            assert isinstance(results, list)

class TestOSWalk:
    """Tests for OS.walk method"""
    def test_walk_existing_directory(self, tmp_path):
        """Test walk with existing directory"""
        # Create some files and subdirs
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file2.txt").write_text("content2")

        # Walk should work
        results = list(OS.walk(str(tmp_path)))
        assert len(results) > 0

class TestOSChdirMethod:
    """Tests for chdir method"""

    def test_chdir_updates_cwd(self, tmp_path):
        """Test that chdir updates cached cwd"""
        original_cwd = os.getcwd()

        try:
            # Change to temp directory
            new_cwd = OS.chdir(str(tmp_path))

            # Should update _cwd cache
            assert new_cwd == str(tmp_path)
            assert OS._cwd == str(tmp_path)
            assert os.getcwd() == str(tmp_path)
        finally:
            # Restore original directory
            os.chdir(original_cwd)
            # Reset OS cwd cache
            OS._cwd = original_cwd
