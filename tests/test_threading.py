# Consolidated tests for commands/threading.py (unit)

# ---- from test_threading9.py ----


import pytest
from commands.threading import MyThread, Threading


def test_mythread_callable_runs(monkeypatch):
    ran = {"done": False}

    def func():
        ran["done"] = True

    t = MyThread(func, name="t1")
    t(wait_for_keyboard_interrupt=False)
    t.thread.join()
    assert ran["done"]


def test_mythread_kill_sets_flag():
    t = MyThread(lambda: None, name="t2")
    t.kill()
    assert t.killed is True


def test_threading_callable_starts(monkeypatch):
    ran = {"count": 0}

    def func():
        ran["count"] += 1

    pool = Threading(max_threads=1)
    pool.add(func)
    pool(wait_for_keyboard_interrupt=False)
    pool.wait_for_keyboard_interrupt()
    assert ran["count"] == 1


def test_threading_add_defaults():
    pool = Threading()
    pool.add(lambda: None)
    assert pool.total_input_threads() == 1


# ---- from test_threading_comprehensive.py ----


import pytest
import time
from threading import Event
from unittest.mock import patch, Mock, MagicMock
from commands.threading import MyThread, Threading, IsRunning


class TestMyThreadComprehensive:
    """Comprehensive tests for MyThread class"""

    def test_qprint_verbose_true(self):
        """Test qprint with verbose=True to cover lines 40-41"""
        def simple_func():
            return "done"

        thread = MyThread(simple_func, verbose=True)

        with patch('commands.print.Print') as mock_print:
            thread.qprint("Test message")
            # Print should be called when verbose=True
            assert mock_print.called

    def test_qprint_verbose_false(self):
        """Test qprint with verbose=False"""
        def simple_func():
            return "done"

        thread = MyThread(simple_func, verbose=False)

        with patch('commands.print.Print') as mock_print:
            thread.qprint("Test message")
            # Print should not be called when verbose=False
            assert not mock_print.called


    def test_start_verbose_true(self):
        """Test start with verbose=True to cover line 57"""
        def quick_func():
            time.sleep(0.05)
            return "result"

        thread = MyThread(quick_func, verbose=True)
        thread.bench.start = Mock(wraps=thread.bench.start)
        thread.start()
        thread.thread.join(timeout=2)

        thread.bench.start.assert_called_once_with()

    def test_is_running(self):
        """Test is_running method to cover line 80"""
        release = Event()

        def slow_func():
            release.wait(timeout=1)
            return "result"

        thread = MyThread(slow_func)
        thread.start()
        assert thread.is_running()

        release.set()
        thread.thread.join(timeout=1)
        assert not thread.is_running()

    def test_globaltrace_and_localtrace(self):
        """Test globaltrace and localtrace to cover lines 84-92"""
        def simple_func():
            x = 1 + 1
            return "result"

        thread = MyThread(simple_func)

        # Test globaltrace with 'line' event (not 'call')
        result = thread.globaltrace(None, 'line', None)
        assert result is None

        # Test with 'call' event
        result = thread.globaltrace(None, 'call', None)
        assert result == thread.localtrace

        # Test localtrace when not killed
        result = thread.localtrace(None, 'line', None)
        assert result == thread.localtrace

        # Test localtrace when killed
        thread.killed = True
        with pytest.raises(SystemExit):
            thread.localtrace(None, 'line', None)


