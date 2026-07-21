# Consolidated tests for commands/random.py (negative)

# ---- from test_random_instance_error_paths.py ----


import pytest

from commands.random import Random




from commands import random as random_module

def test_random_instance_string_negative_length():
    r = Random(seed=1)
    with pytest.raises(ValueError):
        r.string(-5)


def test_random_instance_item_empty(monkeypatch):
    r = Random(seed=2)
    with pytest.raises(IndexError):
        r.item([])
    with pytest.raises(TypeError):
        r.item(123)


def test_random_class_boolean_and_shuffle_types():
    # boolean classmethod already covered for distribution, ensure return type
    assert isinstance(Random.boolean(), bool)
    with pytest.raises(TypeError):
        Random.shuffle(1)  # non-iterable

def test_random_string_negative_length():
    with pytest.raises(ValueError):
        Random.string(-1)

def test_random_string_non_int_length():
    with pytest.raises(TypeError):
        Random.string("five")

def test_random_item_empty():
    with pytest.raises(IndexError):
        Random.item([])

def test_random_item_invalid_type():
    with pytest.raises(TypeError):
        Random.item(123)

class TestRandomInstanceComprehensive:
    """Comprehensive tests for Random instance methods to maximize coverage"""
    def test_instance_string_negative_length(self):
        """Test instance string with negative length to cover line 30"""
        r = Random(seed=300)
        with pytest.raises(ValueError, match="length must be non-negative"):
            r.string(-1)

class TestNegativeCases:
    """Additional negative tests"""
    def test_classmethod_string_negative_length(self):
        """Test classmethod string with negative length"""
        with pytest.raises(ValueError, match="length must be non-negative"):
            Random.string(-5)
    def test_instance_item_empty_list(self):
        """Test instance item with empty list"""
        r = Random(seed=1300)
        with pytest.raises(IndexError):
            r.item([])
    def test_classmethod_item_empty_list(self):
        """Test classmethod item with empty list"""
        with pytest.raises(IndexError):
            Random.item([])

def test_random_class_string_negative():
    with pytest.raises(ValueError):
        Random.string(-1)

class TestRandomInstance:
    """Tests for Random instance methods"""
    def test_instance_string_negative_length(self):
        """Test Random instance string raises on negative length"""
        r = Random(seed=42)
        with pytest.raises(ValueError):
            r.string(-1)

def test_random_class_item_empty_raises():
    with pytest.raises(IndexError):
        Random.item([])

def test_random_class_shuffle_non_iterable():
    with pytest.raises(TypeError):
        Random.shuffle(123)
