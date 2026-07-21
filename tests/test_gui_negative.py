# Consolidated tests for commands/gui.py (negative)

# ---- from test_gui_negative.py ----

# Placeholder for future tests.
import pytest
import sys
from commands.gui import Gui
from commands.os import OS
import types

def test_gui_notify_raises_without_message():
    g = Gui()
    with pytest.raises(ValueError):
        g.notify()

def test_gui_notify_not_implemented(monkeypatch):
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", False)
    g = Gui("msg")
    with pytest.raises(NotImplementedError):
        g.notify()

def test_gui_warning_instance_missing_message_raises():
    with pytest.raises(ValueError, match="Message is not set"):
        Gui().warning()

def test_gui_notify_instance_missing_message():
    g = Gui()
    with pytest.raises(ValueError):
        g.notify()

def test_gui_notification_unsupported(monkeypatch):
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", False)
    with pytest.raises(NotImplementedError):
        Gui.notification("msg")

def test_gui_warning_missing_message(monkeypatch):
    with pytest.raises(ValueError):
        Gui().notify()
