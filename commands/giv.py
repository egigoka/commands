#! python3
# -*- coding: utf-8 -*-
"""Global Interpreter Variables."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, cast
    from .json import JsonDict
    from .path import Path
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value


__version__ = "0.1.0"
if not TYPE_CHECKING:
    JsonDict = LazyProperty(".json", "JsonDict")
    Path = LazyProperty(".path", "Path")


class GIV:
    """Global Interpreter Variables implementation."""

    json: Optional[JsonDict] = None
    _sentinel: object = object()

    def __call__(self, key: str, value: Any = _sentinel) -> Any:
        """Shortcut: GIV(key) -> get, GIV(key, value) -> set and return value."""
        if value is self._sentinel:
            return self.__class__.__getitem__(key)
        self.__class__.__setitem__(key, value)
        return value

    @classmethod
    def init(cls) -> None:
        """Initialize the backing JSON storage."""
        if cls.json is None:

            json_path = Path.combine(Path.temp(), "commands_GIV.json")
            cls.json = JsonDict(json_path, debug=False, verbose=False)

    @classmethod
    def __getitem__(cls, item: str) -> Any:
        """Return the value for a key."""
        cls.init()
        json_obj = cast(JsonDict, cls.json)
        json_obj.load()
        return json_obj.__getitem__(item)

    @classmethod
    def __setitem__(cls, key: str, value: Any) -> None:
        """Set a value for a key."""
        cls.init()
        json_obj = cast(JsonDict, cls.json)
        json_obj.__setitem__(key, value)
        json_obj.save()

    @classmethod
    def __repr__(cls) -> str:
        """Return string representation of stored data."""
        cls.init()
        json_obj = cast(JsonDict, cls.json)
        return json_obj.__repr__()

    @classmethod
    def clean(cls) -> None:
        """Clear all stored values."""
        cls.init()
        json_obj = cast(JsonDict, cls.json)
        json_obj.string = {}
        json_obj.save()

    @classmethod
    def pop(cls, *args: Any) -> Any:
        """Remove and return a stored value."""
        cls.init()
        json_obj = cast(JsonDict, cls.json)
        result = json_obj.pop(*args)
        json_obj.save()
        return result


GIV = GIV()  # type: ignore[assignment, misc]
