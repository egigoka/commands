#! python3
# -*- coding: utf-8 -*-
"""I'm trying work with threads
"""
__version__ = "1.9.0"

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
        self.bench = Bench(name, verbose=False)

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

    def __init__(self, daemons=None, verbose=None, max_threads=0, start_from_first=False):
        from .id9 import ID
        self.input_threads = []
        self.runner_threads = []
        self.thread_ids = ID()
        self.daemons = daemons
        self.quiet = not verbose
        self.max_threads = max_threads
        self.thread_pop_lock = Lock()
        self.start_from_first = start_from_first
        self.results = {}

    def add(self, func, name=None, args=(), kwargs=_imdict, daemon=None, quiet=None):
        if daemon is None:
            daemon = self.daemons
        if quiet is None:
            quiet = self.quiet
        self.input_threads.append(MyThread(thread_id=self.thread_ids.get(), func=func, name=name, args=args,
                                           kwargs=kwargs, daemon=daemon, quiet=quiet))

    def runner(self, runner_no):
        if not self.quiet:
            print(f"Started runner #{runner_no}")
        while True:
            with self.thread_pop_lock:
                cnt_of_threads = len(self.input_threads)
                if not cnt_of_threads:
                    if not self.quiet:
                        print(f"Finished runner #{runner_no}")
                    return
                thread = self.input_threads.pop()
            self.results[thread.thread_id] = IsRunning()
            thread.start(wait_for_keyboard_interrupt=True)
            self.results[thread.thread_id] = thread.result


    def start(self, wait_for_keyboard_interrupt=False, quiet=True):
        """Starts all added threads"""
        assert len(self.input_threads) != 0, "No threads"

        max_threads = self.max_threads
        if max_threads == 0:
            max_threads = len(self.input_threads)

        if self.start_from_first:
            self.input_threads.reverse()

        for i in range(1, max_threads + 1):
            t = MyThread(self.runner, name=f"runner_{i}", kwargs=ImDict({"runner_no": i}))
            self.runner_threads.append(t)
            t.start()

        if wait_for_keyboard_interrupt:
            self.wait_for_keyboard_interrupt(quiet=quiet)

    def wait_for_keyboard_interrupt(self, quiet=True):
        import time
        try:
            while True:
                alive = []  # list of alive threads
                for thread in self.runner_threads:
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
        self.input_threads = []
        self.runner_threads = []
        self.thread_ids.__init__()

    def get_ids(self):
        ids = []
        for thread in self.input_threads:
            ids.append(thread.get_id())
        return ids

    def raise_exception(self):
        for thread in self.runner_threads:
            thread.raise_exception()
        for thread in self.input_threads:
            thread.raise_exception()

    kill = raise_exception

    def get_results(self):
        from .dict9 import Dict
        results = Dict.sorted_by_key(self.results)
        return results.values()

    def is_running(self):
        cnt = 0
        for thread in self.input_threads:
            if thread.is_running():
                cnt += 1
        return cnt

    def total_input_threads(self):
        return len(self.input_threads)

    def running_threads(self):
        running = 0
        for runner in self.runner_threads:
            if runner.is_running():
                running += 1
        running += len(self.input_threads)
        return running

class Lock:
    def __call__(self, *args, **kwargs):
        import threading
        return threading.Lock()


Lock = Lock()
