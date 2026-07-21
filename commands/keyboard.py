#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with keyboard."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

from .module import LazyModule

__version__ = "0.2.2"

pyautogui = LazyModule("pyautogui", optional=True)


class Keyboard:
    """Keyboard interaction helpers."""

    def __init__(self) -> None:
        pass

    @classmethod
    def hotkey(cls, *args: str, verbose: bool = False, **kwargs: Any) -> Any:
        """Trigger a hotkey combination via pyautogui."""
        if verbose:
            print(f"Keyboard.hotkey({args=}, {kwargs=})")
        return pyautogui.hotkey(*args, **kwargs)

    # https://github.com/asweigart/pyautogui/issues/137

    @classmethod
    def translate(cls, key: str) -> str:
        """Return qwerty key or the given key itself if no mapping found."""
        qwerty = r"!\@#$%^&*()_+qwertyuiop[]asdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
        ycuken = r"!\"№;%:?*()_+йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖ\ЭЯЧСМИТЬБЮ,"

        tr = dict(zip(ycuken, qwerty))  # join as keys and values

        return "".join(map(lambda x: tr.get(x, x), key))

    @classmethod
    def translate_string(cls, string: str) -> str:
        """Translate a full string from ycuken to qwerty layout."""
        output = ""
        for symbol in string:
            output += cls.translate(symbol)
        return output

    @classmethod
    def write(cls, string: str, verbose: bool = False) -> None:
        """Type a translated string via pyautogui."""
        output = cls.translate_string(string)

        if verbose:
            print(f'Keyboard.write("{string}") -> pyautogui.write("{output}")')

        pyautogui.write(output)

    # Instance-friendly wrappers
    def hotkey_do(self, *args: str, verbose: bool = False, **kwargs: Any) -> Any:
        """Instance wrapper for hotkey."""
        return self.__class__.hotkey(*args, verbose=verbose, **kwargs)

    def type(self, string: str, verbose: bool = False) -> None:
        """Instance wrapper for write."""
        self.__class__.write(string, verbose=verbose)
