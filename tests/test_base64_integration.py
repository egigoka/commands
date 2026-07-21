# Consolidated tests for commands/base64.py (integration)

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.base64 import Base64
import base64

def test_to_file_and_from_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.b64")
        encoded_str = "SGVsbG8sIFdvcmxkIQ=="

        Base64(encoded_str, filename=filename).to_file()
        assert os.path.exists(filename)

        result = Base64(filename=filename).from_file()
        assert b"SGVsbG8sIFdvcmxkIQ==" in result

def test_base64_instance_shortcut():
    b64 = Base64(b"hi")
    encoded = b64.from_bytes()
    assert Base64(encoded).to_bytes() == b"hi"
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = os.path.join(tmpdir, "out.b64")
        b64.filename = dest
        b64.to_file()
        loaded = b64.from_file()
        assert loaded == encoded

def test_base64_write_read(tmp_path):
    data = base64.b64encode(b"data")
    path = tmp_path / "out.b64"
    b = Base64(data=data, filename=str(path))
    b.to_file()
    assert path.exists()
    b2 = Base64(filename=str(path))
    out = b2.from_file()
    assert out.strip() == data
