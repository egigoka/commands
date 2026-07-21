#! python3
# -*- coding: utf-8 -*-
"""Helpers for working with threads."""
from __future__ import annotations

from typing import TYPE_CHECKING
from .module import LazyModule, LazyProperty

__version__ = "1.10.1"

if TYPE_CHECKING:
    import ctypes
    import sys
    import threading
    from typing import Any, Callable, Dict as DictType, List, Mapping, Optional, Protocol, Tuple, Union
    from .bench import Bench
    from .id import ID
    from .print import Print

    class Dict(Protocol):
        """Typing protocol for dictionary helpers."""

        @classmethod
        def sorted_by_key(cls, dictionary: Mapping[Any, Any]) -> DictType[Any, Any]:
            """Return dictionary sorted by key."""
            ...

    class ImDict(dict[Any, Any]):
        """Typing placeholder for immutable dictionaries."""

else:
    ctypes = LazyModule("ctypes")
    sys = LazyModule("sys")
    ImDict = LazyProperty(".dict", "ImDict")
    ID = LazyProperty(".id", "ID")
    Bench = LazyProperty(".bench", "Bench")
    Print = LazyProperty(".print", "Print")
    Dict = LazyProperty(".dict", "Dict")
    threading = LazyModule("threading")



class IsRunning:
    """Marker object for running thread state."""

    pass


class MyThread:
    """Thread wrapper with optional tracing and result capture."""

    _imdict: Mapping[str, Any] = ImDict({})

    def __init__(
        self,
        func: Callable[..., Any],
        thread_id: Optional[int] = None,
        name: Optional[str] = None,
        args: Tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = _imdict,
        daemon: bool = False,
        verbose: bool = False
    ) -> None:
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
        self.result: Any = IsRunning()
        self.killed = False
        self._async_kill_requested = False
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.verbose = verbose
        self.bench = Bench(name, verbose=False)

    def qprint(self, *args: Any, **kwargs: Any) -> None:
        """Print only when verbose is enabled."""
        if self.verbose:
            Print(*args, **kwargs)

    def _make_chained_trace(self, previous_trace: Any) -> Callable[..., Any]:
        stop_requested = False

        def chained_trace(frame: Any, event: str, arg: Any) -> Callable[..., Any]:
            nonlocal stop_requested
            if self.killed and not self._async_kill_requested and not stop_requested:
                stop_requested = True
                raise SystemExit()
            if previous_trace is not None:
                previous_trace(frame, event, arg)
            return chained_trace

        return chained_trace

    def run(self) -> None:
        """Run the thread target with tracing and result capture."""
        self.qprint("Starting " + self.thread.name)
        if self.killed:
            self.qprint(f"Killed {self.thread.name}")
            return
        previous_trace: Any = None
        try:
            if sys.version_info >= (3, 9):
                previous_trace = sys.gettrace()
                sys.settrace(self._make_chained_trace(previous_trace))
            self.result = self.func(*self.args, **self.kwargs)
            self.qprint(f"Finished {self.thread.name}. running: {self.bench.end()}")
        except SystemExit:
            self.qprint(f"Killed {self.thread.name}. running: {self.bench.end()}")
        finally:
            if sys.version_info >= (3, 9):
                sys.settrace(previous_trace)

    def start(self, wait_for_keyboard_interrupt: bool = False) -> None:
        """Start the thread and optionally block on interrupt."""
        self.thread.run = self.run  # type: ignore[method-assign]
        self.thread.start()
        if self.verbose:
            self.bench.start()
        if wait_for_keyboard_interrupt:
            self.wait_for_keyboard_interrupt()

    def __call__(self, wait_for_keyboard_interrupt: bool = False) -> "MyThread":
        """Start thread and optionally wait."""
        self.start(wait_for_keyboard_interrupt=wait_for_keyboard_interrupt)
        return self

    def wait_for_keyboard_interrupt(self, verbose: bool = False) -> None:
        """Join the thread and propagate keyboard interrupts."""
        try:
            self.thread.join()
        except (KeyboardInterrupt, SystemExit):
            self.raise_exception()
            raise

    def is_running(self) -> bool:
        """Return True if the thread is alive."""
        return self.thread.is_alive()

    # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    def globaltrace(self, frame: Any, event: str, arg: Any) -> Optional[Callable[..., Any]]:
        """Trace function to hook calls for kill support."""
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame: Any, event: str, arg: Any) -> Callable[..., Any]:
        """Trace function to exit when killed."""
        if self.killed:
            raise SystemExit()
        return self.localtrace

    def kill(self) -> None:
        """Request thread termination."""
        self._async_kill_requested = sys.version_info < (3, 9) and self.thread.is_alive()
        self.killed = True
        if not self._async_kill_requested:
            return

        thread_id = self.thread.ident
        if thread_id is None:
            return
        result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread_id), ctypes.py_object(SystemExit)
        )
        if result > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_id), None)
            raise SystemError("failed to stop thread cleanly")

    raise_exception = kill


