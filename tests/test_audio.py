# Consolidated tests for commands/audio.py (unit)

# ---- from test_audio9.py ----


import pytest


def test_audio9_import():
    from commands import Audio
    assert Audio is not None


def test_audio_instance_helper(monkeypatch):
    from commands.audio import Audio
    handle = type("H", (), {"info": type("I", (), {"bitrate": 128})()})
    monkeypatch.setattr("commands.audio.mutagen", type("M", (), {"File": lambda path: handle}))
    a = Audio("song.mp3")
    assert a.bitrate() == 128
    assert a.mutagen_handle() is handle


# ---- from test_audio_coverage.py ----


import pytest
from commands.audio import Audio
