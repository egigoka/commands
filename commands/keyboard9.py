#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with keyboard
"""
__version__ = "0.0.1"


class Keyboard:

    @staticmethod
    def hotkey(*args, verbose=False, **kwargs):
        import pyautogui
        if verbose:
            print(f"Keyboard.hotkey({args=}, {kwargs=})")
        return pyautogui.hotkey(*args, **kwargs)