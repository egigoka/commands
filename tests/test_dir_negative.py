# Consolidated tests for commands/dir.py (negative)

# ---- from test_dir_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
import tempfile
from commands.dir import Dir
import shutil
from unittest.mock import patch, Mock, MagicMock
import pathlib
import stat

"""Tests for missing coverage in dir.py module"""
import os
import pytest
from commands import Dir


class TestDirMissingCoverage:
    """Tests to cover missing lines in dir.py"""

    def test_copy_symlink_with_existing_destination(self, tmp_path):
        """Test copying symlinks when destination already exists (line 234)"""
        if os.name == 'nt':
            pytest.skip("Symlink test not reliable on Windows")

        src_dir = tmp_path / "src_symlink"
        dst_dir = tmp_path / "dst_symlink"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a file and a symlink to it
        target_file = src_dir / "target.txt"
        target_file.write_text("target content")

        symlink_path = src_dir / "link.txt"
        symlink_path.symlink_to(target_file)

        # Create a destination symlink that will be replaced
        dst_symlink = dst_dir / "link.txt"
        dst_symlink.symlink_to(target_file)

        # Copy with symlinks=True, should replace existing symlink
        Dir.copy(str(src_dir), str(dst_dir), symlinks=True)

        assert dst_symlink.is_symlink()
        assert dst_symlink.exists()

    def test_copy_file_not_found_error_raises(self, tmp_path, monkeypatch):
        """Test FileNotFoundError raises when skip_file_not_found_error=False (line 263)"""
        src_dir = tmp_path / "src_fnf"
        dst_dir = tmp_path / "dst_fnf"
        src_dir.mkdir()
        (src_dir / "file.txt").write_text("content")

        # Mock shutil.copy2 to raise FileNotFoundError
        import shutil
        original_copy2 = shutil.copy2

        def mock_copy2(src, dst):
            raise FileNotFoundError(f"File not found: {src}")

        monkeypatch.setattr(shutil, 'copy2', mock_copy2)

        # Should raise FileNotFoundError when skip_file_not_found_error=False
        with pytest.raises(FileNotFoundError, match="File not found"):
            Dir.copy(str(src_dir), str(dst_dir),
                    skip_file_not_found_error=False,
                    quiet_file_not_found_error=True)  # quiet but still raise

class TestDirCopySymlinksAndErrors:
    """Tests for symlinks and error handling in copy method"""
    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_copy_permission_error_no_skip(self, mock_isdir, mock_exists,
                                          mock_listdir, mock_copy2):
        """Test copy with PermissionError and skip=False to cover line 258"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['file.txt']
        mock_isdir.return_value = False
        mock_copy2.side_effect = PermissionError("Access denied")
        # Should raise with skip_permission_error=False
        with pytest.raises(PermissionError):
            Dir.copy('/src', '/dst', skip_permission_error=False)
    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_copy_os_error_no_skip(self, mock_isdir, mock_exists,
                                  mock_listdir, mock_copy2):
        """Test copy with OSError and skip=False"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['file.txt']
        mock_isdir.return_value = False
        mock_copy2.side_effect = OSError("OS error")

        # Should raise with skip_os_error=False
        with pytest.raises(OSError):
            Dir.copy('/src', '/dst', skip_os_error=False)

class TestDirNegativeCases:
    """Additional negative test cases"""

    def test_instance_create_no_path(self):
        """Test instance create without path set"""
        d = Dir()
        with pytest.raises(ValueError, match="Directory path is not set"):
            d.create()

    def test_instance_rename_no_path(self):
        """Test instance rename without path set"""
        d = Dir()
        with pytest.raises(ValueError, match="Directory path is not set"):
            d.rename("newname")

    def test_instance_move_no_path(self):
        """Test instance move without path set"""
        d = Dir()
        with pytest.raises(ValueError, match="Directory path is not set"):
            d.move("/some/path")

    def test_instance_delete_no_path(self):
        """Test instance delete without path set"""
        d = Dir()
        with pytest.raises(ValueError, match="Directory path is not set"):
            d.delete()

def test_dir_ensure_path_required():
    d = Dir()
    with pytest.raises(ValueError):
        d._ensure_path()
