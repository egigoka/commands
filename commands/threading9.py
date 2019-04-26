#! python3
# -*- coding: utf-8 -*-
"""I trying work with threads
"""
__version__ = "0.0.1"

from .dict9 import imdict


class MyThread:
    _imdict = imdict({})

    def __init__(self, thread_id, name, func, args=(), kwargs=_imdict):
        import threading
        self.thread = threading.Thread()
        print(type(self.thread))
        self.thread_id = thread_id
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print("Starting " + self.name)
        self.func(*self.args, **self.kwargs)
        print("Exiting " + self.name)

    def start(self):
        self.thread.run = self.run
        self.thread.start()


class Threading:
    _imdict = imdict({})

    def __init__(self):
        self.threads = []
        raise NotImplementedError

    def add(self, thread_id, name, func, args=(), kwargs=_imdict):
        self.threads.append(MyThread(thread_id=thread_id, name=name, func=func, args=args, kwargs=kwargs))
        raise NotImplementedError

    def start(self):
        """Starts all added threads"""
        if len(self.threads) == 0:
            raise ValueError("No threads")
        for thread in self.threads:
            thread.start()
        raise NotImplementedError

    def cleanup(self):
        """Just clean queue"""
        self.threads = []
        raise NotImplementedError