class TestThreadingComprehensive:
    """Comprehensive tests for Threading class"""

    def test_runner_verbose_true(self):
        """Test runner with verbose=True to cover line 133 and 139"""
        import sys
        from io import StringIO

        threading_obj = Threading(verbose=True)

        def simple_func():
            return "result"

        threading_obj.add(simple_func)

        # Capture stdout
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            # This will print "Started runner" and "Finished runner"
            threading_obj.runner(1)
        finally:
            sys.stdout = old_stdout

        output = captured_output.getvalue()
        assert 'Started runner #1' in output
        assert 'Finished runner #1' in output

    def test_start_max_threads_zero(self):
        """Test start with max_threads=0 to cover line 157"""
        threading_obj = Threading(max_threads=0)

        def quick_func():
            time.sleep(0.01)
            return "result"

        # Add multiple threads
        threading_obj.add(quick_func)
        threading_obj.add(quick_func)
        threading_obj.add(quick_func)

        # When max_threads=0, it should use len(input_threads)
        threading_obj.start()

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=3)

        # Should have created 3 runner threads (one for each input thread)
        assert len(threading_obj.runner_threads) == 3

    def test_get_ids(self):
        """Test get_ids method to cover lines 199-202"""
        threading_obj = Threading()

        def simple_func():
            return "result"

        # Add threads
        threading_obj.add(simple_func)
        threading_obj.add(simple_func)
        threading_obj.add(simple_func)

        ids = threading_obj.get_ids()
        assert ids == [0, 1, 2]

    def test_raise_exception(self):
        """Test raise_exception method to cover lines 205-208"""
        threading_obj = Threading()

        def slow_func():
            time.sleep(1)
            return "result"

        # Add threads but don't start them yet
        threading_obj.add(slow_func)
        threading_obj.add(slow_func)
        threading_obj.add(slow_func)

        # Start threads
        threading_obj.start()

        # Give threads a moment to start
        time.sleep(0.1)

        # Call raise_exception to kill all threads
        threading_obj.raise_exception()

        # All runner threads should have killed flag set
        for runner in threading_obj.runner_threads:
            assert runner.killed

        # All input threads should have killed flag set
        for thread in threading_obj.input_threads:
            assert thread.killed

        # Wait a bit for cleanup
        time.sleep(0.2)

    def test_get_results(self):
        """Test get_results method to cover lines 213-215"""
        threading_obj = Threading()

        def func1():
            return "result1"

        def func2():
            return "result2"

        threading_obj.add(func1)
        threading_obj.add(func2)
        threading_obj.start()

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)

        results = threading_obj.get_results()
        # Results should be a dict_values object
        results_list = list(results)
        assert len(results_list) == 2

    def test_is_running(self):
        """Test is_running method to cover lines 218-222"""
        threading_obj = Threading()

        def slow_func():
            time.sleep(0.3)
            return "result"

        def quick_func():
            return "result"

        threading_obj.add(slow_func)
        threading_obj.add(quick_func)

        # Before start
        running_count = threading_obj.is_running()
        assert running_count == 0

        # Mock is_running on threads to return True
        for thread in threading_obj.input_threads:
            thread.is_running = Mock(return_value=True)

        running_count = threading_obj.is_running()
        assert running_count == 2

    def test_running_threads(self):
        """Test running_threads method to cover lines 228-233"""
        threading_obj = Threading()
        threading_obj.runner_threads = [
            Mock(is_running=Mock(return_value=True)),
            Mock(is_running=Mock(return_value=False)),
        ]
        threading_obj.input_threads = [Mock(), Mock()]

        assert threading_obj.running_threads() == 3


class TestThreadingCallable:
    """Test Threading __call__ method"""

    def test_threading_call(self):
        """Test Threading __call__ shortcut"""
        threading_obj = Threading()

        def quick_func():
            return "result"

        threading_obj.add(quick_func)

        # Use __call__ to start
        result = threading_obj()

        assert result is threading_obj

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)


class TestMyThreadCallable:
    """Test MyThread __call__ method"""

    def test_mythread_call(self):
        """Test MyThread __call__ shortcut"""
        def quick_func():
            return "result"

        thread = MyThread(quick_func)

        # Use __call__ to start
        result = thread()

        assert result is thread

        # Wait for completion
        thread.thread.join(timeout=1)


class TestThreadingStartFromFirst:
    """Test Threading with start_from_first option"""

    def test_start_from_first_true(self):
        """Test start with start_from_first=True"""
        threading_obj = Threading(max_threads=1, start_from_first=True)

        results_order = []

        def func1():
            results_order.append(1)
            return "result1"

        def func2():
            results_order.append(2)
            return "result2"

        def func3():
            results_order.append(3)
            return "result3"

        # Add in order 1, 2, 3
        threading_obj.add(func1)
        threading_obj.add(func2)
        threading_obj.add(func3)

        threading_obj.start()

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)

        assert results_order == [1, 2, 3]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_threading_extra.py ----


