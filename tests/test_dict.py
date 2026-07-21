# Consolidated tests for commands/dict.py (unit)

# ---- from test_dict9.py ----


import pytest
from collections import OrderedDict
from commands.dict import Dict, ImDict


class TestImDict:
    """Tests for ImDict (immutable dict)"""

    def test_imdict_creation(self):
        d = ImDict({"a": 1, "b": 2})
        assert d["a"] == 1
        assert d["b"] == 2

    def test_imdict_hashable(self):
        d = ImDict({"a": 1})
        # Should be hashable
        hash_value = hash(d)
        assert isinstance(hash_value, int)









class TestDictIterable:
    """Tests for Dict.iterable method"""

    def test_iterable_basic(self):
        d = {"a": 1, "b": 2}
        result = list(Dict.iterable(d))
        assert ("a", 1) in result
        assert ("b", 2) in result

    def test_iterable_copy(self):
        d = {"a": 1, "b": 2}
        result = Dict.iterable(d, copy_dict=True)
        # Modify original
        d["c"] = 3
        # Copy should not be affected
        result_list = list(result)
        assert len(result_list) == 2



class TestDictSortedByKey:
    """Tests for Dict.sorted_by_key method"""

    def test_sorted_by_key_basic(self):
        d = {"c": 3, "a": 1, "b": 2}
        result = Dict.sorted_by_key(d)
        assert list(result.keys()) == ["a", "b", "c"]

    def test_sorted_by_key_case_insensitive(self):
        d = {"B": 2, "a": 1, "C": 3}
        result = Dict.sorted_by_key(d, case_insensitive=True)
        keys = list(result.keys())
        assert keys == ["a", "B", "C"] or keys == ["a", "C", "B"]  # a should be first

    def test_sorted_by_key_returns_ordered_dict(self):
        d = {"c": 3, "a": 1, "b": 2}
        result = Dict.sorted_by_key(d)
        assert isinstance(result, OrderedDict)

    def test_sorted_by_key_custom_func(self):
        d = {"short": 1, "verylongkey": 2, "mid": 3}
        result = Dict.sorted_by_key(d, func=lambda x: len(x[0]))
        keys = list(result.keys())
        assert keys[0] == "mid"  # Shortest
        assert keys[-1] == "verylongkey"  # Longest


class TestDictFromStr:
    """Tests for Dict.from_str method"""

    def test_from_str_basic(self):
        result = Dict.from_str("{'a': 1, 'b': 2}")
        assert result == {"a": 1, "b": 2}

    def test_from_str_empty(self):
        result = Dict.from_str("{}")
        assert result == {}

    def test_from_str_nested(self):
        result = Dict.from_str("{'outer': {'inner': 1}}")
        assert result == {"outer": {"inner": 1}}




class TestDictInstanceOf:
    """Tests for isinstance_keys and isinstance_values methods"""

    def test_isinstance_keys_true(self):
        d = {"a": 1, "b": 2, "c": 3}
        assert Dict.isinstance_keys(d, str) is True

    def test_isinstance_keys_false(self):
        d = {"a": 1, 2: "b"}
        assert Dict.isinstance_keys(d, str) is False

    def test_isinstance_keys_multiple_types(self):
        d = {"a": 1, 2: "b"}
        assert Dict.isinstance_keys(d, (str, int)) is True

    def test_isinstance_values_true(self):
        d = {"a": 1, "b": 2, "c": 3}
        assert Dict.isinstance_values(d, int) is True

    def test_isinstance_values_false(self):
        d = {"a": 1, "b": "two"}
        assert Dict.isinstance_values(d, int) is False

    def test_isinstance_values_multiple_types(self):
        d = {"a": 1, "b": "two"}
        assert Dict.isinstance_values(d, (int, str)) is True


class TestDictLambdaMethods:
    """Tests for all_keys_lambda and all_values_lambda methods"""

    def test_all_keys_lambda_basic(self):
        d = {"a": 1, "b": 2}
        result = Dict.all_keys_lambda(d, str.upper)
        assert result == {"A": 1, "B": 2}

    def test_all_keys_lambda_with_args(self):
        d = {"a": 1, "b": 2}
        result = Dict.all_keys_lambda(d, lambda k, suffix: k + suffix, args=("_key",))
        assert result == {"a_key": 1, "b_key": 2}

    def test_all_values_lambda_basic(self):
        d = {"a": 1, "b": 2}
        result = Dict.all_values_lambda(d, lambda v: v * 2)
        assert result == {"a": 2, "b": 4}

    def test_all_values_lambda_with_args(self):
        d = {"a": 1, "b": 2}
        result = Dict.all_values_lambda(d, lambda v, mult: v * mult, args=(3,))
        assert result == {"a": 3, "b": 6}

    def test_all_values_lambda_str_conversion(self):
        d = {"a": 1, "b": 2, "c": 3}
        result = Dict.all_values_lambda(d, str)
        assert result == {"a": "1", "b": "2", "c": "3"}


