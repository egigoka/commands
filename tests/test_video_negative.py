# Consolidated tests for commands/video.py (negative)

# ---- from test_video_negative.py ----

# Placeholder for future tests.
import pytest
import types
from commands.video import Video

def test_video_instance_requires_path():
    with pytest.raises(ValueError, match="Video path is not set"):
        Video().clip()
