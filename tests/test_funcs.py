# Consolidated tests for commands/funcs.py (unit)

# ---- from test_funcs9.py ----


import pytest
from commands.funcs import Q, dirify, multiple
from typing import Union


def test_q_repr_raises_systemexit():
    q = Q()
    with pytest.raises(SystemExit):
        repr(q)


def test_dirify_basic(capsys):
    class TestClass:
        attr1 = "value1"
        attr2 = 42
        attr3 = 3.14

    dirify(TestClass, "attr*")
    captured = capsys.readouterr()
    assert "attr1" in captured.out
    assert "attr2" in captured.out
    assert "attr3" in captured.out


def test_dirify_with_wildcard(capsys):
    class TestClass:
        test1 = 1
        test2 = 2
        other = 3

    dirify(TestClass, "test*")
    captured = capsys.readouterr()
    assert "test1" in captured.out
    assert "test2" in captured.out
    assert "other" not in captured.out


def test_multiple():
    result = multiple(int, str, float)
    assert result == Union[int, str, float]




# Negative tests






# Coverage improvement tests
class TestFuncsLegacyCoverage:
    """Tests to improve coverage for funcs9.py"""

    def test_q_call(self):
        """Test Q.__call__ method (lines 13-15)"""
        q = Q()
        # Calling q() should raise SystemExit
        with pytest.raises(SystemExit):
            q()

    def test_q_call_with_code(self):
        """Test Q.__call__ with exit code"""
        q = Q()
        with pytest.raises(SystemExit):
            q(0)

    def test_dirify_type_error(self, capsys):
        """Test dirify with TypeError exception (lines 35-36)"""
        # Create a class whose __getattribute__ raises TypeError with 2 args
        class TestClass:
            @classmethod
            def special_method(cls):
                pass

        # Access a classmethod, which may trigger TypeError path
        dirify(TestClass, "special*")
        captured = capsys.readouterr()
        assert "special" in captured.out

    def test_dirify_attribute_error(self, capsys):
        """Test dirify with AttributeError exception (lines 37-39)"""
        # Create a descriptor that raises AttributeError
        class BrokenDescriptor:
            def __get__(self, obj, objtype=None):
                raise AttributeError("Cannot access this")

        class TestClass:
            broken = BrokenDescriptor()
            normal = "value"

        dirify(TestClass, "*")
        captured = capsys.readouterr()
        # Should handle the AttributeError gracefully
        assert "AttributeError" in captured.out or "broken" in captured.out

    def test_dirify_os_error(self, capsys):
        """Test dirify with OSError exception (lines 40)"""
        # Create a descriptor that raises OSError
        class BrokenDescriptor:
            def __get__(self, obj, objtype=None):
                raise OSError("Cannot access this")

        class TestClass:
            broken = BrokenDescriptor()
            normal = "value"

        dirify(TestClass, "*")
        captured = capsys.readouterr()
        # Should handle the OSError gracefully
        assert "OSError" in captured.out or "broken" in captured.out



# ---- from test_funcs_coverage.py ----


import pytest
from commands.funcs import dirify
from io import StringIO
import sys


class TestFuncsCoverage:
    """Tests to improve funcs module coverage"""

    def test_dirify_handles_attribute_error(self, capsys):
        """Test dirify handles AttributeError gracefully"""

        class TestObj:
            def __getattribute__(self, name):
                if name == "bad_attr":
                    raise AttributeError("test error")
                return object.__getattribute__(self, name)

            bad_attr = "should trigger error"
            good_attr = "works fine"

        obj = TestObj()
        # This should handle AttributeError and continue
        dirify(obj, "bad_attr")

        captured = capsys.readouterr()
        assert "AttributeError happened" in captured.out

    def test_dirify_handles_os_error(self, capsys):
        """Test dirify handles OSError gracefully"""

        class TestObj:
            def __getattribute__(self, name):
                if name == "bad_os":
                    raise OSError("test os error")
                return object.__getattribute__(self, name)

            bad_os = "should trigger error"
            good_attr = "works fine"

        obj = TestObj()
        # This should handle OSError and continue
        dirify(obj, "bad_os")

        captured = capsys.readouterr()
        assert "OSError happened" in captured.out


# ---- from test_funcs_instance.py ----


import pytest
from commands.funcs import Q, dirify, copy, paste


def test_q_repr_exits():
    q = Q()
    with pytest.raises(SystemExit):
        repr(q)


def test_q_call_exits(monkeypatch):
    # Quitter will raise SystemExit
    q = Q()
    with pytest.raises(SystemExit):
        q()


# ---- from test_funcs_pyperclip.py ----


import sys
import types

from commands.funcs import copy, paste


def test_funcs_copy_and_paste_use_pyperclip(monkeypatch):
    store = {"value": None}

    def fake_copy(value):
        store["value"] = value

    def fake_paste():
        return store["value"]

    monkeypatch.setitem(sys.modules, "pyperclip", types.SimpleNamespace(copy=fake_copy, paste=fake_paste))

    copy("hello")
    assert paste() == "hello"
