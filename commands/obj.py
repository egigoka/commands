#! python3
# -*- coding: utf-8 -*-
"""Internal module for object utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Type

__version__ = "0.0.1"


class Obj:
    """Object casting helpers."""

    @classmethod
    def cast_to(cls, obj: Any, cast_to: List[Type[Any]]) -> Any:
        """Cast a value to the first compatible type."""
        for type_to in cast_to:
            try:
                return type_to(obj)
            except Exception:
                pass
        return obj

    def __init__(self, obj: Optional[Any] = None) -> None:
        self.obj = obj

    def cast(self, cast_to: List[Type[Any]]) -> Any:
        """Cast the stored value to the first compatible type."""
        return self.__class__.cast_to(self.obj, cast_to)
