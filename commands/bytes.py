#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with bytes."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Union

from .module import LazyModule

__version__ = "0.0.2"

chardet = LazyModule("chardet")


class Bytes:
    """Helpers for working with byte data."""

    def __init__(self, data: Optional[bytes] = None) -> None:
        self.data = data

    def _ensure(self) -> None:
        if self.data is None:
            raise ValueError("Bytes data is not set")

    def __getattribute__(self, name: str) -> Any:
        """Proxy selected methods to the stored byte data."""
        if name in {"get_encoding", "to_string"}:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                self._ensure()
                method: Callable[..., Any] = object.__getattribute__(self.__class__, name).__get__(self, self.__class__)
                return method(self.data, *args, **kwargs)
            return _wrapper
        return object.__getattribute__(self, name)

    @classmethod
    def get_encoding(cls, slice_of_raw_data: bytes) -> Optional[str]:
        """Detect encoding for a slice of raw bytes."""
        # check for utf-16-le
        fail_symbols = 0
        for cnt, sym in enumerate(slice_of_raw_data):
            if cnt % 2 != 0:
                if sym != 0:
                    fail_symbols += 1
        utf_16_le = False
        if len(slice_of_raw_data) == 0:
            pass
        elif fail_symbols / (len(slice_of_raw_data) / 2) < 0.2:
            utf_16_le = True
        encoding: Optional[str]
        if utf_16_le:
            encoding = "utf-16-le"
        # end check for utf-16-le
        else:
            encoding = chardet.detect(slice_of_raw_data)["encoding"]
        return encoding

    @classmethod
    def to_string(cls, slice_of_raw_data: Union[bytes, str]) -> str:
        """Decode bytes to a string using detected encoding."""
        if isinstance(slice_of_raw_data, str):
            return slice_of_raw_data
        enc = cls.get_encoding(slice_of_raw_data)
        return slice_of_raw_data.decode(encoding=enc if enc else "utf-8")
