# Consolidated tests for commands/dir.py (unit)

# ---- from test_dir9.py ----


import pytest
import tempfile
import os
from commands.dir import Dir




















# Negative tests








# Coverage improvement tests
class TestDirCoverage:
    """Tests to improve coverage for dir9.py"""




















# ---- from test_dir_comprehensive.py ----


import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, Mock, MagicMock
from commands.dir import Dir


class TestDirInstanceComprehensive:
    """Comprehensive tests for Dir instance methods"""

    def test_instance_string_property(self):
        """Test string property to cover line 34"""
        d = Dir("/some/path")
        assert d.string == d.path








class TestDirDeletePermissionHandling:
    """Tests for permission error handling in delete method"""

    @patch('os.remove')
    @patch('os.chmod')
    @patch('os.walk')
    def test_delete_permission_error_with_skip(self, mock_walk, mock_chmod, mock_remove):
        """Test delete with skip_permission_error=True to cover lines 149-161"""
        mock_walk.return_value = [('/test', [], ['file.txt'])]
        # First call raises PermissionError, second call after chmod also raises
        mock_remove.side_effect = [PermissionError("Access denied"), PermissionError("Still denied")]

        with pytest.raises(PermissionError):
            # This should try chmod and then fail again
            Dir.delete('/test', remove_readonly=True, skip_permission_error=False)

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.chmod')
    @patch('os.walk')
    @patch('builtins.print')
    def test_delete_permission_error_skip_quiet(self, mock_print, mock_walk, mock_chmod, mock_remove, mock_rmdir):
        """Test delete with skip_permission_error=True and quiet to cover lines 156-161"""
        mock_walk.return_value = [('/test', [], ['file.txt'])]
        # Raise PermissionError twice (once on remove, once after chmod)
        mock_remove.side_effect = [PermissionError("Access denied"), PermissionError("Still denied")]
        mock_chmod.return_value = None
        mock_rmdir.return_value = None

        # Should not raise, should print error
        Dir.delete('/test', remove_readonly=True, skip_permission_error=True, quiet_permission_error=False)

        # Check that error was printed
        assert mock_print.called

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.walk')
    def test_delete_without_remove_readonly(self, mock_walk, mock_remove, mock_rmdir):
        """Test delete without remove_readonly to cover line 164"""
        mock_walk.return_value = [('/test', [], ['file.txt'])]
        mock_remove.return_value = None
        mock_rmdir.return_value = None

        Dir.delete('/test', remove_readonly=False, skip_permission_error=False)

        assert mock_remove.called

    @patch('os.rmdir')
    @patch('os.remove')
    @patch('os.walk')
    @patch('builtins.print')
    def test_delete_without_readonly_with_skip_permission(self, mock_print, mock_walk, mock_remove, mock_rmdir):
        """Test delete without remove_readonly but with skip_permission_error to cover line 170"""
        mock_walk.return_value = [('/test', [], ['file.txt'])]
        mock_remove.side_effect = PermissionError("Access denied")
        mock_rmdir.return_value = None

        # Should not raise, should print error
        Dir.delete('/test', remove_readonly=False, skip_permission_error=True, quiet_permission_error=False)

        # Check that error was printed
        assert mock_print.called


class TestDirCopySymlinksAndErrors:
    """Tests for symlinks and error handling in copy method"""


    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_copy_permission_error_with_skip(self, mock_print, mock_isdir, mock_exists,
                                            mock_listdir, mock_copy2):
        """Test copy with PermissionError handling to cover lines 254-258"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['file.txt']
        mock_isdir.return_value = False
        mock_copy2.side_effect = PermissionError("Access denied")

        # Should not raise with skip_permission_error=True
        Dir.copy('/src', '/dst', skip_permission_error=True, quiet_permission_error=False)

        # Check that error was printed
        assert mock_print.called


    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_copy_file_not_found_error(self, mock_print, mock_isdir, mock_exists,
                                      mock_listdir, mock_copy2):
        """Test copy with FileNotFoundError handling to cover lines 259-263"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['file.txt']
        mock_isdir.return_value = False
        mock_copy2.side_effect = FileNotFoundError("File not found")

        # Should not raise with skip_file_not_found_error=True
        Dir.copy('/src', '/dst', skip_file_not_found_error=True, quiet_file_not_found_error=False)

        # Check that error was printed
        assert mock_print.called

    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_copy_os_error(self, mock_print, mock_isdir, mock_exists,
                          mock_listdir, mock_copy2):
        """Test copy with OSError handling to cover lines 264-268"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['file.txt']
        mock_isdir.return_value = False
        mock_copy2.side_effect = OSError("OS error")

        # Should not raise with skip_os_error=True
        Dir.copy('/src', '/dst', skip_os_error=True, quiet_os_error=False)

        # Check that error was printed
        assert mock_print.called





if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_dir_extra.py ----


import os
import pathlib
import stat

import pytest

from commands.dir import Dir
