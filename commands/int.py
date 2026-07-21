#! python3
# -*- coding: utf-8 -*-
"""Internal module, import it like "from commands.int8 import Int"."""
from __future__ import annotations
import builtins
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional, Union

__version__ = "0.0.5"
Str = LazyProperty(".str", "Str")


class Int:  # pylint: disable=too-few-public-methods
    """Methods to interact with integers."""

    def __init__(self, start: Optional[int] = None, end: Optional[int] = None) -> None:
        self.start = start
        self.end = end

    def _ensure(self) -> None:
        if self.start is None or self.end is None:
            raise ValueError("Both start and end must be set for Int instance")

    def range(self, to_str: bool = False) -> Union[List[str], builtins.range]:
        """Return a range or list of formatted integers for the instance."""
        self._ensure()
        assert self.start is not None and self.end is not None
        return self.__class__.from_to(self.start, self.end, to_str=to_str)

    @classmethod
    def from_to(cls, start: int, end: int, to_str: bool = False) -> Union[List[str], builtins.range]:
        """Return a list/range of integers.

        Return list of integers, if argument
        "to_str" activated, return list of strings with equal length
        if "list" arg activated, list will be returned, otherwise, it will be iterable obj
        """
        roots = builtins.range(start, end + 1)
        if to_str:
            output: List[str] = []
            max_len = max(len(str(start)), len(str(end)))
            for root in roots:
                if root < 0:
                    output.append("-" + Str.leftpad(-root, max_len - 1, 0))
                else:
                    output.append(Str.leftpad(root, max_len, 0))
            return output
        return roots
