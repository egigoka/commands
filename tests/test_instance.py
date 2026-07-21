# Consolidated tests for commands/instance.py (unit)

# ---- from test_instance_coverage.py ----


import pytest
from commands._instance import add_instance_shortcuts




# ---- from test_instance_shortcuts.py ----


from commands._instance import add_instance_shortcuts


class Dummy:
    @classmethod
    def foo(cls):
        return "bar"


def test_add_instance_shortcuts_adds_getattr():
    add_instance_shortcuts(Dummy)
    d = Dummy()
    assert d.foo() == "bar"


def test_add_instance_shortcuts_non_callable_attr():
    class Dummy2:
        value = 1
    add_instance_shortcuts(Dummy2)
    d = Dummy2()
    try:
        _ = d.value
    except AttributeError:
        assert False, "Should allow non-callable attributes to raise naturally"


def test_add_instance_shortcuts_delegate_called():
    add_instance_shortcuts(Dummy)
    d = Dummy()
    # __getattr__ should now be present; call directly to execute delegate
    assert d.__getattr__("foo")() == "bar"
