# Consolidated tests for commands/cache.py (unit)

# ---- from test_cache9.py ----


import pytest
import time
from commands.cache import Cache, CachedFunction
from commands.bench import Bench


def test_cache_basic():
    call_count = [0]

    def test_func():
        call_count[0] += 1
        return "result"

    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=2, bench=bench)

    result1 = cache()  # counter=0, 0%2==0, run() called
    result2 = cache()  # counter=1, 1%2==1, run() not called

    assert result1 == "result"
    assert result2 == "result"
    assert call_count[0] == 1  # Only called once (on first call)


def test_cache_with_args():
    def test_func(x, y):
        return x + y

    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=2, args=(1, 2), bench=bench)

    result = cache()
    assert result == 3


def test_cache_with_kwargs():
    def test_func(a=0, b=0):
        return a * b

    from commands.dict import ImDict
    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=2, kwargs=ImDict({"a": 3, "b": 4}), bench=bench)

    result = cache()
    assert result == 12


def test_cached_function_basic():
    call_count = [0]

    def test_func(x):
        call_count[0] += 1
        return x * 2

    cached = CachedFunction(test_func, update_every=3, verbose=False)

    result1 = cached(5)
    result2 = cached(5)

    assert result1 == 10
    assert result2 == 10


def test_cached_function_different_args():
    def test_func(x):
        return x * 2

    cached = CachedFunction(test_func, update_every=3, verbose=False)

    result1 = cached(5)
    result2 = cached(10)

    assert result1 == 10
    assert result2 == 20


def test_cached_function_kwargs():
    def test_func(x, y=1):
        return x + y

    cached = CachedFunction(test_func, update_every=3, verbose=False)

    result = cached(5, y=3)
    assert result == 8


def test_cache_update_counter():
    call_count = [0]

    def test_func():
        call_count[0] += 1
        return call_count[0]

    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=2, bench=bench)

    r1 = cache()  # counter=0, 0%2==0, run() called
    r2 = cache()  # counter=1, 1%2==1, run() not called
    r3 = cache()  # counter=2, 2%2==0, run() called

    assert call_count[0] == 2  # Called twice (on 1st and 3rd call)


# Negative tests






def test_cache_without_bench_parameter():
    """Should create its own Bench when bench parameter not provided"""
    def test_func():
        return "result"

    # Don't provide bench parameter
    cache = Cache(test_func, update_every=2, verbose=False)

    # Should have created its own bench
    assert cache.bench is not None
    assert hasattr(cache.bench, 'name')

    result = cache()
    assert result == "result"


def test_cache_value_alias(monkeypatch):
    calls = {"cnt": 0}
    def test_func():
        calls["cnt"] += 1
        return calls["cnt"]

    cache = Cache(test_func, update_every=1, verbose=False)
    assert cache.value() == 1
    assert cache() == 2  # update_every=1 triggers run each time


def test_cached_function_value(monkeypatch):
    calls = {"cnt": 0}
    def test_func(x):
        calls["cnt"] += 1
        return x * 2

    cached = CachedFunction(test_func, update_every=2, verbose=False)
    assert cached.value(2) == 4
    assert cached(2) == 4  # from cache




