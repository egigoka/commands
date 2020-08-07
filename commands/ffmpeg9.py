#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with ffmpeg
"""
__version__ = "0.0.8"


class FFMpeg:
    @staticmethod
    def add_subtitles_to_mkv(input_file: str, subs: dict, output_file: str):
        from .console9 import Console
        from .dict9 import Dict
        from .id9 import ID

        subs_names_list = []
        subs_meta_list = []
        subs_meta_id = ID()
        for name, lang in Dict.iterable(subs):
            subs_names_list += ['-i', name]
            subs_meta_list += [f'-metadata:s:s:{subs_meta_id.get()}', f'language={lang}']

        maps_list = []
        for i in range(len(subs)+1):
            maps_list += ['-map', i]

        commands = ["ffmpeg", "-i", input_file] + subs_names_list + maps_list + ["-c", "copy"] + subs_meta_list + [output_file]

        Console.get_output(commands, print_std=True)
