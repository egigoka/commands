#! python3
# -*- coding: utf-8 -*-
__version__ = "0.1.3"

from .dict9 import ImDict


class Cache:
    def __init__(self, func, update_every, args=(), kwargs=ImDict(), quiet=True, bench=None):
        from .id9 import ID
        from .bench9 import Bench
        from .threading9 import Lock

        self.counter = ID()
        self.lock = Lock()

        self.update_every = update_every

        self.bench = bench
        if bench is None:
            self.bench = Bench("cache updated in", verbose=not quiet)

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.stored_output = None

    def run(self):
        self.stored_output = self.func(*self.args, **self.kwargs)
        self.bench.end()

    def __call__(self):
        with self.lock:
            if self.counter.get() % self.update_every == 0:
                self.run()
            try:
                return self.stored_output
            except AttributeError:
                self.run()
                return self.stored_output


class CachedFunction:
    def __init__(self, func, update_every, quiet=True):
        from .id9 import ID
        from .bench9 import Bench
        from .threading9 import Lock

        self.func = func
        self.update_every = update_every
        self.quiet = quiet

        self.caches = {}
        self.counter = ID()
        self.bench = Bench("cache updated in", verbose=not quiet)
        self.lock = Lock()

    def return_value(self, *args, **kwargs):
        try:
            return self.caches[f"{args}{kwargs}"]()
        except KeyError:
            self.caches[f"{args}{kwargs}"] = Cache(func=self.func, update_every=self.update_every,
                                                   args=args, kwargs=ImDict(kwargs), quiet=self.quiet, bench=self.bench)
            return self.return_value(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        with self.lock:
            if self.counter.get() % self.update_every == 0:  # flush caches
                self.caches = {}

            return self.return_value(*args, **kwargs)