import pytest

from commands.threading import Threading, MyThread, IsRunning




def test_threading_runner_flow(monkeypatch):
    calls = []

    def dummy_func(runner_no=None):
        calls.append(runner_no)
        return runner_no

    # Preload input threads
    th = Threading(max_threads=1, start_from_first=True, verbose=False)
    th.add(dummy_func, kwargs={"runner_no": 1})
    th.add(dummy_func, kwargs={"runner_no": 2})

    # Replace MyThread with a synchronous mock to avoid real threads
    class DummyMyThread:
        def __init__(self, func, thread_id=None, name=None, args=(), kwargs=None, daemon=False, verbose=False):
            self.func = func
            self.kwargs = kwargs or {}
            self.thread_id = thread_id or 0
            self.thread = type("T", (), {"is_alive": lambda self: False})()
            self.result = IsRunning()

        def start(self, wait_for_keyboard_interrupt=False):
            self.result = self.func(**self.kwargs)

        def wait_for_keyboard_interrupt(self, verbose=False):
            return

    monkeypatch.setattr("commands.threading.MyThread", DummyMyThread)

    th.start(wait_for_keyboard_interrupt=True)
    assert calls == [1, 2]
    # results recorded
    assert th.results




# ---- from test_threading_trace_and_sync.py ----


import pytest

from commands.threading import MyThread, Threading, IsRunning


def test_mythread_run_restores_trace_and_sets_result(monkeypatch):
    called = []

    def task():
        called.append("ok")
        return 123

    t = MyThread(task, verbose=False)
    t.run()

    assert called == ["ok"]
    assert t.result == 123


def test_mythread_run_chains_existing_trace_and_restores_it():
    import sys

    trace_calls = {"cnt": 0}

    def previous_trace(_frame, _event, _arg):
        trace_calls["cnt"] += 1
        return previous_trace

    def task():
        return "ok"

    t = MyThread(task, verbose=False)
    chained = t._make_chained_trace(previous_trace)
    assert chained(None, "line", None) is chained
    assert trace_calls["cnt"] > 0
    t.killed = True
    with pytest.raises(SystemExit):
        chained(None, "line", None)
    t.killed = False

    old_trace = sys.gettrace()
    sys.settrace(previous_trace)
    try:
        t.run()
        assert t.result == "ok"
        assert sys.gettrace() is previous_trace
    finally:
        sys.settrace(old_trace)




def test_threading_runner_executes_tasks_in_main_thread(monkeypatch):
    # Avoid real threads; make MyThread.start execute synchronously.
    def sync_start(self, wait_for_keyboard_interrupt=False):
        self.run()
        return None

    monkeypatch.setattr(MyThread, "start", sync_start)

    results = []

    def task(n):
        results.append(n)
        return n * 2

    runner = Threading(max_threads=1, start_from_first=True)
    runner.add(task, kwargs={"n": 1})
    runner.add(task, kwargs={"n": 2})

    # Threading.start() applies this when start_from_first=True; runner() pops from the end.
    runner.input_threads.reverse()
    runner.runner(1)

    assert results == [1, 2]
    out = list(runner.get_results())
    assert out == [2, 4]
    assert isinstance(runner.results[0], (IsRunning, int))






# ---- from test_threading_wait_cleanup.py ----


import pytest

from commands.threading import Threading, MyThread


def test_threading_wait_keyboard_interrupt(monkeypatch):
    calls = []

    class DummyThread:
        def __init__(self, name="runner"):
            self.thread = type("T", (), {"is_alive": lambda self: False})()
            self.result = None
        def wait_for_keyboard_interrupt(self, verbose=False):
            calls.append("wait")

    t = Threading()
    t.runner_threads = [DummyThread(), DummyThread()]
    t.wait_for_keyboard_interrupt()
    assert calls == ["wait", "wait"]


def test_threading_cleanup_resets(monkeypatch):
    t = Threading()
    t.input_threads = [1, 2]
    t.runner_threads = [3]
    t.thread_ids.get()
    t.cleanup()
    assert t.input_threads == []
    assert t.runner_threads == []
    # ID should reset to start
    assert t.thread_ids.get() == 0
