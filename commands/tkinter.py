#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with tkinter."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional

__version__ = "0.0.2"


class Tkinter:  # pylint: disable=too-few-public-methods
    """Class to simplify work with tkinter."""

    def __init__(self, red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def color(cls, red: int, green: int, blue: int) -> str:
        """Build a Tkinter color string from RGB values.

        <br>`param red` red intensity (0-255)
        <br>`param green` green intensity (0-255)
        <br>`param blue` green intensity (0-255)
        <br>`return` string of color matching for use in Tkinter
        """
        return str('#%02x%02x%02x' % (red, green, blue))

    def rgb(self, red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None) -> str:
        """Instance-friendly color helper using stored defaults when provided."""
        red = self.red if red is None else red
        green = self.green if green is None else green
        blue = self.blue if blue is None else blue
        if red is None or green is None or blue is None:
            raise ValueError("red, green and blue must be set")
        return self.color(red, green, blue)

    __call__ = rgb
