#! python3
# -*- coding: utf-8 -*-
"""I trying work with threads
"""
__version__ = "0.3.0"

from .dict9 import imdict


class MyThread:
    _imdict = imdict({})

    def __init__(self, thread_id, name, func, args=(), kwargs=_imdict, daemon=False):
        import threading
        self.thread = threading.Thread()
        self.thread.daemon = daemon
        self.thread_id = thread_id
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print("Starting " + self.name)
        try:
            self.func(*self.args, **self.kwargs)
        except SystemExit:
            print("Quited " + self.name)

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
            if thread is self.thread:
                return id
        raise RuntimeError("Thread ID not found")

    def raise_exception(self):
        import ctypes
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            raise RuntimeError('Thread Exception raise failure')


class Threading:
    _imdict = imdict({})

    def __init__(self, daemons=None):
        from .id9 import ID
        self.threads = []
        self.thread_ids = ID()
        self.daemons = daemons

    def add(self, name, func, args=(), kwargs=_imdict, daemon=None):
        if daemon is None:
            daemon = self.daemons
        self.threads.append(MyThread(thread_id=self.thread_ids.get(), name=name, func=func, args=args, kwargs=kwargs,
                                     daemon=daemon))

    def start(self, exitable=False):
        if exitable:
            def waiter(self_t):
                import time
                try:
                    while 1:
                        time.sleep(1)  # wait for KeyboardInterrupt
                except (KeyboardInterrupt, SystemExit):
                    self_t.raise_exception()
            self.add("Waiter", waiter, args=(self,), daemon=True)
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
