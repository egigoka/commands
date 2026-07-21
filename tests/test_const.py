# Consolidated tests for commands/const.py (unit)

# ---- from test_const9.py ----


import pytest
from commands import const


def test_newline():
    assert const.newline == '\n'


def test_ruble():
    assert const.ruble == u"\u20bd"
    assert const.ruble == "₽"


def test_backslash():
    assert const.backslash == "\\"


def test_newline2():
    assert const.newline2 == "\r\n"


def test_rtl():
    assert const.rtl == "\u202e"


def test_kib():
    assert const.KiB == 1024


def test_mib():
    assert const.MiB == 1024 * 1024
    assert const.MiB == 1048576


def test_gib():
    assert const.GiB == 1024 * 1024 * 1024
    assert const.GiB == 1073741824


def test_tib():
    assert const.TiB == 1024 * 1024 * 1024 * 1024
    assert const.TiB == 1099511627776


# Negative tests
def test_constants_are_immutable_types():
    """Verify constants are immutable types"""
    # Strings and integers are immutable in Python
    assert isinstance(const.newline, str)
    assert isinstance(const.backslash, str)
    assert isinstance(const.KiB, int)


def test_byte_size_relationships():
    """Verify byte size constants have correct relationships"""
    assert const.MiB == const.KiB * 1024
    assert const.GiB == const.MiB * 1024
    assert const.TiB == const.GiB * 1024
    # All should be positive
    assert const.KiB > 0
    assert const.MiB > const.KiB
    assert const.GiB > const.MiB
    assert const.TiB > const.GiB
