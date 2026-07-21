# Consolidated tests for commands/screen.py (unit)

# ---- from test_screen9.py ----


import pytest


def test_screen9_import():
    from commands import Screen
    assert Screen is not None


def test_screen_instance_helper(monkeypatch):
    from commands.screen import Screen
    import commands.screen as screen_mod
    screen_mod.pyautogui = type("M", (), {"pixel": staticmethod(lambda x, y: (1, 2, 3))})()
    s = Screen((10, 20))
    assert s.color() == (1, 2, 3)


# ---- from test_screen_coverage.py ----


import pytest
from commands.screen import Screen


class TestScreenCoverage:
    """Tests to improve Screen module coverage"""


    def test_get_pixel_color_without_stub(self, monkeypatch):
        """Test get_pixel_color when pyautogui is not stubbed"""
        import sys
        import commands.screen as screen_mod

        # Remove any existing stub
        if hasattr(screen_mod, 'pyautogui'):
            delattr(screen_mod, 'pyautogui')

        # Mock the real pyautogui import
        mock_pyautogui = type("MockPyAutoGUI", (), {
            "pixel": staticmethod(lambda x, y: (100, 150, 200))
        })()

        # Patch the import
        monkeypatch.setitem(sys.modules, 'pyautogui', mock_pyautogui)

        # Call get_pixel_color - it should import pyautogui
        result = Screen.get_pixel_color(10, 20)
        assert result == (100, 150, 200)
