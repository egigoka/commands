# Consolidated tests for commands/funcs.py (negative)

# ---- from test_funcs_negative.py ----

# Placeholder for future tests.
import pytest
from commands.funcs import Q, dirify, multiple
from typing import Union
from commands.funcs import dirify
from io import StringIO
import sys
from commands.funcs import Q, dirify, copy, paste
import types
from commands.funcs import copy, paste

def test_dirify_nonexistent_attribute(capsys):
    """Should handle objects with no matching attributes"""
    class TestClass:
        real_attr = 1

    dirify(TestClass, "nonexistent*")
    captured = capsys.readouterr()
    # Should produce no output or handle gracefully
    assert "nonexistent" not in captured.out

def test_dirify_empty_wildcard(capsys):
    """Should handle empty wildcard"""
    class TestClass:
        attr1 = 1

    dirify(TestClass, "")
    captured = capsys.readouterr()
    # Empty wildcard matches nothing
    assert captured.out == ""

def test_multiple_with_no_types():
    """Should raise TypeError when no types provided"""
    with pytest.raises(TypeError, match="Cannot take a Union of no types"):
        multiple()
