#! python3
# -*- coding: utf-8 -*-
"""I trying work with threads
"""
__version__ = "1.3.2"

from .dict9 import imdict


class MyThread:
    _imdict = imdict({})

    def __init__(self, func, thread_id=None, name=None, args=(), kwargs=_imdict, daemon=False, quiet=True):
        import threading
        if name is None:
            name = f"Thread {func.__name__}.{thread_id}"
        if thread_id is None:
            thread_id = 0
        self.thread = threading.Thread()
        self.thread.daemon = daemon
        self.thread_id = thread_id
        self.thread.name = name
        self.thread.result = None
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.quiet = quiet
        from .bench9 import Bench
        self.bench = Bench(name, quiet=True)

    def qprint(self, *args, **kwargs):
        if not self.quiet:
            from .print9 import Print
            Print(*args, **kwargs)

    def run(self):
        self.qprint("Starting " + self.thread.name)
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.qprint(f"Ended {self.thread.name}. running: {self.bench.end()}")
        except SystemExit:
            self.qprint(f"Quited {self.thread.name}. running: {self.bench.end()}")

    def start(self, wait_for_keyboard_interrupt=False):
        self.thread.run = self.run
        self.thread.start()
        if not self.quiet:
            self.bench.start()
        if wait_for_keyboard_interrupt:
            self.wait_for_keyboard_interrupt()

    def wait_for_keyboard_interrupt(self, quiet=True):
        import time
        try:
            while self.thread.is_alive():
                time.sleep(1)
                if not quiet:
                    from .print9 import Print
                    Print(self.thread.name)
        except (KeyboardInterrupt, SystemExit):
            self.raise_exception()

    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def get_id(self):
        import threading
        # returns id of the respective thread
        if hasattr(self.thread, '_thread_id'):
            return self.thread._thread_id
        for id, thread in threading._active.items():
            if thread is self.thread:
                return id
        self.qprint("Thread ID not found")

    def raise_exception(self):
        import ctypes
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            raise RuntimeError('Thread Exception raise failure')


class Threading:
    _imdict = imdict({})

    def __init__(self, daemons=None, quiet=None):
        from .id9 import ID
        self.threads = []
        self.thread_ids = ID()
        self.daemons = daemons
        self.quiet = quiet

    def add(self, func, name=None, args=(), kwargs=_imdict, daemon=None, quiet=None):
        if daemon is None:
            daemon = self.daemons
        if quiet is None:
            quiet = self.quiet
        self.threads.append(MyThread(thread_id=self.thread_ids.get(), func=func, name=name, args=args, kwargs=kwargs,
                                     daemon=daemon, quiet=quiet))

    def start(self, wait_for_keyboard_interrupt=False, quiet=True):
        """Starts all added threads"""
        assert len(self.threads) != 0, "No threads"

        for thread in self.threads:
            thread.start()

        if wait_for_keyboard_interrupt:
            self.wait_for_keyboard_interrupt(quiet=quiet)

    def wait_for_keyboard_interrupt(self, quiet=True):
        import time
        try:
            while True:
                alive = []  # list of alive threads
                for thread in self.threads:
                    if thread.thread.is_alive():
                        alive.append(thread.thread.name)
                        time.sleep(1)
                if not alive:  # if none of processes alive
                    return
                if not quiet:
                    from .print9 import Print
                    Print("alive:", alive)
        except (KeyboardInterrupt, SystemExit):
                self.raise_exception()

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
