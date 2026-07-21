# Consolidated tests for commands/threading.py (negative)

# ---- from test_threading_missing_coverage.py ----


#! python3
# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock, MagicMock
from commands.threading import MyThread, Threading, IsRunning
from commands.threading import Threading, MyThread, IsRunning
from commands.threading import Threading, MyThread

"""Tests for missing coverage in threading.py module"""
import time
import pytest
from commands.threading import MyThread, Threading


class TestThreadingMissingCoverage:
    """Tests to cover missing lines in threading.py"""

    def test_mythread_verbose_mode(self):
        """Test MyThread with verbose=True to cover line 57"""
        result = []

        def task():
            result.append("done")

        thread = MyThread(task, verbose=True)
        thread.start()
        thread.thread.join()

        assert result == ["done"]

    def test_mythread_wait_for_keyboard_interrupt(self):
        """Test wait_for_keyboard_interrupt method (lines 66-77)

        This test covers normal completion path through wait_for_keyboard_interrupt.
        """
        result = []

        def task():
            result.append("completed")

        thread = MyThread(task)
        thread.start()
        thread.wait_for_keyboard_interrupt()

        assert result == ["completed"]

    def test_mythread_is_running(self):
        """Test is_running method (line 80)"""
        def long_task():
            time.sleep(0.1)

        thread = MyThread(long_task)
        thread.start()

        # Thread should be running initially
        is_running = thread.is_running()
        # Can't guarantee it's still running due to timing, just call the method
        thread.thread.join()

        # After join, should not be running
        assert not thread.is_running()

    def test_threading_with_verbose(self):
        """Test Threading.runner with verbose=True (lines 132-148)"""
        results = []

        def task1():
            results.append(1)

        def task2():
            results.append(2)

        runner = Threading(max_threads=1, verbose=True)
        runner.add(task1)
        runner.add(task2)
        runner.start()

        # Wait for completion
        time.sleep(0.5)

        assert set(results) == {1, 2}

    def test_threading_max_threads_zero(self):
        """Test Threading with max_threads=0 (line 157)"""
        results = []

        def task():
            results.append("x")

        runner = Threading(max_threads=0)
        runner.add(task)
        runner.add(task)
        runner.start()

        time.sleep(0.5)
        assert len(results) == 2

    def test_threading_start_from_first(self):
        """Test Threading with start_from_first=True (line 160)"""
        results = []

        def task(n):
            results.append(n)

        runner = Threading(start_from_first=True, max_threads=1)
        runner.add(task, kwargs={"n": 1})
        runner.add(task, kwargs={"n": 2})
        runner.start()

        time.sleep(0.5)
        # When start_from_first=True, threads are reversed, so they execute in order
        assert results == [1, 2]

    def test_threading_wait_for_keyboard_interrupt(self):
        """Test Threading.wait_for_keyboard_interrupt (line 168)"""
        results = []

        def task():
            results.append("done")
            time.sleep(0.01)

        runner = Threading(max_threads=1)
        runner.add(task)
        runner.start(wait_for_keyboard_interrupt=True)

        assert results == ["done"]

    def test_threading_cleanup(self):
        """Test Threading.cleanup method (lines 194-196)"""
        runner = Threading()
        runner.add(lambda: None)

        assert len(runner.input_threads) > 0

        runner.cleanup()

        assert len(runner.input_threads) == 0
        assert len(runner.runner_threads) == 0

    def test_threading_get_ids(self):
        runner = Threading()
        runner.add(lambda: None)
        runner.add(lambda: None)
        assert runner.get_ids() == [0, 1]

    def test_threading_raise_exception(self):
        calls = []

        class DummyThread:
            def __init__(self, name):
                self.name = name

            def raise_exception(self):
                calls.append(self.name)

        runner = Threading()
        runner.runner_threads = [DummyThread("runner")]
        runner.input_threads = [DummyThread("input")]
        runner.raise_exception()
        assert calls == ["runner", "input"]

    def test_threading_get_results(self):
        """Test Threading.get_results method (lines 213-215)"""
        def task(n):
            return n * 2

        runner = Threading()
        runner.add(task, kwargs={"n": 1})
        runner.add(task, kwargs={"n": 2})
        runner.start()

        time.sleep(0.5)
        results = runner.get_results()

        assert list(results) == [2, 4]

    def test_threading_is_running(self):
        """Test Threading.is_running method (lines 218-222)"""
        def quick_task():
            pass

        runner = Threading()
        runner.add(quick_task)

        # Before start, nothing should be running
        running_count = runner.is_running()
        assert running_count == 0

    def test_threading_running_threads(self):
        """Test Threading.running_threads method (lines 228-233)"""
        def long_task():
            time.sleep(0.5)

        runner = Threading(max_threads=1)
        runner.add(long_task)
        runner.add(long_task)
        runner.start()

        time.sleep(0.1)  # Let first thread start
        running = runner.running_threads()

        # Should have threads running
        assert running > 0

        # Wait for completion
        time.sleep(1)

