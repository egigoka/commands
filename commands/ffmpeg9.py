#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with ffmpeg
"""
__version__ = "0.5.4"


class FFMpeg:

    class MetadataTypes:
        subtitles = "s"
        audio = "a"

    @staticmethod
    def add_something_to_mkv(input_file: str, additional_files: dict,
                             output_file: str, metadata_type: str, existed_langs: list = (), debug: bool = False):
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

        if debug:
            from .print9 import Print
            from .list9 import List
            Print.colored(f"commands={commands}", "red")
            Print.colored('" "'.join(List.to_strings(commands)), "magenta")

        Console.get_output(commands, print_std=True, debug=debug)

    @classmethod
    def add_subtitles_to_mkv(cls, input_file: str, subs: dict, output_file: str, existed_langs: list = (),
                             debug: bool = False):
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=subs,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.subtitles,
                                 debug=debug)

    @classmethod
    def add_audio_to_mkv(cls, input_file: str, audio: dict, output_file: str, existed_langs: list = (),
                         debug: bool = False):
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=audio,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.audio,
                                 debug=debug)

    @staticmethod
    def convert_avi_to_mkv(input_file, output_file, verbose=False):
        from .console9 import Console

        commands = ["ffmpeg", "-y", "-fflags", "+genpts", "-i", input_file, "-c:v", "copy", "-c:a", "copy", "-map", "0",
                    output_file]
        if verbose:
            print(" ".join(commands))
        Console.get_output(commands, print_std=True)

    @staticmethod
    def convert_to_mkv(input_file, output_file, verbose=False):
        from .console9 import Console

        commands = [f'ffmpeg -i "{input_file}" -c:v copy -c:a copy -map 0 "{output_file}"']
        if verbose:
            print(" ".join(commands))
        Console.get_output(commands, print_std=True, pure_shell=True)
