#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with mouse."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, Tuple

from .module import LazyModule, LazyProperty

__version__ = "1.6.0"
Time = LazyProperty(".time", "Time")

pyautogui = LazyModule("pyautogui", optional=True)


class SettingsMouse:  # pylint: disable=too-few-public-methods
    """Mouse settings defaults."""

    mouse_move_duration = 0.5
    sleep_before_click = 0.1

    @classmethod
    def set_mouse_move_duration(cls, seconds: float) -> None:
        """Set default mouse move duration.

        <br>`param seconds` int|float, seconds to move mouse
        <br>`return` None
        """
        cls.mouse_move_duration = seconds


class Mouse:  # pylint: disable=too-few-public-methods
    """Class with functions to work with mouse."""

    def __init__(self) -> None:
        pass
    class Scroll:  # doesnt work good at new Windows >= 8
        """Class with functions to scroll."""

        @classmethod
        def scroll(cls, value: int, up: bool) -> None:  # pylint: disable=invalid-name
            """Scroll the mouse wheel.

            <br>`param value` int, how much to scroll, idk, how it work
            <br>`param up` boolean, scroll up or down
            <br>`return`
            """
            value = int(value)
            if not up:
                value = 0-value
            pyautogui.vscroll(clicks=value)
            print("scrolled", value)

        @classmethod
        def up(cls, value: int = 100) -> None:  # pylint: disable=invalid-name
            """Scroll up by a value.

            <br>`param value` int, how much to scroll, idk, how it work
            <br>`return`
            """
            cls.scroll(value, up=True)

        @classmethod
        def down(cls, value: int = 100) -> None:
            """Scroll down by a value.

            <br>`param value` int, how much to scroll, idk, how it work
            <br>`return`
            """
            cls.scroll(value, up=False)

    class Click:
        """Class with click mouse functions."""

        @classmethod
        def click(
            cls,
            button: str,
            position: Optional[Tuple[int, int]],
            verbose: bool = False,
            sleep_before_click: float = SettingsMouse.sleep_before_click
        ) -> None:
            """Click a mouse button.

            <br>`param button` string with button name
            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param verbose` boolean, suppress print to console
            <br>`return` None
            """
            Time.sleep(sleep_before_click, verbose=verbose)
            if position:
                pyautogui.click(x=position[0], y=position[1], button=button)
            else:
                pyautogui.click(button=button)
            if verbose:
                print("click mouse " + button)

        @classmethod
        def right(
            cls,
            position: Optional[Tuple[int, int]] = None,
            verbose: bool = False,
            sleep_before_click: float = SettingsMouse.sleep_before_click
        ) -> None:
            """Right-click the mouse.

            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param verbose` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='right', position=position, verbose=verbose, sleep_before_click=sleep_before_click)

        @classmethod
        def left(
            cls,
            position: Optional[Tuple[int, int]] = None,
            verbose: bool = False,
            sleep_before_click: float = SettingsMouse.sleep_before_click
        ) -> None:
            """Left-click the mouse.

            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param verbose` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='left', position=position, verbose=verbose, sleep_before_click=sleep_before_click)

        @classmethod
        def middle(
            cls,
            position: Optional[Tuple[int, int]] = None,
            verbose: bool = False,
            sleep_before_click: float = SettingsMouse.sleep_before_click
        ) -> None:
            """Click the middle mouse button.

            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param verbose` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='middle', position=position, verbose=verbose, sleep_before_click=sleep_before_click)

    @classmethod
    def move(
        cls,
        x: Any,
        y: Optional[int] = None,
        x2: Optional[int] = None,
        y2: Optional[int] = None,  # pylint: disable=too-many-arguments, invalid-name
        duration: float = SettingsMouse.mouse_move_duration,
        tween: Optional[Any] = None,
        rel: bool = False,
        verbose: bool = False
    ) -> None:
        """Move the mouse cursor.

        <br>`param x` int, position in pixels
        <br>`param y` int, position in pixels
        <br>`param x2` int, used if position is rectangle, so center will be found
        <br>`param y2` int, used if position is rectangle, so center will be found
        <br>`param duration` float|int, time to move mouse
        <br>`param tween` tween from pyautogui
        <br>`param rel` boolean, move relatively
        <br>`param verbose` boolean, suppress print to console
        <br>`return` None
        """
        if tween is None:
            tween = pyautogui.easeInOutQuad
        if isinstance(x, tuple):
            if len(x) == 2:
                y = x[1]
                x = x[0]
            elif len(x) == 4:
                y = x[1]
                x2 = x[2]
                y2 = x[3]
                x = x[0]
        if x2 and y2:
            x, y = pyautogui.center((x, y, x2, y2))
        if verbose:
            if rel:
                how = "relative"
            else:
                how = "to"
            print("moved mouse", how, x, y)

        if rel:
            pyautogui.moveRel(x, y, duration=duration, tween=tween)
        else:
            pyautogui.moveTo(x, y, duration=duration, tween=tween)

    @classmethod
    def get_position(cls) -> Tuple[int, int]:
        """Return the current mouse position.

        <br>`return` typle, x and y position of mouse
        """
        x, y = pyautogui.position()
        return int(x), int(y)

    # Instance helpers
    def scroll(self, value: int, up: bool = True) -> None:
        """Scroll the mouse wheel."""
        return self.Scroll.scroll(value, up=up)

    def click(
        self,
        button: str = "left",
        position: Optional[Tuple[int, int]] = None,
        verbose: bool = False,
        sleep_before_click: float = SettingsMouse.sleep_before_click
    ) -> None:
        """Click the mouse using instance defaults."""
        return self.Click.click(button, position, verbose=verbose, sleep_before_click=sleep_before_click)

    def move_to(
        self,
        x: Any,
        y: Optional[int] = None,
        x2: Optional[int] = None,
        y2: Optional[int] = None,
        duration: float = SettingsMouse.mouse_move_duration,
        tween: Optional[Any] = None,
        rel: bool = False,
        verbose: bool = False
    ) -> None:
        """Move the mouse using instance defaults."""
        return self.__class__.move(x, y=y, x2=x2, y2=y2, duration=duration, tween=tween, rel=rel, verbose=verbose)

    def position(self) -> Tuple[int, int]:
        """Return the current mouse position."""
        return self.__class__.get_position()
