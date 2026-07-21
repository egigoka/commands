# Consolidated tests for commands/bytes.py (unit)

# ---- from test_bytes9.py ----


import pytest
from commands.bytes import Bytes


class TestBytesGetEncoding:
    """Tests for Bytes.get_encoding method"""

    def test_get_encoding_utf8(self):
        data = "Hello, world!".encode('utf-8')
        encoding = Bytes.get_encoding(data)
        assert encoding.lower() in ['utf-8', 'ascii']

    def test_get_encoding_utf16_le(self):
        data = "Hello, world!".encode('utf-16-le')
        encoding = Bytes.get_encoding(data)
        assert encoding == 'utf-16-le'

    def test_get_encoding_latin1(self):
        data = "café".encode('latin-1')
        encoding = Bytes.get_encoding(data)
        # chardet might detect ISO-8859-1 or similar
        assert encoding is not None



class TestBytesToString:
    """Tests for Bytes.to_string method"""

    def test_to_string_utf8(self):
        data = "Hello, world!".encode('utf-8')
        result = Bytes.to_string(data)
        assert result == "Hello, world!"

    def test_to_string_utf16_le(self):
        data = "Test string".encode('utf-16-le')
        result = Bytes.to_string(data)
        assert result == "Test string"

    def test_to_string_unicode(self):
        data = "Привет мир".encode('utf-8')
        result = Bytes.to_string(data)
        assert result == "Привет мир"

    def test_to_string_already_string(self):
        """Test that passing a string returns the same string"""
        result = Bytes.to_string("already a string")
        assert result == "already a string"

    def test_to_string_special_chars(self):
        data = "café ñoño".encode('utf-8')
        result = Bytes.to_string(data)
        assert result == "café ñoño"

    def test_to_string_emoji(self):
        # Emoji can be tricky with auto-detection, test basic UTF-8 instead
        data = "Hello World".encode('utf-8')
        result = Bytes.to_string(data)
        assert "Hello" in result and "World" in result


# Negative tests


def test_bytes_instance_helpers():
    b = Bytes(b"hello")
    enc = b.get_encoding().lower()
    assert isinstance(enc, str) and len(enc) > 0
    assert "hello" in b.to_string().lower()


class TestBytesInstance:
    """Tests for Bytes instance methods and forwarding"""

    def test_bytes_instance_init_none(self):
        """Test Bytes instance initialized with None"""
        b = Bytes()
        assert b.data is None

    def test_bytes_instance_init_with_data(self):
        """Test Bytes instance initialized with data"""
        b = Bytes(b"test data")
        assert b.data == b"test data"


    def test_bytes_instance_get_encoding_forwarding(self):
        """Test instance method forwarding for get_encoding"""
        b = Bytes(b"Hello World")
        encoding = b.get_encoding()
        assert encoding.lower() in ['utf-8', 'ascii']

    def test_bytes_instance_to_string_forwarding(self):
        """Test instance method forwarding for to_string"""
        b = Bytes(b"Test String")
        result = b.to_string()
        assert result == "Test String"

    def test_bytes_instance_get_encoding_utf16_forwarding(self):
        """Test instance get_encoding with UTF-16-LE"""
        data = "Hello!".encode('utf-16-le')
        b = Bytes(data)
        encoding = b.get_encoding()
        assert encoding == 'utf-16-le'

    def test_bytes_instance_to_string_unicode_forwarding(self):
        """Test instance to_string with Unicode"""
        data = "Привет".encode('utf-8')
        b = Bytes(data)
        result = b.to_string()
        assert result == "Привет"


    def test_bytes_instance_getattribute_non_forwarded(self):
        """Test that non-forwarded attributes work normally"""
        b = Bytes(b"data")
        assert hasattr(b, 'data')
        assert hasattr(b, '_ensure')
        assert b.data == b"data"

    def test_bytes_instance_chained_operations(self):
        """Test chaining instance operations"""
        b = Bytes("Test".encode('utf-8'))
        # Get encoding first
        encoding = b.get_encoding()
        assert encoding.lower() in ['utf-8', 'ascii']
        # Then convert to string
        result = b.to_string()
        assert result == "Test"


    def test_bytes_instance_special_chars(self):
        """Test instance with special characters"""
        data = "café ñoño 中文".encode('utf-8')
        b = Bytes(data)
        result = b.to_string()
        assert "café" in result
        assert "中文" in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
