# Consolidated tests for commands/time.py (unit)

# ---- from test_time9.py ----


import pytest
import time
import datetime
from commands.time import Time


class TestTimeStamp:
    """Tests for Time.stamp method"""

    def test_stamp_returns_float(self):
        result = Time.stamp()
        assert isinstance(result, float)

    def test_stamp_is_current(self):
        before = time.time()
        result = Time.stamp()
        after = time.time()
        assert before <= result <= after


class TestTimeDatetime:
    """Tests for Time.datetime method"""

    def test_datetime_no_args(self):
        result = Time.datetime()
        assert isinstance(result, datetime.datetime)

    def test_datetime_with_year(self):
        result = Time.datetime(year=2020)
        assert result.year == 2020

    def test_datetime_with_multiple_args(self):
        result = Time.datetime(year=2020, month=5, day=15)
        assert result.year == 2020
        assert result.month == 5
        assert result.day == 15

    def test_datetime_with_time(self):
        result = Time.datetime(hour=14, minute=30, second=45)
        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45


class TestTimeTimestampToDatetime:
    """Tests for Time.timestamp_to_datetime method"""

    def test_timestamp_to_datetime_float(self):
        timestamp = 1609459200.0  # 2021-01-01 00:00:00
        result = Time.timestamp_to_datetime(timestamp)
        assert isinstance(result, datetime.datetime)
        assert result.year == 2021

    def test_timestamp_to_datetime_int(self):
        timestamp = 1609459200
        result = Time.timestamp_to_datetime(timestamp)
        assert isinstance(result, datetime.datetime)

    def test_timestamp_to_datetime_string(self):
        timestamp = "1609459200"
        result = Time.timestamp_to_datetime(timestamp)
        assert isinstance(result, datetime.datetime)

    def test_timestamp_to_datetime_already_datetime(self):
        dt = datetime.datetime.now()
        result = Time.timestamp_to_datetime(dt)
        assert result == dt



class TestTimeDatetimeToTimestamp:
    """Tests for Time.datetime_to_timestamp method"""

    def test_datetime_to_timestamp(self):
        dt = datetime.datetime(2021, 1, 1, 0, 0, 0)
        result = Time.datetime_to_timestamp(dt)
        assert isinstance(result, float)

    def test_datetime_to_timestamp_already_float(self):
        timestamp = 1609459200.0
        result = Time.datetime_to_timestamp(timestamp)
        assert result == timestamp

    def test_datetime_to_timestamp_roundtrip(self):
        dt = datetime.datetime.now()
        timestamp = Time.datetime_to_timestamp(dt)
        dt_back = Time.timestamp_to_datetime(timestamp)
        # Compare without microseconds due to precision loss
        assert dt.replace(microsecond=0) == dt_back.replace(microsecond=0)


class TestTimeDotted:
    """Tests for Time.dotted method"""

    def test_dotted_current_time(self):
        result = Time.dotted()
        assert isinstance(result, str)
        # Format: YYYY.MM.DD_at_HH.MM.SS.MMMMMM
        assert "_at_" in result
        parts = result.split("_at_")
        assert len(parts) == 2

    def test_dotted_custom_timestamp(self):
        timestamp = 1609459200.0  # 2021-01-01 00:00:00
        result = Time.dotted(timestamp)
        assert "2021" in result or "21" in result

    def test_dotted_custom_datetime(self):
        dt = datetime.datetime(2020, 12, 31, 23, 59, 59)
        result = Time.dotted(dt)
        assert "2020" in result or "20" in result
        assert "12.31" in result


class TestTimeSleep:
    """Tests for Time.sleep method"""

    def test_sleep_basic(self):
        start = time.time()
        Time.sleep(0.1)
        elapsed = time.time() - start
        assert elapsed >= 0.1
        assert elapsed < 0.2  # Should not be too long

    def test_sleep_zero(self, monkeypatch):
        calls = []
        monkeypatch.setattr("time.sleep", lambda seconds: calls.append(seconds))
        Time.sleep(0)
        assert calls == [0]



class TestTimeDelta:
    """Tests for Time.delta method"""

    def test_delta_single_arg(self):
        result = Time.delta(10)
        assert isinstance(result, datetime.timedelta)
        assert result.total_seconds() == 10

    def test_delta_two_timestamps(self):
        time_a = 1609459200.0  # 2021-01-01 00:00:00
        time_b = 1609462800.0  # 2021-01-01 01:00:00
        result = Time.delta(time_a, time_b)
        assert result == 3600.0  # 1 hour

    def test_delta_reversed_order(self):
        time_a = 1609462800.0
        time_b = 1609459200.0
        result = Time.delta(time_a, time_b)
        assert result == 3600.0  # Should still be positive

    def test_delta_datetime_objects(self):
        dt_a = datetime.datetime(2021, 1, 1, 0, 0, 0)
        dt_b = datetime.datetime(2021, 1, 1, 1, 0, 0)
        result = Time.delta(dt_a, dt_b)
        assert result == 3600.0


