# Consolidated tests for commands/int.py (negative)

# ---- from test_int_negative.py ----

# Placeholder for future tests.
import pytest
from commands.int import Int

class TestIntInstance:
    """Tests for Int instance methods"""
    def test_int_instance_ensure_raises_no_start(self):
        """Test _ensure raises when start is None"""
        i = Int(None, 10)
        with pytest.raises(ValueError, match="Both start and end must be set"):
            i._ensure()
    def test_int_instance_ensure_raises_no_end(self):
        """Test _ensure raises when end is None"""
        i = Int(5, None)
        with pytest.raises(ValueError, match="Both start and end must be set"):
            i._ensure()
    def test_int_instance_ensure_raises_both_none(self):
        """Test _ensure raises when both are None"""
        i = Int()
        with pytest.raises(ValueError, match="Both start and end must be set"):
            i._ensure()
    def test_int_instance_range_raises_without_params(self):
        """Test instance range raises when start/end not set"""
        i = Int()
        with pytest.raises(ValueError, match="Both start and end must be set"):
            i.range()
