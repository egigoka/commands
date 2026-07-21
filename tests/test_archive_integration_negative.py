# Consolidated tests for commands/archive.py (integration_negative)

# Placeholder for future tests.
import os
import tempfile
import shutil
import zipfile
import tarfile
import pytest
from commands.archive import Archive

def test_Archive_file_nonexistent():
    """Test that Archive.file raises IOError for non-existent input file"""
    temp_dir = tempfile.mkdtemp()
    try:
        nonexistent_file = os.path.join(temp_dir, 'nonexistent.txt')
        zip_path = os.path.join(temp_dir, 'archive.zip')

        with pytest.raises(IOError, match="is not file"):
            Archive(zip_path).file(nonexistent_file)
    finally:
        shutil.rmtree(temp_dir)

def test_Archive_dir_nonexistent():
    """Test that Archive.dir raises IOError for non-existent input directory"""
    temp_dir = tempfile.mkdtemp()
    try:
        nonexistent_dir = os.path.join(temp_dir, 'nonexistent_dir')
        zip_path = os.path.join(temp_dir, 'archive.zip')

        with pytest.raises(IOError, match="is not dir"):
            Archive(zip_path).dir(nonexistent_dir)
    finally:
        shutil.rmtree(temp_dir)