class TestTimeHumanReadable:
    """Tests for Time.human_readable method"""

    def test_human_readable_seconds(self):
        result = Time.human_readable(45)
        assert "45s" in result

    def test_human_readable_minutes(self):
        result = Time.human_readable(125)  # 2 minutes 5 seconds
        assert "m" in result
        assert "s" in result

    def test_human_readable_hours(self):
        result = Time.human_readable(3665)  # 1 hour, 1 minute, 5 seconds
        assert "h" in result

    def test_human_readable_days(self):
        result = Time.human_readable(86400)  # 1 day
        assert "d" in result

    def test_human_readable_timedelta(self):
        td = datetime.timedelta(seconds=120)
        result = Time.human_readable(td)
        assert "m" in result

    def test_human_readable_microseconds(self):
        result = Time.human_readable(1.5)
        assert "ms" in result  # Should include microseconds


# Coverage improvement tests
class TestTimeCoverage:
    """Tests to improve coverage for time9.py"""

    def test_datetime_with_microsecond(self):
        """Test datetime with microsecond parameter (line 44)"""
        dt = Time.datetime(microsecond=123456)
        assert dt.microsecond == 123456

    def test_datetime_with_tzinfo(self):
        """Test datetime with tzinfo parameter (line 46)"""
        import datetime
        tz = datetime.timezone.utc
        dt = Time.datetime(tzinfo=tz)
        assert dt.tzinfo == tz

    def test_datetime_with_fold(self):
        """Test datetime with fold parameter (line 48)"""
        dt = Time.datetime(fold=1)
        assert dt.fold == 1

    def test_sleep_verbose(self):
        """Test sleep with verbose=True (lines 103-120, 134)"""
        import time
        start = time.time()
        # Use a very short sleep time to make the test fast
        Time.sleep(0.1, verbose=True, check_per_sec=50)
        elapsed = time.time() - start
        # Should have slept for approximately 0.1 seconds
        assert 0.05 < elapsed < 0.2

    def test_sleep_verbose_longer(self):
        """Test sleep with verbose=True for longer duration to test timer output"""
        import time
        start = time.time()
        # Sleep for 1.5 seconds to test the timer countdown
        Time.sleep(1.5, verbose=True, check_per_sec=10)
        elapsed = time.time() - start
        assert 1.4 < elapsed < 2.0


def test_time_instance_helpers():
    import datetime
    now = datetime.datetime(2020, 1, 1, 0, 0, 0)
    t = Time(now)
    assert t.to_timestamp() == Time.datetime_to_timestamp(now)
    assert t.delta(now + datetime.timedelta(seconds=5)) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_time_fast_timer.py ----


import pytest

from commands.time import Time


def test_time_timer_fast_seconds_gt_1(monkeypatch):
    class FakeBench:
        def __init__(self, *_a, **_k):
            self._t = 0.0

        def get(self):
            self._t += 0.75
            return self._t

    calls = []

    monkeypatch.setattr("commands.bench.Bench", FakeBench)
    monkeypatch.setattr("time.sleep", lambda _s: None)
    monkeypatch.setattr("commands.print.Print.rewrite", lambda *a, **k: calls.append(" ".join(map(str, a))))

    Time.sleep(2, verbose=True, check_per_sec=10)

    assert any("Timer for 2" in c and "left" in c for c in calls)
    assert calls[-1] == ""


def test_time_timer_fast_seconds_le_1(monkeypatch):
    class FakeBench:
        def __init__(self, *_a, **_k):
            self._calls = 0

        def get(self):
            self._calls += 1
            if self._calls == 1:
                return 0.0
            return 2.0

    calls = []

    monkeypatch.setattr("commands.bench.Bench", FakeBench)
    monkeypatch.setattr("time.sleep", lambda _s: None)
    monkeypatch.setattr("commands.print.Print.rewrite", lambda *a, **k: calls.append(" ".join(map(str, a))))

    Time.sleep(0.5, verbose=True, check_per_sec=10)

    assert any("Timer for 0.5 seconds." in c and "left" not in c for c in calls)
    assert calls[-1] == ""


def test_time_instance_delta_no_args_uses_same_datetime():
    import datetime

    dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    t = Time(dt)
    assert t.delta() == 0


# ---- from test_time_instance.py ----


import datetime
import pytest
from commands.time import Time


def test_time_callable_delta():
    now = datetime.datetime.now()
    t = Time(now)
    assert isinstance(t.delta(now + datetime.timedelta(seconds=1)), float)


def test_time_callable_timestamp():
    now = datetime.datetime.now()
    t = Time(now)
    assert isinstance(t.to_timestamp(), float)
