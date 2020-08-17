#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with ffmpeg
"""
__version__ = "0.5.0"


class FFMpeg:

    class MetadataTypes:
        subtitles = "s"
        audio = "a"

    @staticmethod
    def add_something_to_mkv(input_file: str, additional_files: dict,
                             output_file: str, metadata_type: str, existed_langs: list = ()):
        import os
        from .console9 import Console
        from .dict9 import Dict
        from .id9 import ID

        names_list = []
        meta_list = []
        meta_id = ID()

        for lang in existed_langs:
            meta_list += [f'-metadata:s:{metadata_type}:{meta_id.get()}', f'language={lang}']

        for name, lang in Dict.iterable(additional_files):
            names_list += ['-i', name]
            meta_list += [f'-metadata:s:{metadata_type}:{meta_id.get()}', f'language={lang}']

        maps_list = []
        for i in range(len(additional_files) + 1):
            maps_list += ['-map', i]

        commands = ["ffmpeg", "-y", "-i", input_file] + names_list + maps_list + ["-c", "copy"] + meta_list + [
            output_file]

        Console.get_output(commands, print_std=True)


    @classmethod
    def add_subtitles_to_mkv(cls, input_file: str, subs: dict, output_file: str, existed_langs: list = ()):
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=subs,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.subtitles)

    @classmethod
    def add_audio_to_mkv(cls, input_file: str, audio: dict, output_file: str, existed_langs: list = ()):
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=audio,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.audio)

    @staticmethod
    def convert_avi_to_mkv(input_file, output_file):
        from .console9 import Console

        commands = ["ffmpeg", "-y", "-fflags", "+genpts", "-i", input_file, "-c:v", "copy", "-c:a", "copy", "-map", "0", output_file]
        Console.get_output(commands, print_std=True)

    @staticmethod
    def convert_to_mkv(input_file, output_file):
        from .console9 import Console

        commands = ["ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "copy", "-map", "0", output_file]
        Console.get_output(commands, print_std=True)