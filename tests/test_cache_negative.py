# Consolidated tests for commands/cache.py (negative)

# ---- from test_cache_negative.py ----

# Placeholder for future tests.
import pytest
import time
from commands.cache import Cache, CachedFunction
from commands.bench import Bench

def test_cache_update_every_zero():
    """Should handle update_every=0 (updates every time)"""
    call_count = [0]

    def test_func():
        call_count[0] += 1
        return "result"

    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=1, bench=bench)  # Every call updates

    cache()
    cache()
    cache()

    # Should be called 3 times (every call)
    assert call_count[0] == 3

def test_cache_with_exception_in_func():
    """Should handle exceptions in cached function"""
    def failing_func():
        raise ValueError("Test error")

    bench = Bench(verbose=False)
    cache = Cache(failing_func, update_every=2, bench=bench)

    with pytest.raises(ValueError):
        cache()

def test_cached_function_with_mutable_args():
    """Should handle mutable arguments"""
    def test_func(lst):
        return len(lst)

    cached = CachedFunction(test_func, update_every=10, verbose=False)

    result1 = cached([1, 2, 3])
    result2 = cached([1, 2, 3, 4])

    assert result1 == 3
    assert result2 == 4

def test_cache_attribute_error_recovery():
    """Should handle missing stored_output attribute"""
    call_count = [0]

    def test_func():
        call_count[0] += 1
        return f"call_{call_count[0]}"

    bench = Bench(verbose=False)
    cache = Cache(test_func, update_every=3, bench=bench)

    # First call: counter=0, 0%3==0, run() called
    result1 = cache()
    assert result1 == "call_1"

    # Second call: counter=1, 1%3!=0, run() NOT called, returns stored_output
    # But we delete stored_output to trigger except block
    delattr(cache, 'stored_output')

    # Should recover by calling run() in except block
    result2 = cache()
    assert result2 == "call_2"  # run() was called in except block
    assert call_count[0] == 2
