#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import base64
    from typing import Optional, Union

__version__ = "2.0.1"
if not TYPE_CHECKING:
    base64 = LazyModule("base64")
File = LazyProperty(".file", "File")


class Base64:
    """Class to work with base64."""

    def __init__(self, data: Optional[Union[str, bytes, bytearray]] = None, filename: Optional[str] = None) -> None:
        self.data = data
        self.filename = filename

    def _ensure_data(self) -> None:
        if self.data is None:
            raise ValueError("Base64 data is not set")

    def _ensure_filename(self) -> None:
        if not self.filename:
            raise ValueError("Filename is not set")

    def to_bytes(self) -> bytes:
        """Decode stored base64 data into bytes."""
        self._ensure_data()
        input_ = self.data
        assert input_ is not None
        if isinstance(input_, str):
            return base64.decodebytes(input_.encode('ascii'))
        if isinstance(input_, bytearray):
            return base64.decodebytes(bytes(input_))
        return base64.decodebytes(input_)

    def from_bytes(self) -> bytes:
        """Encode stored data into base64 bytes."""
        self._ensure_data()
        raw = self.data
        assert raw is not None
        if isinstance(raw, str):
            raw_bytes = raw.encode("utf-8")
        elif isinstance(raw, bytearray):
            raw_bytes = bytes(raw)
        else:
            raw_bytes = raw
        encoded = base64.encodebytes(raw_bytes)
        self.data = encoded
        return encoded

    def to_file(self) -> None:
        """Decode stored base64 data and write bytes to a file."""
        self._ensure_data()
        self._ensure_filename()
        assert self.filename is not None
        file_bytes = self.to_bytes()
        File.write(self.filename, file_bytes, mode="wb")

    def from_file(self) -> bytes:
        """Read a file and return its base64-encoded bytes."""
        self._ensure_filename()
        assert self.filename is not None
        with open(self.filename, mode="rb") as file:
            file_bytes = file.read()
        self.data = file_bytes
        return self.from_bytes()
