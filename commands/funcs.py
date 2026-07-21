#! python3
# -*- coding: utf-8 -*-
"""Internal module with utility functions."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, NoReturn, Optional, Type

from .module import LazyModule, LazyProperty

__version__ = "3.4.3"
sitebuiltins = LazyModule("_sitebuiltins")
List = LazyProperty(".list", "List")
Str = LazyProperty(".str", "Str")

pyperclip = LazyModule("pyperclip")
typing = LazyModule("typing")


class Q:
    """Raise SystemExit on representation or call."""

    def __repr__(self) -> NoReturn:
        """Exit when represented."""
        raise SystemExit

    def __call__(self, code: Optional[int] = None) -> NoReturn:
        """Exit with optional status code."""
        quitter = sitebuiltins.Quitter("q", "end of file? wtf? why it's string?")
        quitter.__call__(code)
        raise SystemExit(code)


def dirify(_object: Any, wildcard: str = "*") -> None:
    """Print and return list of object public attributes.

    <br>`param object_` object to input
    <br>`param regexp` string with shell-like wildcards for filtering
    <br>`param verbose` suppress output to console
    <br>`return` None
    """
    longest_name = 0
    attrs = List.wildcard_search(dir(_object), wildcard)
    for attr_str in attrs:
        if len(attr_str) > longest_name:
            longest_name = len(attr_str)
    for attr_str in attrs:
        try:
            _type: Any = type(_object.__getattribute__(attr_str))
        except TypeError:
            _type = type(_object.__getattribute__(_object, attr_str))
        except AttributeError:
            _type = "AttributeError happened"
        except OSError:
            _type = "OSError happened"
        _type = Str.substring(str(_type), "<class ", ">", safe=True)
        print(f"{Str.rightpad(attr_str, longest_name, '—')}>{_type}")


def multiple(*types: Type[Any]) -> Any:
    """Return a typing.Union of the provided types."""
    return typing.Union[types]


def copy(string: str) -> None:
    """Copy a string to the clipboard."""
    pyperclip.copy(string)


def paste() -> str:
    """Paste a string from the clipboard."""
    return pyperclip.paste()  # type: ignore[no-any-return]


q = Q()
exit = Q()
