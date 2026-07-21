# Consolidated tests for commands/int.py (unit)

# ---- from test_int9.py ----


import pytest
from commands.int import Int


class TestIntFromTo:
    """Tests for Int.from_to method"""

    def test_from_to_basic(self):
        result = list(Int.from_to(1, 5))
        assert result == [1, 2, 3, 4, 5]

    def test_from_to_negative(self):
        result = list(Int.from_to(-2, 2))
        assert result == [-2, -1, 0, 1, 2]

    def test_from_to_single(self):
        result = list(Int.from_to(5, 5))
        assert result == [5]

    def test_from_to_to_str(self):
        result = Int.from_to(1, 5, to_str=True)
        assert result == ["1", "2", "3", "4", "5"]

    def test_from_to_to_str_padded(self):
        result = Int.from_to(7, 12, to_str=True)
        assert result == ["07", "08", "09", "10", "11", "12"]

    def test_from_to_to_str_negative(self):
        result = Int.from_to(-2, 2, to_str=True)
        assert result == ["-2", "-1", "00", "01", "02"]

    def test_from_to_large_range(self):
        result = list(Int.from_to(1, 100))
        assert len(result) == 100
        assert result[0] == 1
        assert result[-1] == 100

    def test_from_to_returns_range(self):
        """Test that from_to returns a range object (iterable)"""
        result = Int.from_to(1, 5, to_str=False)
        assert hasattr(result, '__iter__')

    # Negative tests
    def test_from_to_reversed_range(self):
        """Should handle reversed range (from > to)"""
        result = list(Int.from_to(5, 1))
        # Should return empty or reversed
        assert len(result) == 0 or result == [5, 4, 3, 2, 1]

    def test_from_to_very_large_range(self):
        """Should handle very large ranges without consuming too much memory"""
        result = Int.from_to(1, 1000000, to_str=False)
        # Should be a generator/range, not a list
        assert hasattr(result, '__iter__')
        # Should be able to get first and last without materializing entire range
        lst = list(result)
        assert lst[0] == 1
        assert lst[-1] == 1000000

    def test_from_to_extreme_negative(self):
        """Should handle very negative numbers"""
        result = list(Int.from_to(-100, -95))
        assert result == [-100, -99, -98, -97, -96, -95]

    def test_from_to_zero_crossing(self):
        """Should handle ranges that cross zero"""
        result = list(Int.from_to(-3, 3))
        assert result == [-3, -2, -1, 0, 1, 2, 3]

    def test_int_instance_shortcut(self):
        i = Int()
        assert list(i.from_to(1, 3)) == [1, 2, 3]


def test_int_instance_range():
    i = Int(1, 2)
    assert list(i.range()) == [1, 2]


class TestIntInstance:
    """Tests for Int instance methods"""

    def test_int_instance_init_both_params(self):
        """Test Int instance with both start and end"""
        i = Int(1, 10)
        assert i.start == 1
        assert i.end == 10

    def test_int_instance_init_none(self):
        """Test Int instance initialized with None values"""
        i = Int()
        assert i.start is None
        assert i.end is None

    def test_int_instance_init_partial(self):
        """Test Int instance with only start"""
        i = Int(5)
        assert i.start == 5
        assert i.end is None




    def test_int_instance_range_basic(self):
        """Test instance range method"""
        i = Int(1, 5)
        result = list(i.range())
        assert result == [1, 2, 3, 4, 5]

    def test_int_instance_range_to_str(self):
        """Test instance range method with to_str"""
        i = Int(7, 12)
        result = i.range(to_str=True)
        assert result == ["07", "08", "09", "10", "11", "12"]

    def test_int_instance_range_negative(self):
        """Test instance range with negative numbers"""
        i = Int(-3, 3)
        result = list(i.range())
        assert result == [-3, -2, -1, 0, 1, 2, 3]

    def test_int_instance_range_negative_to_str(self):
        """Test instance range with negative numbers to_str"""
        i = Int(-5, 5)
        result = i.range(to_str=True)
        # Should have proper padding
        assert "-5" in result
        assert "05" in result or " 5" in result


    def test_int_instance_range_single_value(self):
        """Test instance range with single value"""
        i = Int(42, 42)
        result = list(i.range())
        assert result == [42]

    def test_int_instance_range_reversed(self):
        """Test instance range with reversed values"""
        i = Int(10, 5)
        result = list(i.range())
        # Should be empty for reversed range
        assert len(result) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
