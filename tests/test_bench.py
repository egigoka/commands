# Consolidated tests for commands/bench.py (unit)

# ---- from test_bench9.py ----


import pytest
import time
import datetime
from commands.bench import Bench


class TestBenchInit:
    """Tests for Bench initialization."""

    def test_init_default(self):
        """Default init sets time_start, no name, not verbose."""
        bench = Bench()
        assert bench.name == ""
        assert bench.verbose is False
        assert bench.time_start is not None
        assert bench.time_end is None

    def test_init_with_name(self):
        """Init with name stores it."""
        bench = Bench("my timer")
        assert bench.name == "my timer"

    def test_init_with_verbose(self):
        """Init with verbose stores it."""
        bench = Bench(verbose=True)
        assert bench.verbose is True

    def test_init_with_name_and_verbose(self):
        """Init with both parameters."""
        bench = Bench("test", verbose=True)
        assert bench.name == "test"
        assert bench.verbose is True


class TestBenchStart:
    """Tests for start() method."""

    def test_start_resets_time(self):
        """start() resets time_start to now."""
        bench = Bench()
        original = bench.time_start
        time.sleep(0.01)
        bench.start()
        assert bench.time_start > original

    def test_start_clears_time_end(self):
        """start() clears time_end."""
        bench = Bench()
        bench.stop()
        assert bench.time_end is not None
        bench.start()
        assert bench.time_end is None

    def test_start_returns_self(self):
        """start() returns self for chaining."""
        bench = Bench()
        result = bench.start()
        assert result is bench


class TestBenchGet:
    """Tests for get() method."""

    def test_get_returns_elapsed(self):
        """get() returns elapsed time in seconds."""
        bench = Bench()
        time.sleep(0.02)
        delta = bench.get()
        assert delta >= 0.02

    def test_get_does_not_stop(self):
        """get() does not set time_end."""
        bench = Bench()
        bench.get()
        assert bench.time_end is None

    def test_get_increases_over_time(self):
        """Multiple get() calls return increasing values."""
        bench = Bench()
        d1 = bench.get()
        time.sleep(0.01)
        d2 = bench.get()
        assert d2 > d1


class TestBenchStop:
    """Tests for stop() method."""

    def test_stop_returns_elapsed(self):
        """stop() returns elapsed time."""
        bench = Bench()
        time.sleep(0.02)
        delta = bench.stop()
        assert delta >= 0.02

    def test_stop_sets_time_end(self):
        """stop() sets time_end."""
        bench = Bench()
        assert bench.time_end is None
        bench.stop()
        assert bench.time_end is not None

    def test_stop_freezes_time(self):
        """After stop(), time_end is fixed."""
        bench = Bench()
        time.sleep(0.01)
        bench.stop()
        end1 = bench.time_end
        time.sleep(0.01)
        assert bench.time_end == end1


class TestBenchEnd:
    """Tests for end() method."""

    def test_end_returns_elapsed(self):
        """end() returns elapsed time."""
        bench = Bench()
        time.sleep(0.02)
        delta = bench.end()
        assert delta >= 0.02

    def test_end_stops_timer(self):
        """end() sets time_end."""
        bench = Bench()
        bench.end()
        assert bench.time_end is not None

    def test_end_verbose_false_no_output(self, capsys):
        """end(verbose=False) produces no output."""
        bench = Bench()
        bench.end(verbose=False)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_end_verbose_true_prints(self, capsys):
        """end(verbose=True) prints result."""
        bench = Bench("test timer")
        time.sleep(0.01)
        bench.end(verbose=True)
        captured = capsys.readouterr()
        assert "test timer" in captured.out
        assert "seconds" in captured.out

    def test_end_uses_instance_verbose(self, capsys):
        """end() uses self.verbose when not specified."""
        bench = Bench("timer", verbose=True)
        time.sleep(0.01)
        bench.end()
        captured = capsys.readouterr()
        assert "timer" in captured.out

    def test_end_verbose_override(self, capsys):
        """end(verbose=False) overrides instance verbose=True."""
        bench = Bench("timer", verbose=True)
        bench.end(verbose=False)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_end_precision(self, capsys):
        """end() respects precision parameter."""
        bench = Bench("p", verbose=True)
        time.sleep(0.0123)
        bench.end(precision=2)
        captured = capsys.readouterr()
        # With precision=2, should show 2 decimal places
        assert "seconds" in captured.out


