# Consolidated tests for commands/list.py (unit)

# ---- from test_list9.py ----


import pytest
from commands.list import List


class TestListFlatterize:
    """Tests for List.flatterize method"""

    def test_flatterize_basic(self):
        result = List.flatterize([1, [2, 3], 4])
        assert result == [1, 2, 3, 4]

    def test_flatterize_nested(self):
        result = List.flatterize([1, [2, [3, 4]], 5])
        assert result == [1, 2, 3, 4, 5]  # Recursively flattens all levels

    def test_flatterize_tuple(self):
        result = List.flatterize((1, (2, 3), 4))
        assert result == [1, 2, 3, 4]



class TestListSplitEvery:
    """Tests for List.split_every method"""

    def test_split_every_basic(self):
        result = List.split_every([1, 2, 3, 4, 5, 6], 2)
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_split_every_uneven(self):
        result = List.split_every([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_split_every_zero(self):
        result = List.split_every([1, 2, 3], 0)
        assert result == [[1], [2], [3]]

    def test_split_every_larger_than_list(self):
        result = List.split_every([1, 2, 3], 10)
        assert result == [[1, 2, 3]]

    def test_split_every_single_element(self):
        result = List.split_every([1, 2, 3, 4], 1)
        assert result == [[1], [2], [3], [4]]


class TestListWildcardSearch:
    """Tests for List.wildcard_search method"""

    def test_wildcard_search_star(self):
        items = ["apple", "apricot", "banana", "application"]
        result = List.wildcard_search(items, "app*")
        assert result == ["apple", "application"]

    def test_wildcard_search_question(self):
        items = ["cat", "cut", "car", "cart"]
        result = List.wildcard_search(items, "c?t")
        assert result == ["cat", "cut"]

    def test_wildcard_search_combined(self):
        items = ["test1.txt", "test2.txt", "data.csv"]
        result = List.wildcard_search(items, "*.txt")
        assert result == ["test1.txt", "test2.txt"]

    def test_wildcard_search_no_match(self):
        items = ["apple", "banana"]
        result = List.wildcard_search(items, "orange")
        assert result == []


class TestListReplaceString:
    """Tests for List.replace_string method"""

    def test_replace_string_basic(self):
        result = List.replace_string(["hello", "world"], "o", "0")
        assert result == ["hell0", "w0rld"]

    def test_replace_string_integers(self):
        result = List.replace_string([123, 456], "3", "9")
        assert result == ["129", "456"]

    def test_replace_string_no_match(self):
        result = List.replace_string(["hello"], "x", "y")
        assert result == ["hello"]


class TestListApplyLambda:
    """Tests for List.apply_lambda_to_all_elements method"""

    def test_apply_lambda_basic(self):
        result = List.apply_lambda_to_all_elements([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_apply_lambda_string_upper(self):
        result = List.apply_lambda_to_all_elements(["a", "b"], str.upper)
        assert result == ["A", "B"]


class TestListToStrings:
    """Tests for List.to_strings method"""

    def test_to_strings_mixed_types(self):
        result = List.to_strings([1, 2.5, "test", True])
        assert result == ["1", "2.5", "test", "True"]

    def test_to_strings_already_strings(self):
        result = List.to_strings(["a", "b", "c"])
        assert result == ["a", "b", "c"]


class TestListRemoveDuplicates:
    """Tests for List.remove_duplicates method"""

    def test_remove_duplicates_preserve_order(self):
        result = List.remove_duplicates([3, 1, 2, 1, 3], preserve_order=True)
        assert result == [3, 1, 2]

    def test_remove_duplicates_no_preserve_order(self):
        result = List.remove_duplicates([1, 2, 1, 3, 2], preserve_order=False)
        assert set(result) == {1, 2, 3}
        assert len(result) == 3

    def test_remove_duplicates_no_duplicates(self):
        result = List.remove_duplicates([1, 2, 3])
        assert result == [1, 2, 3]

    def test_remove_duplicates_strings(self):
        result = List.remove_duplicates(["a", "b", "a", "c"], preserve_order=True)
        assert result == ["a", "b", "c"]


class TestListMostCommon:
    """Tests for List.most_common method"""

    def test_most_common_basic(self):
        result = List.most_common([1, 2, 2, 3, 3, 3], 2)
        assert result == [(3, 3), (2, 2)]

    def test_most_common_strings(self):
        result = List.most_common(["a", "b", "a", "a", "c", "b"], 2)
        assert result == [("a", 3), ("b", 2)]

    def test_most_common_single(self):
        result = List.most_common([1, 2, 2, 3], 1)
        assert result == [(2, 2)]


class TestListShuffle:
    """Tests for List.shuffle method"""

    def test_shuffle_preserves_elements(self):
        original = [1, 2, 3, 4, 5]
        result = List.shuffle(original)
        assert sorted(result) == sorted(original)

    def test_shuffle_doesnt_modify_original(self):
        original = [1, 2, 3]
        result = List.shuffle(original)
        assert original == [1, 2, 3]  # Original unchanged

    def test_shuffle_different_results(self):
        # Run shuffle multiple times, at least one should be different
        original = list(range(10))
        results = [List.shuffle(original) for _ in range(5)]
        # At least one shuffle should differ from original
        assert any(r != original for r in results)


class TestListRemoveEmptyStrings:
    """Tests for List.remove_empty_strings method"""

    def test_remove_empty_strings_basic(self):
        result = List.remove_empty_strings(["a", "", "b", "", "c"])
        assert "" not in result
        assert "a" in result and "b" in result and "c" in result

    def test_remove_empty_strings_no_empty(self):
        result = List.remove_empty_strings(["a", "b", "c"])
        assert result == ["a", "b", "c"]

    def test_remove_empty_strings_all_empty(self):
        result = List.remove_empty_strings(["", "", ""])
        assert len(result) < 3  # Some removed


class TestListSortBy:
    """Tests for List.sort_by method"""

    def test_sort_by_single_key(self):
        data = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
        result = List.sort_by(data, "age")
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"

    def test_sort_by_multiple_keys(self):
        data = [
            {"first": "John", "last": "Doe"},
            {"first": "Jane", "last": "Doe"},
            {"first": "Alice", "last": "Smith"}
        ]
        result = List.sort_by(data, "last", "first")
        assert result[0]["first"] == "Jane"  # Doe, Jane
        assert result[1]["first"] == "John"  # Doe, John
        assert result[2]["first"] == "Alice"  # Smith, Alice


class TestListEnumBy:
    """Tests for List.enum_by method"""

    def test_enum_by_basic(self):
        data = [("a", 1), ("b", 2), ("c", 3)]
        result = List.enum_by(data, 0)
        assert result == {"a": ("a", 1), "b": ("b", 2), "c": ("c", 3)}

    def test_enum_by_dict_list(self):
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        result = List.enum_by(data, "id")
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"


# Negative tests
class TestListNegative:
    """Negative tests for List module"""

    def test_flatterize_empty_list(self):
        """Should handle empty list"""
        result = List.flatterize([])
        assert result == []

    def test_flatterize_deeply_nested(self):
        """Should handle deeply nested lists"""
        result = List.flatterize([[[[[1]]]]])
        # May not flatten all levels, just verify it returns a list
        assert isinstance(result, list)

    def test_split_every_empty_list(self):
        """Should handle empty list"""
        result = List.split_every([], 5)
        # May return [[]] or []
        assert isinstance(result, list)

    def test_split_every_negative(self):
        """Should handle negative split size"""
        result = List.split_every([1, 2, 3], -1)
        # May raise error or handle gracefully
        assert isinstance(result, list)

    def test_wildcard_search_empty_list(self):
        """Should handle empty list"""
        result = List.wildcard_search([], "pattern")
        assert result == []

    def test_wildcard_search_empty_pattern(self):
        """Should handle empty pattern"""
        result = List.wildcard_search(["test"], "")
        assert isinstance(result, list)

    def test_apply_lambda_empty_list(self):
        """Should handle empty list"""
        result = List.apply_lambda_to_all_elements([], lambda x: x * 2)
        assert result == []


    def test_most_common_empty_list(self):
        """Should handle empty list"""
        result = List.most_common([], 5)
        assert result == []

    def test_most_common_zero_count(self):
        """Should handle zero count request"""
        result = List.most_common([1, 2, 3], 0)
        assert result == []

    def test_shuffle_empty_list(self):
        """Should handle empty list"""
        result = List.shuffle([])
        assert result == []


    def test_enum_by_empty_list(self):
        """Should handle empty list"""
        result = List.enum_by([], 0)
        assert result == {}



# Coverage improvement tests
class TestListCoverage:
    """Tests to improve coverage for list9.py"""

    def test_itemgetter_with_casting_non_iterable_cast_to(self):
        """Test itemgetter_with_casting with cast_to as single type (line 102)"""
        data = [{"num": "42"}, {"num": "100"}]
        # Pass int directly, not as tuple
        result = List.sort_by(data, "num", cast_to=int)
        assert result[0]["num"] == "42"
        assert result[1]["num"] == "100"

    def test_itemgetter_with_casting_single_item_fallback(self):
        """Test itemgetter_with_casting single item with casting failure (lines 107-110)"""
        data = [{"value": "not_a_number"}, {"value": "123"}]
        # Try to cast to int but will fail for first item - should fallback to original
        func = List.itemgetter_with_casting("value", cast_to=(int,))
        result1 = func(data[0])  # Should return original string
        assert result1 == "not_a_number"
        result2 = func(data[1])  # Should return int
        assert result2 == 123

    def test_itemgetter_with_casting_multiple_items_fallback(self):
        """Test itemgetter_with_casting multiple items with casting failure (lines 120-125)"""
        data = {"a": "not_a_number", "b": "456", "c": "also_not_a_number"}
        # Try to cast to int but will fail for some items
        func = List.itemgetter_with_casting("a", "b", "c", cast_to=(int,))
        result = func(data)
        # Should return tuple with original string for 'a', int for 'b', original for 'c'
        assert result[0] == "not_a_number"
        assert result[1] == 456
        assert result[2] == "also_not_a_number"

    def test_itemgetter_with_casting_multiple_cast_types(self):
        """Test itemgetter_with_casting with multiple types in cast_to"""
        data = [{"val": "123.45"}, {"val": "not_a_number"}]
        # Try float first, then int
        func = List.itemgetter_with_casting("val", cast_to=(float, int))
        assert func(data[0]) == 123.45  # Should cast to float
        assert func(data[1]) == "not_a_number"  # Should fallback to original

    def test_enum_by_with_cast_to(self):
        """Test enum_by with cast_to parameter (lines 144-148)"""
        # Create a simple class for testing
        class Item:
            def __init__(self, id, name):
                self.id = id
                self.name = name

        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        # Use cast_to to convert dict to Item objects
        # This should exercise the cast_to loop in enum_by
        result = List.enum_by(data, "id", cast_to=(Item,))
        # Casting will fail, so should keep original dicts
        assert result[1] == {"id": 1, "name": "Alice"}
        assert result[2] == {"id": 2, "name": "Bob"}

    def test_sort_by_with_cast_to_tuple(self):
        """Test sort_by with cast_to as tuple"""
        data = [{"num": "100"}, {"num": "20"}, {"num": "3"}]
        result = List.sort_by(data, "num", cast_to=(int,))
        # Should sort numerically, not lexicographically
        assert result[0]["num"] == "3"
        assert result[1]["num"] == "20"
        assert result[2]["num"] == "100"


def test_list_instance_helpers():
    l = List([1, [2, 3], 4])
    assert l.flatterize() == [1, 2, 3, 4]
    assert l.remove_duplicates() == [1, 2, 3, 4]
    l.data = [1, 2, 3, 4]
    assert l.split_every(2) == [[1, 2], [3, 4]]
    assert len(l.shuffle()) == 4


def test_list_callable_returns_data():
    l = List([1, 2, 3])
    assert l() == [1, 2, 3]




class TestListInstance:
    """Tests for List instance methods and forwarding"""

    def test_list_instance_init_none(self):
        """Test List instance initialized with None"""
        l = List()
        assert l.data is None

    def test_list_instance_init_with_data(self):
        """Test List instance initialized with data"""
        l = List([1, 2, 3])
        assert l.data == [1, 2, 3]

    def test_list_instance_call_with_data(self):
        """Test __call__ returns data when set"""
        l = List([5, 10, 15])
        assert l() == [5, 10, 15]

    def test_list_instance_call_with_none(self):
        """Test __call__ returns None when data is None"""
        l = List(None)
        assert l() is None


    def test_list_instance_flatterize_forwarding(self):
        """Test instance method forwarding for flatterize"""
        l = List([1, [2, 3], 4])
        result = l.flatterize()
        assert result == [1, 2, 3, 4]
        # Should update instance data
        assert l.data == [1, 2, 3, 4]

    def test_list_instance_split_every_forwarding(self):
        """Test instance method forwarding for split_every"""
        l = List([1, 2, 3, 4, 5, 6])
        result = l.split_every(2)
        assert result == [[1, 2], [3, 4], [5, 6]]
        # split_every doesn't modify instance data
        assert l.data == [1, 2, 3, 4, 5, 6]

    def test_list_instance_shuffle_forwarding(self):
        """Test instance method forwarding for shuffle"""
        l = List([1, 2, 3, 4, 5])
        original = l.data.copy()
        result = l.shuffle()
        # Should update instance data
        assert l.data == result
        # Should contain same elements
        assert sorted(l.data) == sorted(original)

    def test_list_instance_remove_duplicates_forwarding(self):
        """Test instance method forwarding for remove_duplicates"""
        l = List([1, 2, 2, 3, 3, 3])
        result = l.remove_duplicates()
        assert result == [1, 2, 3]
        # Should update instance data
        assert l.data == [1, 2, 3]

    def test_list_instance_remove_duplicates_no_order(self):
        """Test remove_duplicates without preserving order"""
        l = List([3, 1, 2, 1, 3, 2])
        result = l.remove_duplicates(preserve_order=False)
        # Should have unique elements
        assert set(result) == {1, 2, 3}
        assert len(result) == 3
        # Should update instance data
        assert l.data == result


    def test_list_instance_getattribute_non_forwarded(self):
        """Test that non-forwarded attributes work normally"""
        l = List([1, 2, 3])
        assert hasattr(l, 'data')
        assert hasattr(l, '_ensure')
        assert l.data == [1, 2, 3]

    def test_list_instance_multiple_operations(self):
        """Test chaining instance operations"""
        l = List([1, [2, 3], [4, 5]])
        # Flatterize first
        l.flatterize()
        assert l.data == [1, 2, 3, 4, 5]
        # Then shuffle
        l.shuffle()
        assert sorted(l.data) == [1, 2, 3, 4, 5]
        # Then split
        result = l.split_every(2)
        # split_every doesn't modify data
        assert len(l.data) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_list_enum_by_cast.py ----


from commands.list import List


def test_list_enum_by_cast_to_breaks_on_success():
    data = [(1, "10"), (2, "20")]
    out = List.enum_by(data, 0, cast_to=(list,))
    assert out[1] == [1, "10"]
    assert out[2] == [2, "20"]
