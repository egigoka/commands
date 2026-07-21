# Consolidated tests for commands/audio.py (negative)

# ---- from test_audio_negative.py ----

# Placeholder for future tests.
import pytest
from commands.audio import Audio

class TestAudioCoverage:
    """Tests to improve Audio module coverage"""

    def test_init_raises_when_path_not_set(self):
        """Test __init__ raises ValueError when path is not set"""
        with pytest.raises(ValueError, match="Audio path is not set"):
            Audio("")