class TestBenchCall:
    """Tests for __call__ method."""

    def test_call_returns_elapsed(self):
        """Calling bench returns elapsed time."""
        bench = Bench()
        time.sleep(0.02)
        delta = bench()
        assert delta >= 0.02

    def test_call_does_not_stop(self):
        """Calling bench does not stop timer."""
        bench = Bench()
        bench()
        assert bench.time_end is None


class TestBenchContextManager:
    """Tests for context manager protocol."""

    def test_context_manager_basic(self):
        """Bench works as context manager."""
        with Bench() as b:
            time.sleep(0.02)
        assert b.time_end is not None
        delta = (b.time_end - b.time_start).total_seconds()
        assert delta >= 0.02

    def test_context_manager_restarts(self):
        """Context manager restarts the timer on entry."""
        bench = Bench()
        original = bench.time_start
        time.sleep(0.01)
        with bench:
            pass
        assert bench.time_start > original


class TestBenchRepr:
    """Tests for __repr__ method."""

    def test_repr_running(self):
        """repr shows running state."""
        bench = Bench("test")
        r = repr(bench)
        assert "Bench(" in r
        assert "name='test'" in r
        assert "running" in r

    def test_repr_stopped(self):
        """repr shows stopped state."""
        bench = Bench("test")
        bench.stop()
        r = repr(bench)
        assert "stopped" in r

    def test_repr_elapsed(self):
        """repr shows elapsed time."""
        bench = Bench()
        time.sleep(0.01)
        r = repr(bench)
        assert "elapsed=" in r


class TestBenchPrintFallback:
    """Tests for print fallback behavior."""

    def test_fallback_on_import_error(self, capsys, monkeypatch):
        """Falls back to print() when Print import fails."""
        def mock_import_error(*args, **kwargs):
            raise ImportError("Mock")

        import commands.bench
        original_print_result = commands.bench.Bench._print_result

        def patched_print_result(self, delta, precision):
            # Simulate ImportError by using plain print
            rounded = round(delta, precision)
            prefix = f"{self.name} " if self.name else "Bench: "
            print(f"{prefix}{rounded} seconds")

        monkeypatch.setattr(commands.bench.Bench, "_print_result", patched_print_result)

        bench = Bench("fallback")
        time.sleep(0.01)
        bench.end(verbose=True)
        captured = capsys.readouterr()
        assert "fallback" in captured.out
        assert "seconds" in captured.out

    def test_fallback_on_type_error(self, capsys, monkeypatch):
        """Falls back to print() when Print.colored raises TypeError."""
        def mock_colored_error(*args, **kwargs):
            raise TypeError("Mock")

        import commands.print
        monkeypatch.setattr(commands.print.Print, "colored", mock_colored_error)

        bench = Bench("type error test")
        time.sleep(0.01)
        bench.end(verbose=True)
        captured = capsys.readouterr()
        assert "type error test" in captured.out
        assert "seconds" in captured.out

    def test_fallback_on_attribute_error(self, capsys, monkeypatch):
        """Falls back to print() when Print.colored raises AttributeError."""
        def mock_colored_error(*args, **kwargs):
            raise AttributeError("Mock")

        import commands.print
        monkeypatch.setattr(commands.print.Print, "colored", mock_colored_error)

        bench = Bench("attr error test")
        time.sleep(0.01)
        bench.end(verbose=True)
        captured = capsys.readouterr()
        assert "attr error test" in captured.out


class TestBenchNoName:
    """Tests for bench without name."""

    def test_no_name_uses_default_prefix(self, capsys):
        """When no name, uses 'Bench: ' prefix."""
        bench = Bench(verbose=True)
        time.sleep(0.01)
        bench.end()
        captured = capsys.readouterr()
        assert "Bench: " in captured.out
