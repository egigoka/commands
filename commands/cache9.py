#! python3
# -*- coding: utf-8 -*-

__version__ = "0.0.3"

from .dict9 import imdict


class Cache:
    def __init__(self, func, update_every, args=(), kwargs=imdict(), quiet=True):
        from .id9 import ID
        from .bench9 import Bench

        self.called = False
        self.counter = ID()
        self.update_every = update_every
        self.bench = Bench("cache updated in", quiet=quiet)
        self.stored_output = None
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        if (self.counter.get() % self.update_every == 0) or not self.called:
            self.called = True
            self.stored_output = self.func(*self.args, **self.kwargs)
        return self.stored_output


class CachedFunction:
    def __init__(self, func, update_every, quiet=True):
        self.func = func
        self.update_every = update_every
        self.quiet = quiet
        self.caches = {}

    def __call__(self, *args, **kwargs):
        try:
            return self.caches[f"{args}{kwargs}"]()
        except KeyError:
            self.caches[f"{args}{kwargs}"] = Cache(func=self.func, update_every=self.update_every,
                                                   args=args, kwargs=kwargs, quiet=self.quiet)
            return self.__call__(*args, **kwargs)