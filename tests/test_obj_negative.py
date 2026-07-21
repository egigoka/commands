# Consolidated tests for commands/obj.py (negative)

# ---- from test_obj_negative.py ----

# Placeholder for future tests.
import pytest
from commands.obj import Obj

def test_cast_to_multiple_types_all_fail():
    class CustomType:
        def __init__(self, val):
            raise ValueError("Cannot convert")

    result = Obj.cast_to("test", [CustomType])
    assert result == "test"

def test_cast_to_returns_original_on_all_failures():
    original = {"key": "value"}
    result = Obj.cast_to(original, [int, float])
    assert result == original

def test_cast_to_empty_type_list():
    """Should return original value when no types provided"""
    original = "test"
    result = Obj.cast_to(original, [])
    assert result == original

def test_cast_to_invalid_string_to_int():
    """Should return original when string can't be converted to int"""
    result = Obj.cast_to("not_a_number", [int])
    assert result == "not_a_number"

def test_cast_to_invalid_string_to_float():
    """Should return original when string can't be converted to float"""
    result = Obj.cast_to("abc", [float])
    assert result == "abc"

class TestObjInstance:
    """Tests for Obj instance methods"""
    def test_obj_instance_cast_fails_returns_original(self):
        """Test instance cast returns original when all fail"""
        o = Obj({"key": "value"})
        result = o.cast([int, float])
        assert result == {"key": "value"}
    def test_obj_instance_cast_empty_list(self):
        """Test instance cast with empty type list"""
        o = Obj("test")
        result = o.cast([])
        assert result == "test"
