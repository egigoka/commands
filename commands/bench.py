#! python3
# -*- coding: utf-8 -*-
"""Internal module with Bench class for timing code execution."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import datetime
    from typing import Optional

from .module import LazyModule, LazyProperty

__version__ = "0.7.0"
Print = LazyProperty(".print", "Print")

if not TYPE_CHECKING:
    datetime = LazyModule("datetime")


class Bench:
    """Benchmarking timer for measuring code execution time."""

    def __init__(self, name: str = "", verbose: bool = False) -> None:
        """Initialize a benchmark timer.

        Parameters
        ----------
        name
            Optional name/prefix for this benchmark.
        verbose
            If True, end() will print by default.
        """
        self.name = name
        self.verbose = verbose
        self.time_start: datetime.datetime = datetime.datetime.now()
        self.time_end: Optional[datetime.datetime] = None

    def start(self) -> "Bench":
        """Reset the start time to now."""
        self.time_start = datetime.datetime.now()
        self.time_end = None
        return self

    def get(self) -> float:
        """Get elapsed time in seconds without stopping the timer."""
        now = datetime.datetime.now()
        delta = (now - self.time_start).total_seconds()
        return delta

    def stop(self) -> float:
        """Stop the timer and return elapsed time in seconds."""
        self.time_end = datetime.datetime.now()
        delta = (self.time_end - self.time_start).total_seconds()
        return delta

    def end(self, verbose: Optional[bool] = None, precision: int = 3) -> float:
        """Stop the timer, optionally print result, and return elapsed time.

        Parameters
        ----------
        verbose
            If True, print the elapsed time. Defaults to instance setting.
        precision
            Number of decimal places for display.

        Returns
        -------
        float
            Elapsed time in seconds.
        """
        delta = self.stop()
        if verbose is None:
            verbose = self.verbose
        if verbose:
            self._print_result(delta, precision)
        return delta

    def _print_result(self, delta: float, precision: int) -> None:
        """Print the benchmark result."""
        rounded = round(delta, precision)
        prefix = f"{self.name} " if self.name else "Bench: "
        message = f"{prefix}{rounded} seconds"
        try:
            Print.colored(message, "grey", "on_white")
        except (TypeError, AttributeError, ImportError):
            print(message)

    def __call__(self) -> float:
        """Shortcut for get() - returns elapsed time without stopping."""
        return self.get()

    def __enter__(self) -> "Bench":
        """Context manager entry - starts the timer."""
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit - stops the timer."""
        self.stop()

    def __repr__(self) -> str:
        elapsed = self.get()
        state = "running" if self.time_end is None else "stopped"
        return f"Bench(name={self.name!r}, elapsed={elapsed:.3f}s, {state})"
