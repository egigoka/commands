# Consolidated tests for commands/video.py (unit)

# ---- from test_video9.py ----


import pytest


def test_video9_import():
    from commands import Video
    assert Video is not None


# Coverage improvement tests
class TestVideoCoverage:
    """Tests to improve coverage for video9.py"""

    def test_get_clip_basic(self, monkeypatch):
        """Test Video.get_clip without raw flag (lines 14-23)"""
        from commands.video import Video

        # Mock VideoFileClip
        class MockClip:
            duration = 120.5
            fps = 30.0
            size = (1920, 1080)

        def mock_video_file_clip(path):
            return MockClip()

        # Mock the moviepy import
        import sys
        from unittest.mock import MagicMock

        mock_moviepy = MagicMock()
        mock_moviepy.VideoFileClip = mock_video_file_clip
        sys.modules['moviepy'] = mock_moviepy

        result = Video.get_clip("test.mp4", raw=False)

        assert result["duration"] == 120.5
        assert result["fps"] == 30.0
        assert result["size"] == (1920, 1080)

    def test_get_clip_raw(self, monkeypatch):
        """Test Video.get_clip with raw=True (lines 16-17)"""
        from commands.video import Video

        # Mock VideoFileClip
        class MockClip:
            duration = 60.0
            fps = 24.0
            size = (1280, 720)

        def mock_video_file_clip(path):
            return MockClip()

        # Mock the moviepy import
        import sys
        from unittest.mock import MagicMock

        mock_moviepy = MagicMock()
        mock_moviepy.VideoFileClip = mock_video_file_clip
        sys.modules['moviepy'] = mock_moviepy

        result = Video.get_clip("test.mp4", raw=True)

        # Should return the raw clip object
        assert hasattr(result, 'duration')
        assert result.duration == 60.0

    def test_get_length(self, monkeypatch):
        """Test Video.get_length (lines 26-28)"""
        from commands.video import Video

        # Mock get_clip to return a dict
        def mock_get_clip(path):
            return {"duration": 150.0, "fps": 25.0, "size": (1920, 1080)}

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_length("test.mp4")
        assert result == 150.0

    def test_get_fps(self, monkeypatch):
        """Test Video.get_fps (lines 31-33)"""
        from commands.video import Video

        # Mock get_clip to return a dict
        def mock_get_clip(path):
            return {"duration": 100.0, "fps": 60.0, "size": (3840, 2160)}

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_fps("test.mp4")
        assert result == 60.0

    def test_get_bitrate(self, monkeypatch):
        """Test Video.get_bitrate (lines 36-39)"""
        from commands.video import Video

        # Mock VideoFileClip with reader
        class MockReader:
            bitrate = 5000  # 5000 KiB/s

        class MockClip:
            duration = 120.0
            fps = 30.0
            size = (1920, 1080)
            reader = MockReader()

        def mock_get_clip(path, raw=False):
            return MockClip()

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_bitrate("test.mp4")
        # Should multiply by KiB (1024)
        assert result == 5000 * 1024

    def test_get_audio_bitrate(self, monkeypatch):
        """Test Video.get_audio_bitrate (lines 42-45)"""
        from commands.video import Video

        # Mock VideoFileClip with audio reader
        class MockAudioReader:
            bitrate = 320  # 320 KiB/s

        class MockAudio:
            reader = MockAudioReader()

        class MockClip:
            duration = 120.0
            fps = 30.0
            size = (1920, 1080)
            audio = MockAudio()

        def mock_get_clip(path, raw=False):
            return MockClip()

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_audio_bitrate("test.mp4")
        # Should multiply by KiB (1024)
        assert result == 320 * 1024

    def test_get_resolution(self, monkeypatch):
        """Test Video.get_resolution (lines 48-50)"""
        from commands.video import Video

        # Mock get_clip to return a dict
        def mock_get_clip(path):
            return {"duration": 90.0, "fps": 24.0, "size": (2560, 1440)}

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_resolution("test.mp4")
        assert result == (2560, 1440)

    def test_get_info(self, monkeypatch):
        """Test Video.get_info (lines 53-54)"""
        from commands.video import Video

        # Mock VideoFileClip
        class MockClip:
            duration = 180.0
            fps = 30.0
            size = (1920, 1080)

        def mock_get_clip(path, raw=False):
            if raw:
                return MockClip()
            return {"duration": 180.0, "fps": 30.0, "size": (1920, 1080)}

        monkeypatch.setattr(Video, "get_clip", mock_get_clip)

        result = Video.get_info("test.mp4")
        assert hasattr(result, 'duration')
        assert result.duration == 180.0

    def test_video_instance_helpers(self, monkeypatch):
        from commands.video import Video

        class MockClip:
            duration = 10.0
            fps = 24.0
            size = (100, 200)
            class reader:
                bitrate = 1
            class audio:
                class reader:
                    bitrate = 2

        monkeypatch.setattr(Video, "get_clip", lambda path, raw=False: MockClip() if raw else {"duration": 10.0, "fps": 24.0, "size": (100, 200)})
        monkeypatch.setattr(Video, "get_bitrate", lambda path: 1)
        monkeypatch.setattr(Video, "get_audio_bitrate", lambda path: 2)

        v = Video("p.mp4")
        assert v.length() == 10.0
        assert v.fps() == 24.0
        assert v.resolution() == (100, 200)


