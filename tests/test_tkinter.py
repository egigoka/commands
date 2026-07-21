# Consolidated tests for commands/tkinter.py (unit)

# ---- from test_tkinter9.py ----


import pytest


def test_tkinter9_import():
    from commands import Tkinter
    assert Tkinter is not None


def test_tkinter_color_rgb():
    from commands.tkinter import Tkinter
    assert Tkinter.color(255, 0, 0) == "#ff0000"
    t = Tkinter(0, 128, 255)
    assert t() == "#0080ff"




# ---- from test_tkinter_more.py ----


import pytest

from commands.tkinter import Tkinter


def test_tkinter_color_formats_hex():
    assert Tkinter.color(0, 0, 0) == "#000000"
    assert Tkinter.color(255, 255, 255) == "#ffffff"
    assert Tkinter.color(1, 2, 3) == "#010203"


def test_tkinter_instance_rgb_uses_defaults():
    t = Tkinter(red=1, green=2, blue=3)
    assert t.rgb() == "#010203"
    assert t() == "#010203"


def test_tkinter_instance_rgb_overrides_defaults():
    t = Tkinter(red=1, green=2, blue=3)
    assert t.rgb(10, 11, 12) == "#0a0b0c"
