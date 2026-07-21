# Consolidated tests for commands/screen.py (negative)

# ---- from test_screen_negative.py ----

# Placeholder for future tests.
import pytest
from commands.screen import Screen

class TestScreenCoverage:
    """Tests to improve Screen module coverage"""
    def test_color_instance_without_position_raises(self):
        """Test that calling color() without position raises ValueError"""
        s = Screen()
        with pytest.raises(ValueError, match="Position is not set"):
            s.color()
