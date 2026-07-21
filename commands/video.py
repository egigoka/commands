#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with video."""
from __future__ import annotations

from typing import Any, Optional, Tuple, TypedDict, cast

from .module import LazyModule

__version__ = "0.2.1"

json = LazyModule("json")
subprocess = LazyModule("subprocess")


class Video:
    """Class to work with video."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path

    def _ensure(self) -> None:
        if not self.path:
            raise ValueError("Video path is not set")

    def clip(self, raw: bool = False) -> Any:
        """Get summarized or raw ffprobe information."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_clip(self.path, raw=raw)

    def length(self) -> float:
        """Get video length in seconds."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_length(self.path)

    def fps(self) -> float:
        """Get frames per second for the video."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_fps(self.path)

    def bitrate(self) -> float:
        """Get video bitrate in bits per second."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_bitrate(self.path)

    def audio_bitrate(self) -> float:
        """Get audio bitrate in bits per second."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_audio_bitrate(self.path)

    def resolution(self) -> Tuple[int, int]:
        """Get video resolution as [width, height]."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_resolution(self.path)

    def info(self) -> Any:
        """Get raw clip info for the video."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_info(self.path)

    class _ClipInfo(TypedDict):
        duration: float
        fps: float
        size: Tuple[int, int]

    @classmethod
    def _probe(cls, path: str) -> dict[str, Any]:
        """Return ffprobe metadata for a media file."""
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries",
                "format=duration,bit_rate:stream=codec_type,width,height,avg_frame_rate,r_frame_rate,bit_rate",
                "-of", "json",
                path,
            ],
            capture_output=True,
            check=True,
            text=True,
        )
        return cast(dict[str, Any], json.loads(result.stdout))

    @staticmethod
    def _stream(info: dict[str, Any], codec_type: str) -> dict[str, Any]:
        """Return first stream matching codec type."""
        for stream in info.get("streams", []):
            if stream.get("codec_type") == codec_type:
                return cast(dict[str, Any], stream)
        raise ValueError(f"ffprobe returned no {codec_type} stream")

    @staticmethod
    def _rate(stream: dict[str, Any]) -> float:
        """Convert an ffprobe frame-rate value to float."""
        value = str(stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0")
        numerator, separator, denominator = value.partition("/")
        if not separator:
            return float(numerator)
        if float(denominator) == 0:
            return 0.0
        return float(numerator) / float(denominator)

    @classmethod
    def get_clip(cls, path: str, raw: bool = False) -> Any:
        """Load summarized or raw ffprobe information."""
        info = cls._probe(path)
        if raw:
            return info
        stream = cls._stream(info, "video")
        duration = info.get("format", {}).get("duration") or stream.get("duration")
        if duration is None:
            raise ValueError("ffprobe returned no video duration")
        outclip: Video._ClipInfo = {
            "duration": float(duration),
            "fps": cls._rate(stream),
            "size": (int(stream["width"]), int(stream["height"])),
        }
        return outclip

    @classmethod
    def get_length(cls, path: str) -> float:
        """Get video length in seconds."""
        clip = cls.get_clip(path)
        return cast(float, clip["duration"])

    @classmethod
    def get_fps(cls, path: str) -> float:
        """Get frames per second for the video."""
        clip = cls.get_clip(path)
        return cast(float, clip["fps"])

    @classmethod
    def get_bitrate(cls, path: str) -> float:
        """Get video bitrate in bits per second."""
        info = cls.get_info(path)
        stream = cls._stream(info, "video")
        bitrate = stream.get("bit_rate") or info.get("format", {}).get("bit_rate")
        if bitrate is None:
            raise ValueError("ffprobe returned no video bitrate")
        return float(bitrate)

    @classmethod
    def get_audio_bitrate(cls, path: str) -> float:
        """Get audio bitrate in bits per second."""
        info = cls.get_info(path)
        stream = cls._stream(info, "audio")
        bitrate = stream.get("bit_rate")
        if bitrate is None:
            raise ValueError("ffprobe returned no audio bitrate")
        return float(bitrate)

    @classmethod
    def get_resolution(cls, path: str) -> Tuple[int, int]:
        """Get video resolution as [width, height]."""
        clip = cls.get_clip(path)
        return cast(Tuple[int, int], clip["size"])

    @classmethod
    def get_info(cls, path: str) -> Any:
        """Get raw clip info for the video."""
        return cls._probe(path)
