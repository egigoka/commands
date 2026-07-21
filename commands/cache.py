#! python3
# -*- coding: utf-8 -*-
"""Simple caching helpers for function calls."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Mapping, Optional, Tuple


__version__ = "0.1.3"
ImDict = LazyProperty(".dict", "ImDict")
ID = LazyProperty(".id", "ID")
Bench = LazyProperty(".bench", "Bench")
Lock = LazyProperty(".threading", "Lock")



class Cache:
    """Cache wrapper with periodic refresh."""

    def __init__(
        self,
        func: Callable[..., Any],
        update_every: int,
        args: Tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = ImDict(),
        verbose: bool = False,
        bench: Optional[Any] = None
    ) -> None:

        self.counter = ID()
        self.lock = Lock()

        self.update_every = update_every

        self.bench: Any = bench
        if bench is None:
            self.bench = Bench("cache updated in", verbose=verbose)

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.stored_output: Any = None

    def __call__(self) -> Any:
        """Return cached value."""
        return self.value()

    def value(self) -> Any:
        """Return cached value, updating if needed."""
        with self.lock:
            if self.counter.get() % self.update_every == 0:
                self.run()
            try:
                return self.stored_output
            except AttributeError:
                self.run()
                return self.stored_output

    def run(self) -> None:
        """Recompute and store the cached value."""
        self.stored_output = self.func(*self.args, **self.kwargs)
        self.bench.end()


class CachedFunction:
    """Callable that caches per-argument results."""

    def __init__(self, func: Callable[..., Any], update_every: int, verbose: bool = False) -> None:

        self.func = func
        self.update_every = update_every
        self.verbose = verbose

        self.caches: Dict[str, Cache] = {}
        self.counter = ID()
        self.bench = Bench("cache updated in", verbose=verbose)
        self.lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Return cached value for provided arguments."""
        return self.value(*args, **kwargs)

    def return_value(self, *args: Any, **kwargs: Any) -> Any:
        """Get or create a cache entry for provided arguments."""
        try:
            return self.caches[f"{args}{kwargs}"]()
        except KeyError:
            self.caches[f"{args}{kwargs}"] = Cache(func=self.func, update_every=self.update_every,
                                                   args=args, kwargs=ImDict(kwargs), verbose=self.verbose, bench=self.bench)
            return self.return_value(*args, **kwargs)

    def value(self, *args: Any, **kwargs: Any) -> Any:
        """Return cached value, refreshing caches when needed."""
        with self.lock:
            if self.counter.get() % self.update_every == 0:  # flush caches
                self.caches = {}

            return self.return_value(*args, **kwargs)