class Threading:
    """Thread pool helper with simple scheduling."""

    _imdict: Mapping[str, Any] = ImDict({})

    def __init__(
        self,
        daemons: Optional[bool] = None,
        verbose: Optional[bool] = None,
        max_threads: int = 0,
        start_from_first: bool = False
    ) -> None:
        self.input_threads: List[MyThread] = []
        self.running_now_threads: List[MyThread] = []
        self.finished_threads: List[MyThread] = []
        self.runner_threads: List[MyThread] = []
        self.thread_ids = ID()
        self.daemons = daemons
        self.verbose = verbose
        self.max_threads = max_threads
        self.thread_pop_lock = Lock()
        self.thread_move_lock = Lock()
        self.start_from_first = start_from_first
        self.results: DictType[int, Any] = {}

    def __call__(self, wait_for_keyboard_interrupt: bool = False, verbose: bool = False) -> "Threading":
        """Start added threads with a short call."""
        self.start(wait_for_keyboard_interrupt=wait_for_keyboard_interrupt, verbose=verbose)
        return self

    def add(
        self,
        func: Callable[..., Any],
        name: Optional[str] = None,
        args: Tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = _imdict,
        daemon: Optional[bool] = None,
        verbose: Optional[bool] = None
    ) -> None:
        """Add a thread job to the queue."""
        if daemon is None:
            daemon = self.daemons
        if verbose is None:
            verbose = self.verbose
        self.input_threads.append(MyThread(thread_id=self.thread_ids.get(), func=func, name=name, args=args,
                                           kwargs=kwargs, daemon=daemon if daemon else False, verbose=verbose if verbose else False))

    def runner(self, runner_no: int) -> None:
        """Run queued threads until the queue is empty."""
        if self.verbose:
            print(f"Started runner #{runner_no}")
        while True:
            with self.thread_pop_lock:
                cnt_of_threads = len(self.input_threads)
                if not cnt_of_threads:
                    if self.verbose:
                        print(f"Finished runner #{runner_no}")
                    return
                thread = self.input_threads.pop()
            with self.thread_move_lock:
                self.running_now_threads.append(thread)
            self.results[thread.thread_id] = IsRunning()
            thread.start(wait_for_keyboard_interrupt=True)
            self.results[thread.thread_id] = thread.result
            with self.thread_move_lock:
                self.finished_threads.append(self.running_now_threads[self.running_now_threads.index(thread)])


    def start(self, wait_for_keyboard_interrupt: bool = False, verbose: bool = False) -> None:
        """Start all added threads."""
        assert len(self.input_threads) != 0, "No threads"

        max_threads = self.max_threads
        if max_threads == 0:
            max_threads = len(self.input_threads)

        if self.start_from_first:
            self.input_threads.reverse()

        for i in range(1, max_threads + 1):
            t = MyThread(self.runner, name=f"runner.{i}", kwargs=ImDict({"runner_no": i}))
            self.runner_threads.append(t)
            t.start()

        if wait_for_keyboard_interrupt:
            self.wait_for_keyboard_interrupt(verbose=verbose)

    def wait_for_keyboard_interrupt(self, verbose: bool = False) -> None:
        """Wait for all runners and handle interrupts."""
        try:
            for t in self.runner_threads:
                t.wait_for_keyboard_interrupt()

        except (KeyboardInterrupt, SystemExit):
            self.raise_exception()
            raise

    def cleanup(self) -> None:
        """Clean the thread queue."""
        self.input_threads = []
        self.runner_threads = []
        self.thread_ids = ID()

    def get_ids(self) -> List[int]:
        """Return thread IDs from the input queue."""
        ids: List[int] = []
        for thread in self.input_threads:
            ids.append(thread.thread_id)
        return ids

    def raise_exception(self) -> None:
        """Raise a stop signal on all queued and active threads."""
        for thread in self.input_threads:
            thread.raise_exception()
        for thread in self.running_now_threads:
            thread.raise_exception()

    kill = raise_exception

    def get_results(self) -> Any:
        """Return results for completed threads."""
        results = Dict.sorted_by_key(self.results)
        return results.values()

    def is_running(self) -> int:
        """Count running threads in the input queue."""
        cnt = 0
        for thread in self.input_threads:
            if thread.is_running():
                cnt += 1
        return cnt

    def total_input_threads(self) -> int:
        """Return the total number of queued input threads."""
        return len(self.input_threads)

    def running_threads(self) -> int:
        """Return the number of active runner and queued threads."""
        running = 0
        for runner in self.runner_threads:
            if runner.is_running():
                running += 1
        running += len(self.input_threads)
        return running


Lock = threading.Lock
