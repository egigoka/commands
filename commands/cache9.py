#! python3
# -*- coding: utf-8 -*-
__version__ = "0.1.1"

from .dict9 import imdict


class Cache:
    def __init__(self, func, update_every, args=(), kwargs=imdict(), quiet=True, bench=None):
        from .id9 import ID
        from .bench9 import Bench

        self.counter = ID()
        self.update_every = update_every
        self.bench = bench
        if bench is None:
            self.bench = Bench("cache updated in", quiet=quiet)
        self.stored_output = None
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        if self.counter.get() % self.update_every == 0:
            self.stored_output = self.func(*self.args, **self.kwargs)
            self.bench.end()
        return self.stored_output


class CachedFunction:
    def __init__(self, func, update_every, quiet=True):
        from .id9 import ID
        from .bench9 import Bench

        self.func = func
        self.update_every = update_every
        self.quiet = quiet
        self.caches = {}
        self.counter = ID()
        self.bench = Bench("cache updated in", quiet=quiet)

    def return_value(self, *args, **kwargs):
        try:
            return self.caches[f"{args}{kwargs}"]()
        except KeyError:
            self.caches[f"{args}{kwargs}"] = Cache(func=self.func, update_every=self.update_every,
                                                   args=args, kwargs=kwargs, quiet=self.quiet, bench=self.bench)
            return self.return_value(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.counter.get() % self.update_every == 0:  # flush caches
            self.caches = {}

        return self.return_value(*args, **kwargs)