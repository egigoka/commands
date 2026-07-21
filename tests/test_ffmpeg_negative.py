# Consolidated tests for commands/ffmpeg.py (negative)

# ---- from test_ffmpeg_negative.py ----

# Placeholder for future tests.
import pytest
from commands.ffmpeg import FFMpeg
from unittest.mock import MagicMock, patch

def test_ffmpeg_instance_requires_input():
    f = FFMpeg(output_file="out.mkv")
    with pytest.raises(ValueError):
        f.subtitles({}, {})

def test_ffmpeg_instance_requires_output():
    f = FFMpeg(input_file="in.mkv")
    with pytest.raises(ValueError):
        f.subtitles({}, None)

def test_ffmpeg_instance_missing_input_output():
    f = FFMpeg()
    with pytest.raises(ValueError):
        f.subtitles({}, {})
    with pytest.raises(ValueError):
        f.audio({}, {})

def test_ffmpeg_input_output_validation():
    ff = FFMpeg()
    with pytest.raises(ValueError):
        ff._input(None)
    with pytest.raises(ValueError):
        ff._output(None)
