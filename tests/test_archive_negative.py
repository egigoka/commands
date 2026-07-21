# Consolidated tests for commands/archive.py (negative)

# Placeholder for future tests.
import os
import tempfile
import shutil
import zipfile
import tarfile
import pytest
from commands.archive import Archive

def test_Archive_tar_gz_invalid_mode():
    """Test that tar.gz raises ValueError for invalid modes"""
    temp_dir = tempfile.mkdtemp()
    try:
        tar_path = os.path.join(temp_dir, 'archive.tar.gz')
        with pytest.raises(ValueError, match="mode must be 'r', 'w' or 'x'"):
            Archive(tar_path, archive_type=Archive.MODE_TARGZ, mode='a')._open()
    finally:
        shutil.rmtree(temp_dir)

class TestArchiveCoverage:
    """Tests to improve Archive module coverage"""
    def test_archive_ensure_raises_when_archive_file_not_set(self):
        """Test Archive._ensure_archive_file raises ValueError (line 63)"""
        c = Archive(archive_file=None)
        with pytest.raises(ValueError, match="archive_file must be set"):
            c._ensure_archive_file()
    def test_archive_open_unknown_type(self):
        """Test Archive._open raises for unknown archive_type."""
        arch = Archive("test.zip", archive_type=999)
        with pytest.raises(ValueError, match="unknown archive_type"):
            arch._open()
