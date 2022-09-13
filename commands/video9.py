#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with video
"""
__version__ = "0.0.1"


class Video:
    """Class to work with video
    """

    @staticmethod
    def get_clip(path):
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(path)
        return clip

    @classmethod
    def get_length(cls, path):
        clip = cls.get_clip(path)
        return clip.duration

    @classmethod
    def get_fps(cls, path):
        clip = cls.get_clip(path)
        return clip.fps

    @classmethod
    def get_resolution(cls, path):
        clip = cls.get_clip(path)
        return clip.size

    @classmethod
    def get_info(cls, path):
        return cls.get_clip(path)

