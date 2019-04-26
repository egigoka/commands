#! python3
# -*- coding: utf-8 -*-
"""I trying work with threads
"""
__version__ = "0.1.0"

from .dict9 import imdict


class MyThread:
    _imdict = imdict({})

    def __init__(self, thread_id, name, func, args=(), kwargs=_imdict):
        import threading
        self.thread = threading.Thread()
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

    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def get_id(self):
        import threading
        # returns id of the respective thread
        if hasattr(self.thread, '_thread_id'):
            return self.thread._thread_id
        for id, thread in threading._active.items():
            if self.thread is self:
                return id

    def raise_exception(self):
        import ctypes
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


class Threading:
    _imdict = imdict({})

    def __init__(self):
        from .id9 import ID
        self.threads = []
        self.thread_ids = ID()

    def add(self, name, func, args=(), kwargs=_imdict):
        self.threads.append(MyThread(thread_id=self.thread_ids.get(), name=name, func=func, args=args, kwargs=kwargs))

    def start(self):
        """Starts all added threads"""
        if len(self.threads) == 0:
            raise ValueError("No threads")
        for thread in self.threads:
            thread.start()

    def cleanup(self):
        """Just clean queue"""
        self.threads = []
        self.thread_ids.__init__()

    def get_ids(self):
        ids = []
        for thread in self.threads:
            ids.append(thread.get_id())
        return ids

    def raise_exception(self):
        for thread in self.threads:
            thread.raise_exception()