class TestMyThreadComprehensive:
    """Comprehensive tests for MyThread class"""
    def test_run_system_exit(self):
        """Test run method with SystemExit to cover lines 50-51"""
        def raising_func():
            raise SystemExit("test exit")

        thread = MyThread(raising_func, verbose=True)

        with patch('commands.print.Print') as mock_print:
            thread.run()
            # Should print "Killed" message
            # Check if print was called with a message containing "Killed"
            call_args = [str(call) for call in mock_print.call_args_list]
            assert any("Killed" in str(arg) for arg in call_args)
    def test_wait_for_keyboard_interrupt_with_exception(self):
        """Test wait_for_keyboard_interrupt with KeyboardInterrupt to cover lines 75-77"""
        def quick_func():
            time.sleep(0.1)
            return "result"

        thread = MyThread(quick_func)
        thread.start()

        # Mock thread.join to raise KeyboardInterrupt
        with patch.object(thread.thread, 'join', side_effect=KeyboardInterrupt()):
            with pytest.raises(KeyboardInterrupt):
                thread.wait_for_keyboard_interrupt()

class TestThreadingComprehensive:
    """Comprehensive tests for Threading class"""
    def test_wait_for_keyboard_interrupt_with_exception(self):
        """Test wait_for_keyboard_interrupt with KeyboardInterrupt to cover lines 188-190"""
        threading_obj = Threading()

        def quick_func():
            return "result"

        threading_obj.add(quick_func)
        threading_obj.start()

        # Mock wait_for_keyboard_interrupt on runner threads to raise KeyboardInterrupt
        for runner in threading_obj.runner_threads:
            with patch.object(runner, 'wait_for_keyboard_interrupt', side_effect=KeyboardInterrupt()):
                with pytest.raises(KeyboardInterrupt):
                    threading_obj.wait_for_keyboard_interrupt()
                break  # Only test one

def test_threading_start_no_threads():
    t = Threading()
    with pytest.raises(AssertionError):
        t.start()

def test_mythread_localtrace_and_kill():
    state = {"raised": False}

    def sample():
        return "done"

    mt = MyThread(sample)
    assert isinstance(mt.localtrace(None, "call", None), type(mt.localtrace))
    mt.kill()
    with pytest.raises(SystemExit):
        mt.localtrace(None, "line", None)

def test_mythread_kill_triggers_system_exit_on_trace_call():
    t = MyThread(lambda: None)
    t.kill()
    with pytest.raises(SystemExit):
        t.localtrace(None, "line", None)

def test_mythread_wait_for_keyboard_interrupt_kills_and_reraises(monkeypatch):
    t = MyThread(lambda: None, verbose=False)
    monkeypatch.setattr(t.thread, "join", lambda: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        t.wait_for_keyboard_interrupt()
    assert t.killed is True

def test_threading_wait_for_keyboard_interrupt_kills_all(monkeypatch):
    class DummyThread:
        def __init__(self, wait_raises=False):
            self.killed = False
            self.wait_raises = wait_raises

        def wait_for_keyboard_interrupt(self, verbose=False):
            if self.wait_raises:
                raise KeyboardInterrupt()

        def raise_exception(self):
            self.killed = True

    runner = Threading(max_threads=0)
    runner.runner_threads = [DummyThread(wait_raises=True)]
    runner.input_threads = [DummyThread(wait_raises=False)]

    with pytest.raises(KeyboardInterrupt):
        runner.wait_for_keyboard_interrupt()

    assert all(t.killed for t in runner.runner_threads)
    assert all(t.killed for t in runner.input_threads)
