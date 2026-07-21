#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with audio."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

from .module import LazyModule

__version__ = "0.0.1"

mutagen = LazyModule("mutagen")


class Audio:
    """Class to work with audio."""

    def __init__(self, path: str) -> None:
        if not path:
            raise ValueError("Audio path is not set")
        self.path = path

    def mutagen_handle(self) -> Any:
        """Return mutagen handle for the current path."""
        assert self.path is not None
        mutagen_file = getattr(mutagen, "File")
        return mutagen_file(self.path)

    def bitrate(self) -> int:
        """Return the audio bitrate for the current path."""
        handle = self.mutagen_handle()
        return handle.info.bitrate  # type: ignore[no-any-return]
