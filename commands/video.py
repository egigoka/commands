#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with video."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Literal, Optional, Tuple, TypedDict, overload

from .module import LazyModule, LazyProperty

__version__ = "0.2.1"

moviepy = LazyModule("moviepy")
KiB = LazyProperty(".const", "KiB")
if not TYPE_CHECKING:
    typing = LazyModule("typing")
    TypedDict = getattr(typing, "TypedDict", dict)
    overload = typing.overload


class Video:
    """Class to work with video."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path

    def _ensure(self) -> None:
        if not self.path:
            raise ValueError("Video path is not set")

    def clip(self, raw: bool = False) -> Any:
        """Get clip info or a raw VideoFileClip object."""
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
        """Get video bitrate in bytes per second."""
        self._ensure()
        assert self.path is not None
        return self.__class__.get_bitrate(self.path)

    def audio_bitrate(self) -> float:
        """Get audio bitrate in bytes per second."""
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

    @overload
    @classmethod
    def get_clip(cls, path: str, raw: Literal[False] = False) -> "_ClipInfo":
        ...

    @overload
    @classmethod
    def get_clip(cls, path: str, raw: Literal[True]) -> Any:
        ...

    @overload
    @classmethod
    def get_clip(cls, path: str, raw: bool) -> Any:
        ...

    @classmethod
    def get_clip(cls, path: str, raw: bool = False) -> Any:
        """Load a clip and optionally return its raw object."""
        clip = moviepy.VideoFileClip(path)
        if raw:
            return clip
        width, height = clip.size
        outclip: Video._ClipInfo = {
            "duration": float(clip.duration),
            "fps": float(clip.fps),
            "size": (int(width), int(height)),
        }
        del clip
        return outclip

    @classmethod
    def get_length(cls, path: str) -> float:
        """Get video length in seconds."""
        clip = cls.get_clip(path)
        return clip["duration"]

    @classmethod
    def get_fps(cls, path: str) -> float:
        """Get frames per second for the video."""
        clip = cls.get_clip(path)
        return clip["fps"]

    @classmethod
    def get_bitrate(cls, path: str) -> float:
        """Get video bitrate in bytes per second."""
        clip = cls.get_clip(path, raw=True)
        return float(clip.reader.bitrate) * float(KiB)

    @classmethod
    def get_audio_bitrate(cls, path: str) -> float:
        """Get audio bitrate in bytes per second."""
        clip = cls.get_clip(path, raw=True)
        return float(clip.audio.reader.bitrate) * float(KiB)

    @classmethod
    def get_resolution(cls, path: str) -> Tuple[int, int]:
        """Get video resolution as [width, height]."""
        clip = cls.get_clip(path)
        return clip["size"]

    @classmethod
    def get_info(cls, path: str) -> Any:
        """Get raw clip info for the video."""
        return cls.get_clip(path, raw=True)
