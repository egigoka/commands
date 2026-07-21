# Consolidated tests for commands/video.py (unit)

# ---- from test_video9.py ----


import json
import types

import pytest


def _probe_info():
    return {
        "streams": [
            {
                "codec_type": "video",
                "width": 1920,
                "height": 1080,
                "avg_frame_rate": "30/1",
                "bit_rate": "5000000",
            },
            {"codec_type": "audio", "bit_rate": "320000"},
        ],
        "format": {"duration": "120.5", "bit_rate": "5320000"},
    }


def test_video9_import():
    from commands import Video
    assert Video is not None


def test_video_probe_calls_ffprobe(monkeypatch):
    import commands.video as video_module
    from commands.video import Video

    called = {}

    def fake_run(command, **kwargs):
        called["command"] = command
        called["kwargs"] = kwargs
        return types.SimpleNamespace(stdout=json.dumps(_probe_info()))

    monkeypatch.setattr(video_module, "subprocess", types.SimpleNamespace(run=fake_run))

    assert Video._probe("input.mp4") == _probe_info()
    assert called["command"][0:3] == ["ffprobe", "-v", "error"]
    assert called["command"][-1] == "input.mp4"
    assert called["kwargs"] == {"capture_output": True, "check": True, "text": True}


# Coverage improvement tests
class TestVideoCoverage:
    """Tests to improve coverage for video9.py"""

    def test_get_clip_basic(self, monkeypatch):
        """Test Video.get_clip without raw flag (lines 14-23)"""
        from commands.video import Video
        monkeypatch.setattr(Video, "_probe", classmethod(lambda cls, path: _probe_info()))

        result = Video.get_clip("test.mp4", raw=False)

        assert result["duration"] == 120.5
        assert result["fps"] == 30.0
        assert result["size"] == (1920, 1080)

    def test_get_clip_raw(self, monkeypatch):
        """Test Video.get_clip with raw=True (lines 16-17)"""
        from commands.video import Video
        info = _probe_info()
        monkeypatch.setattr(Video, "_probe", classmethod(lambda cls, path: info))

        result = Video.get_clip("test.mp4", raw=True)
        assert result is info

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
        monkeypatch.setattr(Video, "get_info", classmethod(lambda cls, path: _probe_info()))

        result = Video.get_bitrate("test.mp4")
        assert result == 5000000

    def test_get_audio_bitrate(self, monkeypatch):
        """Test Video.get_audio_bitrate (lines 42-45)"""
        from commands.video import Video
        monkeypatch.setattr(Video, "get_info", classmethod(lambda cls, path: _probe_info()))

        result = Video.get_audio_bitrate("test.mp4")
        assert result == 320000

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
        info = _probe_info()
        monkeypatch.setattr(Video, "_probe", classmethod(lambda cls, path: info))

        result = Video.get_info("test.mp4")
        assert result is info

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


from commands.video import Video


def test_video_class_getters_with_mocked_ffprobe(monkeypatch):
    info = _probe_info()
    monkeypatch.setattr(Video, "_probe", classmethod(lambda cls, path: info))

    clip_raw = Video.get_clip("x.mp4", raw=True)
    assert clip_raw is info

    clip = Video.get_clip("x.mp4", raw=False)
    assert clip["duration"] == 120.5
    assert clip["fps"] == 30
    assert clip["size"] == (1920, 1080)

    assert Video.get_length("x.mp4") == 120.5
    assert Video.get_fps("x.mp4") == 30
    assert Video.get_resolution("x.mp4") == (1920, 1080)

    assert Video.get_bitrate("x.mp4") == 5000000
    assert Video.get_audio_bitrate("x.mp4") == 320000
    assert Video.get_info("x.mp4") is info


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
