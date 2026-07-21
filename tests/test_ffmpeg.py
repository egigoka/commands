# Consolidated tests for commands/ffmpeg.py (unit)

# ---- from test_ffmpeg9.py ----


import pytest
from commands.ffmpeg import FFMpeg


def test_ffmpeg_import():
    from commands import FFMpeg as FF
    assert FF is not None






def test_ffmpeg_class_add_subtitles(monkeypatch):
    calls = {}
    monkeypatch.setattr(FFMpeg, "add_something_to_mkv",
                        lambda **kwargs: calls.update(kwargs))
    FFMpeg.add_subtitles_to_mkv("in.mkv", {"sub.srt": "en"}, "out.mkv")
    assert calls["input_file"] == "in.mkv"
    assert calls["output_file"] == "out.mkv"
    assert calls["metadata_type"] == FFMpeg.MetadataTypes.subtitles


def test_ffmpeg_class_add_audio(monkeypatch):
    calls = {}
    monkeypatch.setattr(FFMpeg, "add_something_to_mkv",
                        lambda **kwargs: calls.update(kwargs))
    FFMpeg.add_audio_to_mkv("in.mkv", {"aud.wav": "en"}, "out.mkv")
    assert calls["metadata_type"] == FFMpeg.MetadataTypes.audio


def test_ffmpeg_convert_avi_to_mkv(monkeypatch):
    from commands.console import Console
    called = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: called.update({"args": a, "kwargs": k}))
    FFMpeg.convert_avi_to_mkv("in.avi", "out.mkv")
    assert "ffmpeg" in called["args"][0][0]


def test_ffmpeg_convert_to_mkv(monkeypatch):
    from commands.console import Console
    called = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: called.update({"args": a, "kwargs": k}))
    FFMpeg.convert_to_mkv("in.avi", "out.mkv")
    assert "ffmpeg" in called["args"][0][0]




# ---- from test_ffmpeg_coverage.py ----


import pytest
from commands.ffmpeg import FFMpeg
from unittest.mock import MagicMock, patch


class TestFFmpegCoverage:
    """Tests to improve FFmpeg module coverage"""

    def test_subtitles_instance_method(self, monkeypatch):
        """Test FFMpeg.subtitles instance method (line 34)"""
        # Mock the class method that it delegates to
        mock_add_subtitles = MagicMock(return_value="success")
        monkeypatch.setattr(FFMpeg, "add_subtitles_to_mkv", mock_add_subtitles)

        ff = FFMpeg(input_file="input.mkv", output_file="output.mkv")
        result = ff.subtitles(subs=["sub1.srt"], output_file="custom_output.mkv")

        # Verify the class method was called with correct parameters
        mock_add_subtitles.assert_called_once()
        call_args = mock_add_subtitles.call_args
        assert call_args.kwargs['input_file'] == "input.mkv"
        assert call_args.kwargs['subs'] == ["sub1.srt"]
        assert call_args.kwargs['output_file'] == "custom_output.mkv"

    def test_audio_instance_method(self, monkeypatch):
        """Test FFMpeg.audio instance method (lines 43-44)"""
        # Mock the class method that it delegates to
        mock_add_audio = MagicMock(return_value="success")
        monkeypatch.setattr(FFMpeg, "add_audio_to_mkv", mock_add_audio)

        ff = FFMpeg(input_file="input.mkv", output_file="output.mkv")
        result = ff.audio(audio=["audio1.mp3"], output_file="custom_output.mkv")

        # Verify the class method was called with correct parameters
        mock_add_audio.assert_called_once()
        call_args = mock_add_audio.call_args
        assert call_args.kwargs['input_file'] == "input.mkv"
        assert call_args.kwargs['audio'] == ["audio1.mp3"]
        assert call_args.kwargs['output_file'] == "custom_output.mkv"

    def test_convert_avi_to_mkv_verbose(self, monkeypatch, capsys):
        """Test FFMpeg.convert_avi_to_mkv with verbose=True (line 124)"""
        # Mock Console.get_output to avoid actual execution
        import commands.console
        mock_get_output = MagicMock(return_value="")
        monkeypatch.setattr(commands.console.Console, "get_output", mock_get_output)

        # Call with verbose=True to trigger print statement on line 124
        FFMpeg.convert_avi_to_mkv("input.mkv", "output.mkv", verbose=True)

        # Verify the print statement was executed
        captured = capsys.readouterr()
        assert "ffmpeg" in captured.out
        assert "input.mkv" in captured.out
        assert "output.mkv" in captured.out

    def test_convert_to_mkv_verbose(self, monkeypatch, capsys):
        """Test FFMpeg.convert_to_mkv with verbose=True (line 133)"""
        # Mock Console.get_output to avoid actual execution
        import commands.console
        mock_get_output = MagicMock(return_value="")
        monkeypatch.setattr(commands.console.Console, "get_output", mock_get_output)

        # Call with verbose=True to trigger print statement on line 133
        FFMpeg.convert_to_mkv("input.avi", "output.mkv", verbose=True)

        # Verify the print statement was executed
        captured = capsys.readouterr()
        assert "ffmpeg" in captured.out
        assert "input.avi" in captured.out
        assert "output.mkv" in captured.out


# ---- from test_ffmpeg_extra.py ----


import pytest

from commands.ffmpeg import FFMpeg




def test_ffmpeg_add_something_builds_commands(monkeypatch):
    captured = {}

    class DummyID:
        def __init__(self):
            self.i = 0

        def get(self):
            val = self.i
            self.i += 1
            return val

    def fake_get_output(cmds, *args, **kwargs):
        captured["commands"] = cmds
        captured["kwargs"] = kwargs

    debug_calls = []
    monkeypatch.setattr("commands.id.ID", DummyID)
    monkeypatch.setattr("commands.console.Console.get_output", fake_get_output)
    monkeypatch.setattr("commands.print.Print.colored", lambda *a, **k: debug_calls.append(a))

    FFMpeg.add_something_to_mkv(
        input_file="in.mkv",
        additional_files={"sub1.srt": "en", "sub2.srt": "fr"},
        output_file="out.mkv",
        metadata_type=FFMpeg.MetadataTypes.subtitles,
        existed_langs=["es"],
        debug=True,
    )

    assert captured["commands"][0] == "ffmpeg"
    # expect two additional inputs + original
    assert captured["commands"].count("-i") == 3
    # meta language flags include existed_langs + two inputs
    assert any(isinstance(part, str) and "language=en" in part for part in captured["commands"])
    assert debug_calls  # debug branch exercised


def test_ffmpeg_instance_shortcuts(monkeypatch):
    called = {}

    def fake_convert_avi(**kwargs):
        called["avi"] = kwargs

    def fake_convert_mkv(**kwargs):
        called["mkv"] = kwargs

    monkeypatch.setattr(FFMpeg, "convert_avi_to_mkv", staticmethod(fake_convert_avi))
    monkeypatch.setattr(FFMpeg, "convert_to_mkv", staticmethod(fake_convert_mkv))

    ff = FFMpeg(input_file="in.avi", output_file="out.mkv")
    ff.avi_to_mkv(verbose=True)
    ff.mkv(verbose=True)

    assert called["avi"]["input_file"] == "in.avi"
    assert called["avi"]["output_file"] == "out.mkv"
    assert called["mkv"]["input_file"] == "in.avi"
    assert called["mkv"]["output_file"] == "out.mkv"
