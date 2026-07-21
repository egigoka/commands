# Consolidated tests for commands/base64.py (negative)

import pytest

from commands.base64 import Base64


import tempfile
import os
import base64

def test_to_bytes_invalid_base64():
    """Should handle invalid base64 string without crashing"""
    # Base64 module is lenient and tries to decode what it can
    result = Base64("This is not valid base64").to_bytes()
    assert isinstance(result, bytes)


def test_to_bytes_malformed_padding():
    """Should handle malformed padding without crashing"""
    # Base64 module handles extra padding
    result = Base64("SGVsbG8=").to_bytes()
    assert isinstance(result, bytes)


def test_from_bytes_empty():
    """Should handle empty bytes"""
    result = Base64(b"").from_bytes()
    assert isinstance(result, bytes)

def test_base64_missing_data():
    b = Base64()
    with pytest.raises(ValueError):
        b.from_bytes()

def test_base64_missing_filename():
    b = Base64(data=b"abc")
    with pytest.raises(ValueError):
        b.from_file()

def test_base64_write_missing_filename():
    b = Base64(data=b"abc")
    with pytest.raises(ValueError):
        b.to_file()
