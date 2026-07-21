# Consolidated tests for commands/module.py (unit)

# ---- from test_module.py ----


import math
import types
import pytest

from commands.module import LazyModule, LazyProperty




def test_lazy_module_sys_modules_override(monkeypatch):
    dummy_module = types.SimpleNamespace(value=42)
    monkeypatch.setitem(__import__("sys").modules, "dummy_mod", dummy_module)
    lazy = LazyModule("dummy_mod")
    assert bool(lazy) is True
    assert lazy.value == 42
    assert repr(lazy) == repr(dummy_module)


def test_lazy_module_overrides_and_delete():
    lazy = LazyModule("math")
    lazy.custom = "override"
    assert lazy.custom == "override"
    del lazy.custom
    with pytest.raises(AttributeError):
        _ = lazy.custom


def test_lazy_module_dir_optional_missing():
    lazy = LazyModule("module_that_does_not_exist_67890", optional=True)
    assert lazy.__dir__() == []


def test_lazy_property_repr_and_call():
    prop = LazyProperty("math", "sqrt")
    assert "LazyProperty" in repr(prop)
    assert prop(9) == 3
    assert "LazyProperty" not in repr(prop)


def test_lazy_property_bin_ops():
    prop = LazyProperty("math", "pi")
    assert round(prop + 1, 6) == round(math.pi + 1, 6)
    assert round(1 + prop, 6) == round(math.pi + 1, 6)
    assert round(prop * 2, 6) == round(math.pi * 2, 6)


def test_lazy_property_attr_set_del(monkeypatch):
    target = types.SimpleNamespace(value=1)
    dummy_module = types.SimpleNamespace(target=target)
    monkeypatch.setitem(__import__("sys").modules, "dummy_lazy_prop", dummy_module)
    prop = LazyProperty("dummy_lazy_prop", "target")
    assert prop.value == 1
    prop.value = 2
    assert target.value == 2
    prop.new_attr = "x"
    assert target.new_attr == "x"
    del prop.new_attr
    assert not hasattr(target, "new_attr")
