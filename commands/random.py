#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for creating some random values."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import random
    import string
    from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
    from .str import Str

from .module import LazyModule, LazyProperty

__version__ = "0.7.0"
if not TYPE_CHECKING:
    string = LazyModule("string")
    Str = LazyProperty(".str", "Str")
    random = LazyModule("random")


class Random:
    """Class with functions for creating some random values."""

    def __init__(self, seed: Optional[Any] = None) -> None:
        self._rng = random.Random(seed)
        self._string_symbols: Optional[str] = None
        self._seed = seed

    def _integer_instance(self, minimum: int, maximum: int, to_str: bool = False) -> Union[int, str]:
        if maximum < minimum:
            minimum, maximum = maximum, minimum
        result: Union[int, str] = self._rng.randrange(minimum, maximum + 1)
        if to_str:
            result = Str.leftpad(result, len(str(maximum)))
        return result

    def _float_instance(self, minimum: float, maximum: float) -> float:
        return self._rng.uniform(minimum, maximum)

    def _string_instance(self, length: int, string_of_symbols: Optional[str] = None) -> str:
        if length < 0:
            raise ValueError("length must be non-negative")
        if not string_of_symbols:
            if self._string_symbols is None:
                self._string_symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits
            string_of_symbols = self._string_symbols
        return ''.join(self._rng.choices(string_of_symbols, k=length))

    def _item_instance(self, *objects: Any, **kwargs: Any) -> Any:
        objs: Any = objects
        if len(objects) == 1:
            objs = objects[0]
        if kwargs:
            objs = kwargs

        if isinstance(objs, dict):
            return self._rng.choice(list(objs.items()))
        return self._rng.choice(objs)

    def _boolean_instance(self) -> bool:
        return self._rng.random() < 0.5

    def __call__(self, minimum: int = 0, maximum: int = 1, float_mode: bool = False) -> Union[int, float, str]:
        """Shortcut: Random()(a, b) -> int, float_mode=True -> float."""
        if float_mode:
            return self._float_instance(minimum, maximum)
        return self._integer_instance(minimum, maximum)

    class _DualMethod:
        def __init__(self, instance_attr: str, class_attr: str) -> None:
            self._instance_attr = instance_attr
            self._class_attr = class_attr

        def __get__(self, instance: Any, owner: type) -> Any:
            if instance is None:
                return getattr(owner, self._class_attr)
            return getattr(instance, self._instance_attr)

    @classmethod
    def _integer_class(cls, minimum: int, maximum: int, to_str: bool = False) -> Union[int, str]:
        """Return a random integer in a range.

        <br>`param minimum` int, minimum value
        <br>`param maximum` int, maximum value
        <br>`param to_str` bool, if True - return string with len of str(maximum) param
        <br>`return` int|str, random from 'minimum' to 'maximum'
        """
        if maximum < minimum:
            temp = maximum
            maximum = minimum
            minimum = temp

        result: Union[int, str] = random.randrange(minimum, maximum + 1)
        if to_str:
            result = Str.leftpad(result, len(str(maximum)))
        return result

    @classmethod
    def _float_class(cls, minimum: float, maximum: float) -> float:  # return random floating number
        """Return a random float in a range.

        <br>`param minimum` int|float, minimum value
        <br>`param maximum` int|float, maximum value
        <br>`return` float, random from 'minimum' to 'maximum'
        """
        return random.uniform(minimum, maximum)

    @classmethod
    def _string_class(cls, length: int, string_of_symbols: Optional[str] = None) -> str:
        """Build a random string from the provided symbols.

        <br>`param length` int, length of output string
        <br>`param string_of_symbols` string, will be used to create output
        <br>`return` string, with random symbols
        """
        if length < 0:
            raise ValueError("length must be non-negative")
        if not string_of_symbols:
            string_of_symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choices(string_of_symbols, k=length))

    @classmethod
    def _item_class(cls, *objects: Any, **kwargs: Any) -> Any:
        objs: Any = objects
        if len(objects) == 1:
            objs = objects[0]
        if kwargs:
            objs = kwargs

        if isinstance(objs, dict):
            key, value = random.choice(list(objs.items()))
            return key, value
        else:
            return random.choice(objs)

    @classmethod
    def string_unicode(cls, length: int) -> str:
        """Build a random Unicode string.

        <br>`param length` int, length of output string
        <br>`return` string, with random unicode symbols
        """
        # Update this to include code point ranges to be sampled
        include_ranges: List[Tuple[int, int]] = [
            (0x0021, 0x0021),
            (0x0023, 0x0026),
            (0x0028, 0x007E),
            (0x00A1, 0x00AC),
            (0x00AE, 0x00FF),
            (0x0100, 0x017F),
            (0x0180, 0x024F),
            (0x2C60, 0x2C7F),
            (0x16A0, 0x16F0),
            (0x0370, 0x0377),
            (0x037A, 0x037E),
            (0x0384, 0x038A),
            (0x038C, 0x038C)]

        alphabet = [chr(code_point) for current_range in include_ranges
                    for code_point in range(current_range[0], current_range[1] + 1)]
        return ''.join(random.choice(alphabet) for _ in range(length))

    @classmethod
    def _boolean_class(cls) -> bool:
        """Return a random boolean.

        <br>`return` Boolean, random
        """
        return random.random() < 0.5

    @classmethod
    def guid(cls) -> str:
        """Return a random lowercase GUID string.

        <br>`return` string, guid in lowercase
        """
        symbols = cls._string_class(32, string.digits + "abcdef")
        result = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return result

    @classmethod
    def shuffle(cls, list_like_obj: Sequence[str]) -> str:
        """Shuffle a list-like object into a string."""
        _list = list(list_like_obj)
        random.shuffle(_list)
        return ''.join(_list)


Random.integer = Random._DualMethod("_integer_instance", "_integer_class")  # type: ignore[attr-defined]
Random.float = Random._DualMethod("_float_instance", "_float_class")  # type: ignore[attr-defined]
Random.string = Random._DualMethod("_string_instance", "_string_class")  # type: ignore[attr-defined]
Random.item = Random._DualMethod("_item_instance", "_item_class")  # type: ignore[attr-defined]
Random.boolean = Random._DualMethod("_boolean_instance", "_boolean_class")  # type: ignore[attr-defined]
