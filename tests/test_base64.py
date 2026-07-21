# Consolidated tests for commands/base64.py (unit)

# ---- from test_base64_9.py ----

import pytest
import tempfile
import os
from commands.base64 import Base64


def test_from_bytes_to_bytes():
    original = b"Hello, World!"
    encoded = Base64(original).from_bytes()
    decoded = Base64(encoded).to_bytes()
    assert decoded == original


def test_from_bytes_string():
    data = b"Test data 123"
    result = Base64(data).from_bytes()
    assert isinstance(result, bytes)
    assert b"VGVzdCBkYXRhIDEyMw==" in result


def test_to_bytes_from_string():
    encoded_str = "SGVsbG8sIFdvcmxkIQ=="
    result = Base64(encoded_str).to_bytes()
    assert result == b"Hello, World!"


def test_to_bytes_from_bytes():
    encoded_bytes = b"SGVsbG8sIFdvcmxkIQ=="
    result = Base64(encoded_bytes).to_bytes()
    assert result == b"Hello, World!"


def test_base64_bytearray_paths():
    raw = bytearray(b"bytearray")
    b64 = Base64(raw)
    encoded = b64.from_bytes()
    assert isinstance(encoded, bytes)
    decoded = Base64(bytearray(encoded)).to_bytes()
    assert decoded == b"bytearray"




def test_round_trip_binary_data():
    original = bytes([i for i in range(256)])
    encoded = Base64(original).from_bytes()
    decoded = Base64(encoded).to_bytes()
    assert decoded == original


def test_unicode_data():
    original = "Привет, мир! 你好世界".encode('utf-8')
    encoded = Base64(original).from_bytes()
    decoded = Base64(encoded).to_bytes()
    assert decoded == original




# ---- from test_base64_instance.py ----

import base64
import tempfile
import os
import pytest
from commands.base64 import Base64


def test_base64_encode_decode_roundtrip():
    b = Base64(data="hello")
    encoded = b.from_bytes()
    assert isinstance(encoded, (bytes, bytearray))
    decoded = b.to_bytes()
    assert decoded == b"hello"
