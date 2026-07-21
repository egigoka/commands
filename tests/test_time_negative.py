# Consolidated tests for commands/time.py (negative)

# ---- from test_time_negative.py ----

# Placeholder for future tests.
import pytest
import time
import datetime
from commands.time import Time

class TestTimeTimestampToDatetime:
    """Tests for Time.timestamp_to_datetime method"""
    def test_timestamp_to_datetime_invalid_type(self):
        with pytest.raises(TypeError):
            Time.timestamp_to_datetime([1, 2, 3])

class TestTimeSleep:
    """Tests for Time.sleep method"""
    def test_sleep_negative_raises(self):
        with pytest.raises(ValueError, match="sleep time must be non-negative"):
            Time.sleep(-1)

def test_time_sleep_negative():
    with pytest.raises(ValueError):
        Time.sleep(-1)
