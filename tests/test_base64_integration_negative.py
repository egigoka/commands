# Consolidated tests for commands/base64.py (integration_negative)

# Placeholder for future tests.
import pytest
from commands.base64 import Base64

def test_to_file_invalid_path():
    """Should raise exception when path is invalid"""
    with pytest.raises(Exception):
        Base64("SGVsbG8=", filename="/invalid/nonexistent/path/file.txt").to_file()

def test_from_file_nonexistent():
    """Should raise exception when file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        Base64(filename="/nonexistent/file.txt").from_file()
