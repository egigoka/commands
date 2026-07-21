# Consolidated tests for commands/dict.py (negative)

# ---- from test_dict_negative.py ----

# Placeholder for future tests.
import pytest
from collections import OrderedDict
from commands.dict import Dict, ImDict

class TestImDict:
    """Tests for ImDict (immutable dict)"""
    def test_imdict_setitem_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d["b"] = 2
    def test_imdict_delitem_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            del d["a"]
    def test_imdict_clear_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d.clear()
    def test_imdict_update_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d.update({"b": 2})
    def test_imdict_pop_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d.pop("a")
    def test_imdict_popitem_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d.popitem()
    def test_imdict_setdefault_raises(self):
        d = ImDict({"a": 1})
        with pytest.raises(TypeError, match="object is immutable"):
            d.setdefault("b", 2)

class TestDictIterable:
    """Tests for Dict.iterable method"""
    def test_iterable_invalid_type(self):
        with pytest.raises(TypeError, match="There must be dict in input"):
            Dict.iterable("not a dict")

class TestDictFromStr:
    """Tests for Dict.from_str method"""
    def test_from_str_invalid(self):
        with pytest.raises(Exception):  # literal_eval will raise
            Dict.from_str("not a dict")
    def test_from_str_list_raises(self):
        with pytest.raises(AssertionError, match="Output must be dict"):
            Dict.from_str("[1, 2, 3]")

class TestDictNegative:
    """Negative tests for Dict module"""
    def test_sorted_by_key_invalid_func(self):
        """Should handle invalid lambda function"""
        d = {"a": 1, "b": 2}
        with pytest.raises(Exception):
            Dict.sorted_by_key(d, func=lambda x: x.nonexistent_attr())
    def test_from_str_malformed(self):
        """Should raise on malformed string"""
        with pytest.raises(Exception):
            Dict.from_str("{'key': incomplete")
    def test_all_keys_lambda_exception(self):
        """Should handle lambda that raises exception"""
        d = {"a": 1, "b": 2}
        with pytest.raises(Exception):
            Dict.all_keys_lambda(d, lambda k: k.nonexistent_method())
    def test_all_values_lambda_exception(self):
        """Should handle lambda that raises exception"""
        d = {"a": 1, "b": "string"}
        with pytest.raises(Exception):
            Dict.all_values_lambda(d, lambda v: v.nonexistent_method())

class TestDictInstance:
    """Tests for Dict instance methods and forwarding"""
    def test_dict_instance_ensure_raises(self):
        """Test _ensure raises when data is None"""
        d = Dict()
        d.data = None  # Force None
        with pytest.raises(ValueError, match="Dict data is not set"):
            d._ensure()
    def test_dict_instance_none_data_raises_on_forward(self):
        """Test that forwarded methods raise when data is None"""
        d = Dict()
        d.data = None
        with pytest.raises(ValueError, match="Dict data is not set"):
            d.iterable()
