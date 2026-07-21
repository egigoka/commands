# Consolidated tests for commands/obj.py (unit)

# ---- from test_obj9.py ----


import pytest
from commands.obj import Obj


def test_cast_to_int():
    assert Obj.cast_to("123", [int]) == 123


def test_cast_to_float():
    assert Obj.cast_to("123.45", [float]) == 123.45


def test_cast_to_str():
    assert Obj.cast_to(123, [str]) == "123"


def test_cast_to_multiple_types_first_succeeds():
    assert Obj.cast_to("123", [int, float, str]) == 123


def test_cast_to_multiple_types_second_succeeds():
    assert Obj.cast_to("123.45", [int, float, str]) == 123.45




def test_cast_to_bool():
    assert Obj.cast_to(1, [bool]) is True
    assert Obj.cast_to(0, [bool]) is False


def test_cast_to_list():
    assert Obj.cast_to("abc", [list]) == ['a', 'b', 'c']


def test_obj_instance_helper():
    o = Obj("123")
    assert o.cast([int, str]) == 123




# Negative tests






def test_cast_to_none_value():
    """Should handle None value"""
    result = Obj.cast_to(None, [int, str])
    assert result is None or isinstance(result, str)


def test_cast_to_complex_object():
    """Should return original for complex objects that can't be cast"""
    class CustomClass:
        pass

    obj = CustomClass()
    result = Obj.cast_to(obj, [int, str, float])
    assert result == obj or isinstance(result, str)


class TestObjInstance:
    """Tests for Obj instance methods"""

    def test_obj_instance_init_none(self):
        """Test Obj instance initialized with None"""
        o = Obj()
        assert o.obj is None

    def test_obj_instance_init_with_value(self):
        """Test Obj instance initialized with value"""
        o = Obj("123")
        assert o.obj == "123"

    def test_obj_instance_cast_to_int(self):
        """Test instance cast method to int"""
        o = Obj("42")
        result = o.cast([int])
        assert result == 42
        assert isinstance(result, int)

    def test_obj_instance_cast_to_float(self):
        """Test instance cast method to float"""
        o = Obj("3.14")
        result = o.cast([float])
        assert result == 3.14
        assert isinstance(result, float)

    def test_obj_instance_cast_multiple_types(self):
        """Test instance cast with multiple types"""
        o = Obj("100")
        result = o.cast([int, float, str])
        assert result == 100  # Should cast to first successful type


    def test_obj_instance_cast_with_list(self):
        """Test instance cast with list type"""
        o = Obj("abc")
        result = o.cast([list])
        assert result == ['a', 'b', 'c']

    def test_obj_instance_cast_bool(self):
        """Test instance cast to bool"""
        o = Obj(1)
        result = o.cast([bool])
        assert result is True


    def test_obj_instance_multiple_casts(self):
        """Test multiple cast operations on same instance"""
        o = Obj("123")
        result1 = o.cast([int])
        # obj doesn't change, so we can cast again
        o.obj = "456"
        result2 = o.cast([int])
        assert result1 == 123
        assert result2 == 456

    def test_obj_instance_cast_none(self):
        """Test instance cast with None value"""
        o = Obj(None)
        result = o.cast([int, str])
        assert result is None or isinstance(result, str)
