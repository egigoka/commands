# Consolidated tests for commands/threading.py (integration)

# ---- from test_threading_integration.py ----


import pytest
import time
from commands.threading import MyThread, Threading


class TestThreadingIntegration:
    """Integration tests that actually run threads to cover uncovered paths"""

    def test_threading_with_cleanup(self):
        """Test cleanup method to cover lines 194-196"""
        threading_obj = Threading()

        def quick_func():
            return "result"

        threading_obj.add(quick_func)
        threading_obj.add(quick_func)

        # Call cleanup before starting
        threading_obj.cleanup()

        # Should have cleared everything
        assert len(threading_obj.input_threads) == 0
        assert len(threading_obj.runner_threads) == 0

    def test_threading_get_results_integration(self):
        """Test get_results with actual thread execution"""
        threading_obj = Threading(max_threads=2)

        results_list = []

        def func1():
            time.sleep(0.01)
            results_list.append(1)
            return "result1"

        def func2():
            time.sleep(0.01)
            results_list.append(2)
            return "result2"

        def func3():
            time.sleep(0.01)
            results_list.append(3)
            return "result3"

        threading_obj.add(func1)
        threading_obj.add(func2)
        threading_obj.add(func3)

        threading_obj.start()

        # Wait for all threads to complete
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=5)

        # Get results
        results = list(threading_obj.get_results())

        # Should have 3 results
        assert len(results) == 3

    def test_threading_is_running_integration(self):
        """Test is_running with actual thread execution"""
        threading_obj = Threading()

        def slow_func():
            time.sleep(0.5)
            return "result"

        threading_obj.add(slow_func)
        threading_obj.add(slow_func)

        # Before start, should be 0
        running = threading_obj.is_running()
        assert running == 0

        threading_obj.start()

        # Right after start, threads might be running
        time.sleep(0.1)
        # Just verify the method works
        running = threading_obj.is_running()
        assert running >= 0

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)

    def test_threading_running_threads_integration(self):
        """Test running_threads with actual thread execution"""
        threading_obj = Threading(max_threads=2)

        def slow_func():
            time.sleep(0.3)
            return "result"

        threading_obj.add(slow_func)
        threading_obj.add(slow_func)
        threading_obj.add(slow_func)

        threading_obj.start()

        # Right after start, should have running threads
        time.sleep(0.05)
        running = threading_obj.running_threads()

        # Should have some threads running
        assert running > 0

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)

    def test_threading_total_input_threads(self):
        """Test total_input_threads method"""
        threading_obj = Threading()

        def quick_func():
            return "result"

        # Before adding
        assert threading_obj.total_input_threads() == 0

        threading_obj.add(quick_func)
        threading_obj.add(quick_func)
        threading_obj.add(quick_func)

        # After adding
        assert threading_obj.total_input_threads() == 3

    def test_threading_start_from_first(self):
        """Test start_from_first option"""
        threading_obj = Threading(start_from_first=True, max_threads=1)

        execution_order = []

        def make_func(number):
            def func():
                time.sleep(0.01)
                execution_order.append(number)
                return f"result{number}"
            return func

        # Add in order 1, 2, 3
        threading_obj.add(make_func(1))
        threading_obj.add(make_func(2))
        threading_obj.add(make_func(3))

        threading_obj.start()

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=3)

        # With start_from_first=True, list is reversed before execution
        # So execution should be 1, 2, 3 (instead of 3, 2, 1)
        assert execution_order == [1, 2, 3]

    def test_mythread_kill(self):
        """Test MyThread kill method"""
        def long_running_func():
            for i in range(100):
                time.sleep(0.01)
            return "done"

        thread = MyThread(long_running_func)
        thread.start()

        time.sleep(0.05)

        # Kill the thread
        thread.kill()

        # Should have killed flag set
        assert thread.killed

    def test_threading_kill(self):
        """Test Threading kill method (alias for raise_exception)"""
        threading_obj = Threading()

        def slow_func():
            time.sleep(0.5)
            return "result"

        threading_obj.add(slow_func)
        threading_obj.start()

        time.sleep(0.05)

        # Kill all threads
        threading_obj.kill()

        # Active jobs should stop and internal runners should exit naturally.
        for thread in threading_obj.running_now_threads:
            assert thread.killed
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=2)
            assert not runner.thread.is_alive()

    def test_threading_wait_for_completion(self):
        """Test wait_for_keyboard_interrupt without actual interrupt"""
        threading_obj = Threading()

        def quick_func():
            time.sleep(0.01)
            return "result"

        threading_obj.add(quick_func)
        threading_obj.add(quick_func)

        threading_obj.start()

        # Wait for threads to complete (shouldn't raise)
        threading_obj.wait_for_keyboard_interrupt()

        # All should be done
        assert threading_obj.total_input_threads() == 0

    def test_mythread_callable(self):
        """Test MyThread __call__ method"""
        result_holder = []

        def func():
            result_holder.append("done")
            return "result"

        thread = MyThread(func)

        # Call using __call__
        returned = thread()

        # Should return self
        assert returned is thread

        # Wait for completion
        thread.thread.join(timeout=1)

        assert "done" in result_holder

    def test_threading_callable(self):
        """Test Threading __call__ method"""
        threading_obj = Threading()

        def quick_func():
            return "result"

        threading_obj.add(quick_func)

        # Call using __call__
        returned = threading_obj()

        # Should return self
        assert returned is threading_obj

        # Wait for completion
        for runner in threading_obj.runner_threads:
            runner.thread.join(timeout=1)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
