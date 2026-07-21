# Consolidated tests for commands/dir.py (integration_negative)

# ---- from test_dir_integration_negative.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.dir import Dir
import shutil
from unittest.mock import patch, Mock, MagicMock
import pathlib
import stat

def test_dir_list_of_entries_nonexistent():
    """Should raise FileNotFoundError for nonexistent directory"""
    with pytest.raises(FileNotFoundError):
        Dir.list_of_entries("/nonexistent/directory")

def test_dir_list_of_files_nonexistent():
    """Should raise FileNotFoundError for nonexistent directory"""
    with pytest.raises(FileNotFoundError):
        Dir.list_of_files("/nonexistent/directory")

def test_dir_list_of_dirs_nonexistent():
    """Should raise FileNotFoundError for nonexistent directory"""
    with pytest.raises(FileNotFoundError):
        Dir.list_of_dirs("/nonexistent/directory")

def test_dir_number_of_files_nonexistent():
    """Should raise FileNotFoundError for nonexistent directory"""
    with pytest.raises(FileNotFoundError):
        Dir.number_of_files("/nonexistent/directory", verbose=False)

class TestDirCoverage:
    """Tests to improve coverage for dir9.py"""
    def test_get_size_nonexistent(self):
        """Test Dir.get_size with nonexistent directory (lines 255-256)"""
        with pytest.raises(FileNotFoundError):
            Dir.get_size("/nonexistent/directory")

def test_dir_number_of_files_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        Dir.number_of_files(tmp_path / "missing")

def test_dir_delete_skip_permission(tmp_path, monkeypatch):
    sub = tmp_path / "sub"
    sub.mkdir()
    file_path = sub / "file.txt"
    file_path.write_text("data")

    def fake_remove(path):
        raise PermissionError("deny")

    monkeypatch.setattr(os, "remove", fake_remove)
    # skip permission errors quietly
    with pytest.raises(OSError):
        Dir.delete(sub, skip_permission_error=True, quiet_permission_error=True, remove_readonly=False)
