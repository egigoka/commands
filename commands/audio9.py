#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64
"""
__version__ = "0.0.1"


class Audio:
    """Class to work with audio"""

    @staticmethod
    def get_mutagen_handle(path):
        import mutagen
        return mutagen.File(path)

    @classmethod
    def get_audio_bitrate(cls, path):
        handle = cls.get_mutagen_handle(path)
        return handle.info.bitrate
