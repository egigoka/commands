#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with ffmpeg
"""
__version__ = "0.0.4"


class FFMpeg:
    @staticmethod
    def add_subtitles_to_mkv(input_file: str, subs: dict, output_file: str):
        from .console9 import Console
        from .dict9 import Dict
        from .id9 import ID

        subs_names_str = ''
        subs_meta_str = ''
        subs_meta_id = ID()
        for name, lang in Dict.iterable(subs):
           subs_names_str += f'-i "{name}" '
           subs_meta_str += f'-metadata:s:s:{subs_meta_id.get()} language={lang} '

        maps_str = ''
        for i in range(len(subs)+1):
            maps_str += f'-map {i} '

        command = f'ffmpeg -i "{input_file}" {subs_names_str.strip()} {maps_str.strip()} -c copy {subs_meta_str.strip()} "{output_file}"'

        print(command)

        Console.get_output(command, print_std=True)