# ---- from test_video_more.py ----


import types

import pytest

from commands.video import Video


class _DummyReader:
    def __init__(self, bitrate):
        self.bitrate = bitrate


class _DummyAudio:
    def __init__(self, bitrate):
        self.reader = _DummyReader(bitrate)


class _DummyClip:
    def __init__(self):
        self.duration = 12.5
        self.fps = 30
        self.size = (1920, 1080)
        self.reader = _DummyReader(123)
        self.audio = _DummyAudio(45)




def test_video_class_getters_with_mocked_moviepy(monkeypatch):
    dummy_module = types.SimpleNamespace(VideoFileClip=lambda _path: _DummyClip())
    monkeypatch.setitem(__import__("sys").modules, "moviepy", dummy_module)

    clip_raw = Video.get_clip("x.mp4", raw=True)
    assert isinstance(clip_raw, _DummyClip)

    clip = Video.get_clip("x.mp4", raw=False)
    assert clip["duration"] == 12.5
    assert clip["fps"] == 30
    assert clip["size"] == (1920, 1080)

    assert Video.get_length("x.mp4") == 12.5
    assert Video.get_fps("x.mp4") == 30
    assert Video.get_resolution("x.mp4") == (1920, 1080)

    from commands.const import KiB
    assert Video.get_bitrate("x.mp4") == 123 * KiB
    assert Video.get_audio_bitrate("x.mp4") == 45 * KiB
    assert isinstance(Video.get_info("x.mp4"), _DummyClip)


def test_video_instance_wrappers_call_classmethods(monkeypatch):
    v = Video("x.mp4")
    monkeypatch.setattr(Video, "get_length", classmethod(lambda cls, path: ("len", path)))
    monkeypatch.setattr(Video, "get_fps", classmethod(lambda cls, path: ("fps", path)))
    monkeypatch.setattr(Video, "get_resolution", classmethod(lambda cls, path: ("res", path)))
    monkeypatch.setattr(Video, "get_bitrate", classmethod(lambda cls, path: ("bit", path)))
    monkeypatch.setattr(Video, "get_audio_bitrate", classmethod(lambda cls, path: ("abit", path)))
    monkeypatch.setattr(Video, "get_info", classmethod(lambda cls, path: ("info", path)))
    monkeypatch.setattr(Video, "get_clip", classmethod(lambda cls, path, raw=False: ("clip", path, raw)))

    assert v.length() == ("len", "x.mp4")
    assert v.fps() == ("fps", "x.mp4")
    assert v.resolution() == ("res", "x.mp4")
    assert v.bitrate() == ("bit", "x.mp4")
    assert v.audio_bitrate() == ("abit", "x.mp4")
    assert v.info() == ("info", "x.mp4")
    assert v.clip(raw=True) == ("clip", "x.mp4", True)
