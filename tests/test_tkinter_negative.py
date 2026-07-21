# Consolidated tests for commands/tkinter.py (negative)

# ---- from test_tkinter_negative.py ----

# Placeholder for future tests.
import pytest
from commands.tkinter import Tkinter

def test_tkinter_rgb_missing():
    from commands.tkinter import Tkinter
    t = Tkinter()
    with pytest.raises(ValueError):
        t()

def test_tkinter_instance_rgb_missing_raises():
    t = Tkinter(red=1)
    with pytest.raises(ValueError, match="red, green and blue must be set"):
        t.rgb()
