# Consolidated tests for commands/list.py (negative)

# ---- from test_list_negative.py ----

# Placeholder for future tests.
import pytest
from commands.list import List

class TestListFlatterize:
    """Tests for List.flatterize method"""
    def test_flatterize_invalid_type(self):
        with pytest.raises(TypeError, match="can't be flatterized"):
            List.flatterize("not a list")

class TestListNegative:
    """Negative tests for List module"""
    def test_apply_lambda_exception(self):
        """Should handle lambda that raises exception"""
        with pytest.raises(Exception):
            List.apply_lambda_to_all_elements([1, 2, 3], lambda x: x.nonexistent_method())
    def test_sort_by_missing_key(self):
        """Raise when a requested sort key is missing."""
        data = [{"name": "Alice"}, {"name": "Bob", "age": 30}]
        with pytest.raises(KeyError):
            List.sort_by(data, "age")
    def test_enum_by_invalid_key(self):
        """Raise when a requested enumeration key is missing."""
        data = [{"id": 1}, {"id": 2}]
        with pytest.raises(KeyError):
            List.enum_by(data, "nonexistent")

def test_list_callable_raises_without_data():
    l = List()
    with pytest.raises(ValueError):
        l.flatterize()

class TestListInstance:
    """Tests for List instance methods and forwarding"""
    def test_list_instance_ensure_raises(self):
        """Test _ensure raises when data is None"""
        l = List()
        with pytest.raises(ValueError, match="List data is not set"):
            l._ensure()
    def test_list_instance_none_data_raises_on_forward(self):
        """Test that forwarded methods raise when data is None"""
        l = List()
        l.data = None
        with pytest.raises(ValueError, match="List data is not set"):
            l.shuffle()
