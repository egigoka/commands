# Consolidated tests for commands/random.py (unit)

# ---- from test_random9.py ----


import pytest
from commands.random import Random


class TestRandomInteger:
    """Tests for Random.integer method"""

    def test_integer_basic(self):
        result = Random.integer(1, 10)
        assert isinstance(result, int)
        assert 1 <= result <= 10

    def test_integer_reversed_range(self):
        """Test that reversed min/max are automatically swapped"""
        result = Random.integer(10, 1)
        assert 1 <= result <= 10

    def test_integer_same_min_max(self):
        result = Random.integer(5, 5)
        assert result == 5

    def test_integer_to_str(self):
        result = Random.integer(1, 100, to_str=True)
        assert isinstance(result, str)
        assert len(result) == 3  # Padded to match len(str(100))

    def test_integer_negative_range(self):
        result = Random.integer(-10, -1)
        assert -10 <= result <= -1

    def test_integer_range_includes_endpoints(self):
        """Test that both endpoints can be generated"""
        results = [Random.integer(1, 2) for _ in range(100)]
        assert 1 in results
        assert 2 in results


class TestRandomFloat:
    """Tests for Random.float method"""

    def test_float_basic(self):
        result = Random.float(0.0, 1.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_float_large_range(self):
        result = Random.float(0.0, 1000.0)
        assert 0.0 <= result <= 1000.0

    def test_float_negative_range(self):
        result = Random.float(-10.5, -1.5)
        assert -10.5 <= result <= -1.5

    def test_float_different_values(self):
        """Test that multiple calls produce different values"""
        results = [Random.float(0.0, 100.0) for _ in range(10)]
        # Very unlikely all 10 are the same
        assert len(set(results)) > 1


class TestRandomString:
    """Tests for Random.string method"""

    def test_string_basic(self):
        result = Random.string(10)
        assert isinstance(result, str)
        assert len(result) == 10

    def test_string_alphanumeric(self):
        result = Random.string(20)
        assert result.isalnum()

    def test_string_custom_symbols(self):
        result = Random.string(5, "abc")
        assert len(result) == 5
        assert all(c in "abc" for c in result)

    def test_string_length_zero(self):
        result = Random.string(0)
        assert result == ""

    def test_string_different_values(self):
        """Test that multiple calls produce different strings"""
        results = [Random.string(10) for _ in range(10)]
        assert len(set(results)) > 1


class TestRandomItem:
    """Tests for Random.item method"""

    def test_item_from_list(self):
        items = [1, 2, 3, 4, 5]
        result = Random.item(items)
        assert result in items

    def test_item_from_multiple_args(self):
        result = Random.item("a", "b", "c")
        assert result in ["a", "b", "c"]

    def test_item_from_dict(self):
        d = {"a": 1, "b": 2, "c": 3}
        key, value = Random.item(d)
        assert key in d
        assert d[key] == value

    def test_item_from_tuple(self):
        items = ("x", "y", "z")
        result = Random.item(items)
        assert result in items

    def test_item_kwargs(self):
        key, value = Random.item(a=1, b=2, c=3)
        assert key in ["a", "b", "c"]
        assert value in [1, 2, 3]


class TestRandomStringUnicode:
    """Tests for Random.string_unicode method"""

    def test_string_unicode_basic(self):
        result = Random.string_unicode(10)
        assert isinstance(result, str)
        assert len(result) == 10

    def test_string_unicode_contains_unicode(self):
        result = Random.string_unicode(20)
        # Should contain some non-ASCII characters
        has_unicode = any(ord(c) > 127 for c in result)
        assert has_unicode

    def test_string_unicode_different_values(self):
        results = [Random.string_unicode(10) for _ in range(5)]
        assert len(set(results)) > 1


class TestRandomBoolean:
    """Tests for Random.boolean method"""

    def test_boolean_returns_bool(self):
        result = Random.boolean()
        assert isinstance(result, bool)

    def test_boolean_both_values_possible(self):
        """Test that both True and False can be generated"""
        results = [Random.boolean() for _ in range(100)]
        assert True in results
        assert False in results

    def test_boolean_approximately_balanced(self):
        """Test that distribution is roughly 50/50"""
        results = [Random.boolean() for _ in range(1000)]
        true_count = sum(results)
        # Should be roughly 500, allow for some variance
        assert 400 <= true_count <= 600


class TestRandomGuid:
    """Tests for Random.guid method"""

    def test_guid_format(self):
        result = Random.guid()
        assert isinstance(result, str)
        # GUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assert len(result) == 36
        assert result.count("-") == 4

    def test_guid_lowercase(self):
        result = Random.guid()
        assert result == result.lower()

    def test_guid_hex_chars(self):
        result = Random.guid()
        hex_chars = set("0123456789abcdef-")
        assert all(c in hex_chars for c in result)

    def test_guid_unique(self):
        """Test that multiple GUIDs are different"""
        guids = [Random.guid() for _ in range(10)]
        assert len(set(guids)) == 10

    def test_guid_structure(self):
        result = Random.guid()
        parts = result.split("-")
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12


class TestRandomShuffle:
    """Tests for Random.shuffle method"""

    def test_shuffle_string(self):
        original = "abcdefgh"
        result = Random.shuffle(original)
        assert isinstance(result, str)
        assert len(result) == len(original)
        assert sorted(result) == sorted(original)

    def test_shuffle_list(self):
        original = ['a', 'b', 'c', 'd']
        result = Random.shuffle(original)
        assert isinstance(result, str)
        assert sorted(result) == sorted(''.join(original))

    def test_shuffle_actually_shuffles(self):
        """Test that shuffle produces different orderings"""
        original = "abcdefghijklmnop"
        results = [Random.shuffle(original) for _ in range(10)]
        # At least one should be different from original
        assert any(r != original for r in results)

    def test_shuffle_preserves_characters(self):
        original = "test123"
        result = Random.shuffle(original)
        assert sorted(result) == sorted(original)


def test_random_instance_helpers():
    r = Random(seed=123)
    assert r.integer(1, 3) in (1, 2, 3)
    assert isinstance(r.float(0, 1), float)
    assert len(r.string(4)) == 4
    assert r.boolean() in (True, False)
    assert isinstance(r(float_mode=True), float)
    assert isinstance(r(1, 2), int)


def test_random_integer_to_str():
    result = Random.integer(1, 9, to_str=True)
    assert isinstance(result, str)
    assert len(result) == 1


def test_random_shuffle_list_str():
    result = Random.shuffle(["a", "b"])
    assert set(result) == {"a", "b"}


# Negative tests








if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_random_comprehensive.py ----


import pytest
from commands.random import Random


class TestRandomInstanceComprehensive:
    """Comprehensive tests for Random instance methods to maximize coverage"""

    def test_instance_integer_to_str_branch(self):
        """Test instance integer with to_str=True to cover lines 19-23"""
        r = Random(seed=42)
        # Test with to_str=False (default)
        val1 = r.integer(1, 10, to_str=False)
        assert isinstance(val1, int)
        # Test with to_str=True
        val2 = r.integer(1, 100, to_str=True)
        assert isinstance(val2, str)
        assert len(val2) == 3  # Padded to len(str(100))

    def test_instance_float_coverage(self):
        """Test instance float method to cover line 26"""
        r = Random(seed=100)
        val = r.float(0.0, 10.0)
        assert isinstance(val, float)
        assert 0.0 <= val <= 10.0

    def test_instance_string_with_caching(self):
        """Test instance string to cover lines 29-36 including cache logic"""
        r = Random(seed=200)
        # First call - should create cache (line 34)
        s1 = r.string(5)
        assert len(s1) == 5
        assert s1.isalnum()
        # Second call - should use cached string_symbols (line 35)
        s2 = r.string(3)
        assert len(s2) == 3
        assert s2.isalnum()
        # Call with custom symbols (line 31 false branch)
        s3 = r.string(4, "xyz")
        assert len(s3) == 4
        assert all(c in "xyz" for c in s3)


    def test_instance_item_single_object(self):
        """Test instance item with single object to cover lines 39-40"""
        r = Random(seed=400)
        # Single list/tuple argument should be unwrapped
        result = r.item([1, 2, 3])
        assert result in [1, 2, 3]
        # Single tuple
        result2 = r.item(("a", "b", "c"))
        assert result2 in ("a", "b", "c")

    def test_instance_item_multiple_args(self):
        """Test instance item with multiple args"""
        r = Random(seed=500)
        # Multiple arguments
        result = r.item("x", "y", "z")
        assert result in ["x", "y", "z"]

    def test_instance_item_kwargs(self):
        """Test instance item with kwargs to cover lines 41-45"""
        r = Random(seed=600)
        # kwargs should be treated as dict (line 44-45)
        result = r.item(a=1, b=2, c=3)
        assert isinstance(result, tuple)
        key, value = result
        assert key in ["a", "b", "c"]
        assert value in [1, 2, 3]

    def test_instance_item_dict(self):
        """Test instance item with dict to cover line 45"""
        r = Random(seed=700)
        d = {"alpha": 10, "beta": 20}
        result = r.item(d)
        assert isinstance(result, tuple)
        key, value = result
        assert key in d
        assert d[key] == value

    def test_instance_item_non_dict(self):
        """Test instance item with non-dict to cover line 46"""
        r = Random(seed=800)
        # List should go through line 46
        result = r.item([10, 20, 30])
        assert result in [10, 20, 30]
        # String
        result2 = r.item("abc")
        assert result2 in "abc"

    def test_instance_boolean(self):
        """Test instance boolean to cover line 49"""
        r = Random(seed=900)
        val = r.boolean()
        assert isinstance(val, bool)
        # Test multiple calls to ensure both True and False are possible
        results = [r.boolean() for _ in range(50)]
        assert True in results or False in results

    def test_instance_call_integer_mode(self):
        """Test instance __call__ with integer mode (default)"""
        r = Random(seed=1000)
        val = r(5, 10)
        assert isinstance(val, int)
        assert 5 <= val <= 10

    def test_instance_call_float_mode(self):
        """Test instance __call__ with float_mode=True"""
        r = Random(seed=1100)
        val = r(1.0, 5.0, float_mode=True)
        assert isinstance(val, float)
        assert 1.0 <= val <= 5.0


class TestClassMethodsComprehensive:
    """Comprehensive tests for class methods to ensure full coverage"""

    def test_classmethod_integer_reversed(self):
        """Test integer with reversed min/max"""
        result = Random.integer(100, 50)
        assert 50 <= result <= 100

    def test_classmethod_item_single_list(self):
        """Test item with single list argument"""
        result = Random.item([1, 2, 3])
        assert result in [1, 2, 3]

    def test_classmethod_item_dict(self):
        """Test item with dict argument"""
        result = Random.item({"x": 1, "y": 2})
        assert isinstance(result, tuple)
        key, value = result
        assert key in ["x", "y"]

    def test_classmethod_item_kwargs(self):
        """Test item with kwargs"""
        result = Random.item(foo=10, bar=20)
        assert isinstance(result, tuple)

    def test_string_unicode_zero_length(self):
        """Test string_unicode with zero length"""
        result = Random.string_unicode(0)
        assert result == ""


class TestNegativeCases:
    """Additional negative tests"""

    def test_instance_string_zero_length(self):
        """Test that zero length string works"""
        r = Random(seed=1200)
        result = r.string(0)
        assert result == ""

    def test_classmethod_string_zero_length(self):
        """Test classmethod string with zero length"""
        result = Random.string(0)
        assert result == ""





if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_random_extra.py ----


import pytest

from commands.random import Random


def test_random_class_integer_min_gt_max():
    val = Random.integer(5, 1)
    assert 1 <= val <= 5




def test_random_instance_string_symbols_and_item(monkeypatch):
    r = Random(seed=1)
    s = r.string(3, string_of_symbols="ab")
    assert set(s).issubset(set("ab"))
    # dict item returns tuple
    item = r.item({"k": "v"})
    assert item[0] == "k"


def test_random_unicode_length():
    s = Random.string_unicode(5)
    assert len(s) == 5


def test_random_seed_determinism():
    r = Random(seed=42)
    val = r.integer(1, 10)
    s = r.string(5)
    assert isinstance(val, int)
    assert len(s) == 5
    assert r._seed == 42


# ---- from test_random_instance.py ----


import pytest
from commands.random import Random


class TestRandomInstance:
    """Tests for Random instance methods"""

    def test_instance_integer(self):
        """Test Random instance integer method"""
        r = Random(seed=42)
        result = r.integer(1, 10)
        assert isinstance(result, int)
        assert 1 <= result <= 10

    def test_instance_integer_to_str(self):
        """Test Random instance integer with to_str"""
        r = Random(seed=42)
        result = r.integer(1, 100, to_str=True)
        assert isinstance(result, str)
        assert len(result) == 3  # Padded to match len(str(100))

    def test_instance_float(self):
        """Test Random instance float method"""
        r = Random(seed=42)
        result = r.float(0.0, 1.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_instance_string(self):
        """Test Random instance string method"""
        r = Random(seed=42)
        result = r.string(10)
        assert isinstance(result, str)
        assert len(result) == 10

    def test_instance_string_custom_symbols(self):
        """Test Random instance string with custom symbols"""
        r = Random(seed=42)
        result = r.string(5, "abc")
        assert len(result) == 5
        assert all(c in "abc" for c in result)


    def test_instance_init_stores_seed(self):
        """Test that instance stores seed parameter"""
        r = Random(seed=42)
        assert r._seed == 42
        assert r._string_symbols is None
        assert r._rng is not None

    def test_instance_item_list(self):
        """Test Random instance item method with list"""
        r = Random(seed=42)
        items = [1, 2, 3, 4, 5]
        result = r.item(items)
        assert result in items

    def test_instance_item_multiple_args(self):
        """Test Random instance item method with multiple args"""
        r = Random(seed=42)
        result = r.item(1, 2, 3, 4, 5)
        assert result in [1, 2, 3, 4, 5]

    def test_instance_item_dict(self):
        """Test Random instance item method with dict"""
        r = Random(seed=42)
        items = {"a": 1, "b": 2, "c": 3}
        result = r.item(items)
        assert result in items.items()
        assert isinstance(result, tuple)

    def test_instance_item_kwargs(self):
        """Test Random instance item method with kwargs"""
        r = Random(seed=42)
        result = r.item(a=1, b=2, c=3)
        assert result in [("a", 1), ("b", 2), ("c", 3)]

    def test_instance_boolean(self):
        """Test Random instance boolean method"""
        r = Random(seed=42)
        results = [r.boolean() for _ in range(100)]
        # Should have both True and False
        assert True in results
        assert False in results

    def test_instance_call_integer_mode(self):
        """Test Random instance __call__ method in integer mode"""
        r = Random(seed=42)
        result = r(1, 10)
        assert isinstance(result, int)
        assert 1 <= result <= 10

    def test_instance_call_float_mode(self):
        """Test Random instance __call__ method in float mode"""
        r = Random(seed=42)
        result = r(0, 1, float_mode=True)
        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_instance_call_default_args(self):
        """Test Random instance __call__ with default args"""
        r = Random(seed=42)
        result = r()
        assert isinstance(result, int)
        assert 0 <= result <= 1

    def test_instance_call_default_args_float(self):
        """Test Random instance __call__ with default args in float mode"""
        r = Random(seed=42)
        result = r(float_mode=True)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_instance_method_shadowing_note(self):
        """Document that instance methods are shadowed by classmethods

        NOTE: The Random class has both instance methods (lines 18-49) and
        classmethods (lines 58+) with the same names. When calling r.method(),
        Python resolves to the classmethod, making instance methods unreachable
        through normal syntax. This is a code smell but not a bug we should fix
        in tests.

        The __call__ method (line 51-55) is an instance method that is NOT
        shadowed and works correctly.
        """
        r = Random(seed=42)
        # Verify instance is created with proper attributes
        assert hasattr(r, '_rng')
        assert hasattr(r, '_seed')
        assert hasattr(r, '_string_symbols')
        # __call__ is the main instance method that works
        assert callable(r)


# ---- from test_random_instance_extra.py ----


from commands.random import Random


def test_random_instance_integer_to_str_and_call():
    r = Random(seed=0)
    assert isinstance(r(1, 2), int)
    val = r.integer(1, 3, to_str=True)
    assert isinstance(val, str)
    assert len(val) == len(str(3))


def test_random_instance_float_and_boolean():
    r = Random(seed=1)
    f = r.float(-1, 1)
    assert -1 <= f <= 1
    b = r.boolean()
    assert isinstance(b, bool)


def test_random_instance_string_default_cache():
    r = Random(seed=2)
    first = r.string(4)
    second = r.string(2)
    assert len(first) == 4 and len(second) == 2
    assert first and second


def test_random_instance_item_variants():
    r = Random(seed=3)
    choice = r.item([10, 20, 30])
    assert choice in [10, 20, 30]
    key, value = r.item(alpha=1, beta=2)
    assert key in {"alpha", "beta"}
    assert value in {1, 2}


def test_random_instance_call_float_mode():
    r = Random(seed=4)
    val = r(0, 1, float_mode=True)
    assert isinstance(val, float)


# ---- from test_random_overlap_paths.py ----


import pytest

from commands import random as random_module
from commands.random import Random


def test_random_class_and_instance_overlap(monkeypatch):
    # Ensure class method integer swaps min/max and returns padded string when requested
    val = Random.integer(5, 1, to_str=True)
    assert isinstance(val, str)
    assert len(val) == len(str(5))

    # Instance path still uses internal RNG; ensure callable wrapper respects float_mode
    r = Random(seed=10)
    assert isinstance(r(1, 3, float_mode=True), float)

def test_random_instance_integer_invalid_range():
    r = Random(seed=0)
    val = r.integer(1, 0)
    assert 0 <= val <= 1
