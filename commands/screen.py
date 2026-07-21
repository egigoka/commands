#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for screen capture."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Tuple, Union

from .module import LazyModule, LazyProperty

__version__ = "0.0.1"
sys = LazyModule("sys")

pyautogui = LazyModule("pyautogui", optional=True)


class Screen:
    """Class with functions for screen capture."""

    def __init__(self, position: Optional[Tuple[int, int]] = None) -> None:
        self.position = position

    @classmethod
    def get_pixel_color(cls, x: Union[int, Tuple[int, int]], y: Optional[int] = None) -> Tuple[int, int, int]:
        """Get the RGB color for a pixel at the given position."""
        if y is None:
            assert isinstance(x, tuple)
            y = x[1]
            x = x[0]
        # Prefer stubbed pyautogui if already injected (for tests/headless)
        pyautogui_instance = getattr(sys.modules.get(__name__), "pyautogui", None)
        if pyautogui_instance is None:
            pyautogui_instance = globals().get("pyautogui")
        if pyautogui_instance is None:
            pyautogui_instance = LazyModule("pyautogui", optional=True)

        r, g, b = pyautogui_instance.pixel(x, y)
        return r, g, b

    def color(self) -> Tuple[int, int, int]:
        """Get the RGB color for the stored position."""
        if self.position is None:
            raise ValueError("Position is not set")
        return self.__class__.get_pixel_color(self.position)
