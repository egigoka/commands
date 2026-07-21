# Consolidated tests for commands/id.py (unit)

# ---- from test_id9.py ----


import pytest
from commands.id import ID


def test_id_starts_at_zero():
    counter = ID()
    assert counter.get() == 0


def test_id_increments():
    counter = ID()
    assert counter.get() == 0
    assert counter.get() == 1
    assert counter.get() == 2


def test_id_multiple_instances():
    counter1 = ID()
    counter2 = ID()
    assert counter1.get() == 0
    assert counter2.get() == 0
    assert counter1.get() == 1
    assert counter2.get() == 1


def test_id_many_increments():
    counter = ID()
    for i in range(100):
        assert counter.get() == i


def test_id_call_method():
    """Test ID.__call__ method"""
    counter = ID()
    assert counter() == 0
    assert counter() == 1
    assert counter() == 2


def test_id_call_vs_get():
    """Test that __call__ and get are equivalent"""
    counter = ID()
    val1 = counter.get()  # Returns 0
    val2 = counter()  # Returns 1
    assert val1 == 0
    assert val2 == 1
    # Both methods increment, so they work the same way
    assert counter.get() == 2
    assert counter() == 3
