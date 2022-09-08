#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for screen capture.
"""
__version__ = "0.0.1"


class Screen:
    """Class with functions for screen capture.
    """

    @staticmethod
    def get_pixel_color(x, y=None):
        if y is None:
            y = x[1]
            x = x[0]
        import pyautogui

        r, g, b = pyautogui.pixel(x, y)
        return r, g, b
