#! python3
# -*- coding: utf-8 -*-
"""I'm trying work with threads
"""
__version__ = "1.7.0"

from .dict9 import ImDict


class IsRunning:
    pass


class MyThread:
    _imdict = ImDict({})

    def __init__(self, func, thread_id=None, name=None, args=(), kwargs=_imdict, daemon=False, quiet=True):
        import threading
        if name is None:
            name = f"Thread {func.__name__}"
            if thread_id is not None:
                name += f".{thread_id}"
        if thread_id is None:
            thread_id = 0
        self.thread = threading.Thread()
        self.thread.daemon = daemon
        self.thread_id = thread_id
        self.thread.name = name
        self.result = IsRunning()
        self.killed = False
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
        import sys
        self.qprint("Starting " + self.thread.name)
        try:
            sys.settrace(self.globaltrace)
            self.result = self.func(*self.args, **self.kwargs)
            self.qprint(f"Finished {self.thread.name}. running: {self.bench.end()}")
        except SystemExit:
            self.qprint(f"Killed {self.thread.name}. running: {self.bench.end()}")

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
            raise

    def is_running(self):
        return self.thread.is_alive()

    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

    raise_exception = kill


class Threading:
    _imdict = ImDict({})

    def __init__(self, daemons=None, verbose=None):
        from .id9 import ID
        self.threads = []
        self.thread_ids = ID()
        self.daemons = daemons
        self.quiet = not verbose

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
            raise

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

    kill = raise_exception

    def get_results(self):
        results = []
        for thread in self.threads:
            results.append(thread.result)
        return results

    def is_running(self):
        cnt = 0
        for thread in self.threads:
            if thread.is_running():
                cnt += 1
        return cnt


class Lock:
    def __call__(self, *args, **kwargs):
        import threading
        return threading.Lock()


Lock = Lock()