class TestCacheEdgeCases:
    """Edge case tests for Cache module"""

    def test_cache_run_updates_stored_output(self):
        """Test that run() updates stored_output"""
        def test_func():
            return "result"

        bench = Bench(verbose=False)
        cache = Cache(test_func, update_every=2, bench=bench)

        # Manually call run()
        cache.run()
        assert cache.stored_output == "result"

    def test_cache_run_calls_bench_end(self, monkeypatch):
        """Test that run() calls bench.end()"""
        bench_end_called = [False]

        def mock_bench_end(self):
            bench_end_called[0] = True

        from commands.bench import Bench
        monkeypatch.setattr(Bench, "end", mock_bench_end)

        def test_func():
            return "result"

        bench = Bench(verbose=False)
        cache = Cache(test_func, update_every=2, bench=bench)
        cache.run()

        assert bench_end_called[0] is True

    def test_cached_function_cache_flush(self):
        """Test that CachedFunction flushes caches periodically"""
        call_count = [0]

        def test_func(x):
            call_count[0] += 1
            return x * 2

        cached = CachedFunction(test_func, update_every=3, verbose=False)

        # First call - creates cache
        result1 = cached(5)
        assert result1 == 10
        assert len(cached.caches) == 1

        # Second call - uses cache
        result2 = cached(5)
        assert result2 == 10

        # Third call - counter=2, 2%3!=0, doesn't flush
        result3 = cached(5)
        assert len(cached.caches) == 1

        # Fourth call - counter=3, 3%3==0, flushes caches
        result4 = cached(5)
        # Caches should be flushed and recreated
        assert result4 == 10

    def test_cached_function_multiple_args_creates_separate_caches(self):
        """Test that different args create separate caches"""
        def test_func(x):
            return x * 2

        cached = CachedFunction(test_func, update_every=10, verbose=False)

        cached(1)
        cached(2)
        cached(3)

        # Should have 3 separate caches
        assert len(cached.caches) >= 3

    def test_cached_function_kwargs_creates_separate_cache(self):
        """Test that kwargs create separate cache entries"""
        def test_func(x, y=1):
            return x + y

        cached = CachedFunction(test_func, update_every=10, verbose=False)

        result1 = cached(5, y=2)
        result2 = cached(5, y=3)

        # Should have separate caches for different kwargs
        assert len(cached.caches) >= 2
        assert result1 == 7
        assert result2 == 8

    def test_cached_function_return_value_recursion(self):
        """Test return_value method handles recursion correctly"""
        call_count = [0]

        def test_func(x):
            call_count[0] += 1
            return x * 2

        cached = CachedFunction(test_func, update_every=10, verbose=False)

        # First call goes through return_value -> creates cache -> return_value again
        result = cached(42)
        assert result == 84
        # Should only call function once despite recursion
        assert call_count[0] == 1

    def test_cached_function_counter_increments(self):
        """Test that CachedFunction counter increments"""
        def test_func(x):
            return x

        cached = CachedFunction(test_func, update_every=5, verbose=False)

        initial_count = cached.counter.cnt
        cached(1)
        after_count = cached.counter.cnt

        # Counter should have incremented
        assert after_count > initial_count

    def test_cache_lock_usage(self):
        """Test that Cache uses lock for thread safety"""
        def test_func():
            return "result"

        bench = Bench(verbose=False)
        cache = Cache(test_func, update_every=2, bench=bench)

        # Lock should exist
        assert hasattr(cache, 'lock')
        assert cache.lock is not None

    def test_cached_function_lock_usage(self):
        """Test that CachedFunction uses lock for thread safety"""
        def test_func(x):
            return x

        cached = CachedFunction(test_func, update_every=2, verbose=False)

        # Lock should exist
        assert hasattr(cached, 'lock')
        assert cached.lock is not None

    def test_cache_with_complex_kwargs(self):
        """Test Cache with complex kwargs using ImDict"""
        from commands.dict import ImDict

        def test_func(a, b=1, c=2):
            return a + b + c

        bench = Bench(verbose=False)
        cache = Cache(test_func, update_every=2, args=(10,),
                     kwargs=ImDict({"b": 20, "c": 30}), bench=bench)

        result = cache()
        assert result == 60  # 10 + 20 + 30

    def test_cached_function_with_no_args(self):
        """Test CachedFunction with no arguments"""
        call_count = [0]

        def test_func():
            call_count[0] += 1
            return "no_args"

        cached = CachedFunction(test_func, update_every=5, verbose=False)

        result1 = cached()
        result2 = cached()

        assert result1 == "no_args"
        assert result2 == "no_args"
        # Should use cache, so only called once
        assert call_count[0] == 1
