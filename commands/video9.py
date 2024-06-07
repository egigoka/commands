#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with video
"""
__version__ = "0.2.0"


class Video:
    """Class to work with video
    """

    @staticmethod
    def get_clip(path, raw = False):
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(path)
        if raw:
            return clip
        outclip = {"duration": clip.duration,
                   "fps": clip.fps,
                   "size": clip.size
                   }
        del clip
        return outclip

    @classmethod
    def get_length(cls, path):
        clip = cls.get_clip(path)
        return clip["duration"]

    @classmethod
    def get_fps(cls, path):
        clip = cls.get_clip(path)
        return clip["fps"]

    @classmethod
    def get_bitrate(cls, path):
        from .const9 import KiB
        clip = cls.get_clip(path, raw=True)
        return clip.reader.bitrate * KiB

    @classmethod
    def get_audio_bitrate(cls, path):
        from .const9 import KiB
        clip = cls.get_clip(path, raw=True)
        return clip.audio.reader.bitrate * KiB

    @classmethod
    def get_resolution(cls, path):
        clip = cls.get_clip(path)
        return clip["size"]

    @classmethod
    def get_info(cls, path):
        return cls.get_clip(path, raw=True)