class TestDictHelpers:
    """Tests for helper methods"""

    def test_str_lower_of_dict_key(self):
        item = ("HELLO", 123)
        result = Dict.str_lower_of_dict_key(item)
        assert result == "hello"

    def test_get_dict_key(self):
        item = ("key", "value")
        result = Dict.get_dict_key(item)
        assert result == "key"


# Negative tests
class TestDictNegative:
    """Negative tests for Dict module"""

    def test_imdict_empty(self):
        """Should handle empty dict"""
        d = ImDict({})
        assert len(d) == 0
        assert hash(d) is not None

    def test_imdict_nested_mutable(self):
        """Should handle nested structures"""
        d = ImDict({"outer": {"inner": 1}})
        assert d["outer"]["inner"] == 1
        # Inner dict should still be mutable (only outer is ImDict)

    def test_iterable_empty_dict(self):
        """Should handle empty dictionary"""
        result = list(Dict.iterable({}))
        assert result == []

    def test_sorted_by_key_empty(self):
        """Should handle empty dict"""
        result = Dict.sorted_by_key({})
        assert result == {}



    def test_from_str_null(self):
        """Should handle None values"""
        result = Dict.from_str("{'key': None}")
        assert result == {"key": None}

    def test_isinstance_keys_empty_dict(self):
        """Should handle empty dict"""
        assert Dict.isinstance_keys({}, str) is True  # Vacuous truth

    def test_isinstance_values_empty_dict(self):
        """Should handle empty dict"""
        assert Dict.isinstance_values({}, int) is True  # Vacuous truth

    def test_all_keys_lambda_empty(self):
        """Should handle empty dict"""
        result = Dict.all_keys_lambda({}, str.upper)
        assert result == {}

    def test_all_values_lambda_empty(self):
        """Should handle empty dict"""
        result = Dict.all_values_lambda({}, lambda v: v * 2)
        assert result == {}




def test_dict_instance_helpers():
    d = Dict({"a": 1, "b": 2})
    assert d.iterable()
    assert d.isinstance_keys(int) is False
    assert d.isinstance_values(int) is True
    result = d.all_keys_lambda(lambda k: k.upper())
    assert result == {"A": 1, "B": 2}


class TestDictInstance:
    """Tests for Dict instance methods and forwarding"""

    def test_dict_instance_init_none(self):
        """Test Dict instance initialized with None uses empty dict"""
        d = Dict()
        assert d.data == {}

    def test_dict_instance_init_with_data(self):
        """Test Dict instance initialized with data"""
        d = Dict({"x": 10, "y": 20})
        assert d.data == {"x": 10, "y": 20}


    def test_dict_instance_iterable_forwarding(self):
        """Test instance method forwarding for iterable"""
        d = Dict({"a": 1, "b": 2})
        result = list(d.iterable())
        assert ("a", 1) in result
        assert ("b", 2) in result

    def test_dict_instance_isinstance_keys_forwarding(self):
        """Test instance method forwarding for isinstance_keys"""
        d = Dict({"a": 1, "b": 2})
        assert d.isinstance_keys(str) is True
        assert d.isinstance_keys(int) is False

    def test_dict_instance_isinstance_values_forwarding(self):
        """Test instance method forwarding for isinstance_values"""
        d = Dict({"a": 1, "b": 2})
        assert d.isinstance_values(int) is True
        assert d.isinstance_values(str) is False

    def test_dict_instance_all_keys_lambda_forwarding(self):
        """Test instance method forwarding for all_keys_lambda"""
        d = Dict({"a": 1, "b": 2})
        result = d.all_keys_lambda(str.upper)
        assert result == {"A": 1, "B": 2}

    def test_dict_instance_all_values_lambda_forwarding(self):
        """Test instance method forwarding for all_values_lambda"""
        d = Dict({"a": 1, "b": 2})
        result = d.all_values_lambda(lambda v: v * 10)
        assert result == {"a": 10, "b": 20}

    def test_dict_instance_sorted_by_key_forwarding(self):
        """Test instance method forwarding for sorted_by_key"""
        d = Dict({"c": 3, "a": 1, "b": 2})
        result = d.sorted_by_key()
        assert list(result.keys()) == ["a", "b", "c"]

    def test_dict_instance_lambda_with_kwargs(self):
        """Test lambda methods with kwargs parameter"""
        d = Dict({"a": 1, "b": 2})
        # Test with kwargs
        result = d.all_values_lambda(
            lambda v, mult=1: v * mult,
            kwargs=ImDict({"mult": 5})
        )
        assert result == {"a": 5, "b": 10}


    def test_dict_instance_getattribute_non_forwarded(self):
        """Test that non-forwarded attributes work normally"""
        d = Dict({"a": 1})
        assert hasattr(d, 'data')
        assert hasattr(d, '_ensure')
        assert d.data == {"a": 1}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
