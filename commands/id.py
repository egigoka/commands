#! python3
# -*- coding: utf-8 -*-
"""Internal module to create counters."""
__version__ = "0.0.1"


class ID:
    """Simple incrementing counter."""

    def __init__(self) -> None:
        self.cnt: int = -1

    def get(self) -> int:
        """Return the next counter value."""
        self.cnt += 1
        return self.cnt

    def __call__(self) -> int:
        """Return the next counter value."""
        return self.get()
