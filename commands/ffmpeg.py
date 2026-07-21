#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with ffmpeg."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Sequence
__version__ = "0.5.4"
Console = LazyProperty(".console", "Console")
Dict = LazyProperty(".dict", "Dict")
ID = LazyProperty(".id", "ID")
Print = LazyProperty(".print", "Print")
List = LazyProperty(".list", "List")


class FFMpeg:
    """Helper methods for common ffmpeg operations."""

    class MetadataTypes:
        """Metadata stream type identifiers."""

        subtitles = "s"
        audio = "a"

    def __init__(self, input_file: Optional[str] = None, output_file: Optional[str] = None) -> None:
        self.input_file: Optional[str] = input_file
        self.output_file: Optional[str] = output_file

    def _input(self, input_file: Optional[str]) -> str:
        input_file = input_file or self.input_file
        if not input_file:
            raise ValueError("input_file must be set")
        return input_file

    def _output(self, output_file: Optional[str]) -> str:
        output_file = output_file or self.output_file
        if not output_file:
            raise ValueError("output_file must be set")
        return output_file

    def subtitles(
        self,
        subs: dict[str, str],
        output_file: Optional[str] = None,
        existed_langs: Sequence[str] = (),
        debug: bool = False
    ) -> None:
        """Add subtitles to MKV using stored input/output when not provided."""
        input_file = self._input(None)
        output_file = self._output(output_file)
        return self.add_subtitles_to_mkv(input_file=input_file,
                                         subs=subs,
                                         output_file=output_file,
                                         existed_langs=existed_langs,
                                         debug=debug)

    def audio(
        self,
        audio: dict[str, str],
        output_file: Optional[str] = None,
        existed_langs: Sequence[str] = (),
        debug: bool = False
    ) -> None:
        """Add audio tracks using stored input/output when not provided."""
        input_file = self._input(None)
        output_file = self._output(output_file)
        return self.add_audio_to_mkv(input_file=input_file,
                                     audio=audio,
                                     output_file=output_file,
                                     existed_langs=existed_langs,
                                     debug=debug)

    def avi_to_mkv(
        self,
        input_file: Optional[str] = None,
        output_file: Optional[str] = None,
        verbose: bool = False
    ) -> None:
        """Convert AVI to MKV using stored input/output when not provided."""
        input_file = self._input(input_file)
        output_file = self._output(output_file)
        return self.convert_avi_to_mkv(input_file=input_file,
                                       output_file=output_file,
                                       verbose=verbose)

    def mkv(
        self,
        input_file: Optional[str] = None,
        output_file: Optional[str] = None,
        verbose: bool = False
    ) -> None:
        """Convert to MKV using stored input/output when not provided."""
        input_file = self._input(input_file)
        output_file = self._output(output_file)
        return self.convert_to_mkv(input_file=input_file,
                                   output_file=output_file,
                                   verbose=verbose)

    @classmethod
    def add_something_to_mkv(
        cls,
        input_file: str,
        additional_files: dict[str, str],
        output_file: str,
        metadata_type: str,
        existed_langs: Sequence[str] = (),
        debug: bool = False
    ) -> None:
        """Add extra streams to an MKV with metadata."""
        names_list: list[str] = []
        meta_list: list[str] = []
        meta_id = ID()

        for lang in existed_langs:
            meta_list += [f'-metadata:s:{metadata_type}:{meta_id.get()}', f'language={lang}']

        for name, lang in Dict.iterable(additional_files):
            names_list += ['-i', name]
            meta_list += [f'-metadata:s:{metadata_type}:{meta_id.get()}', f'language={lang}']

        maps_list: list[str] = []
        for i in range(len(additional_files) + 1):
            maps_list += ['-map', str(i)]

        commands = ["ffmpeg", "-y", "-i", input_file] + names_list + maps_list + ["-c", "copy"] + meta_list + [
            output_file]

        if debug:
            Print.colored(f"commands={commands}", "red")
            Print.colored('" "'.join(List.to_strings(commands)), "magenta")

        Console.get_output(commands, print_std=True, debug=debug)

    @classmethod
    def add_subtitles_to_mkv(
        cls,
        input_file: str,
        subs: dict[str, str],
        output_file: str,
        existed_langs: Sequence[str] = (),
        debug: bool = False
    ) -> None:
        """Add subtitle streams to an MKV."""
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=subs,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.subtitles,
                                 debug=debug)

    @classmethod
    def add_audio_to_mkv(
        cls,
        input_file: str,
        audio: dict[str, str],
        output_file: str,
        existed_langs: Sequence[str] = (),
        debug: bool = False
    ) -> None:
        """Add audio streams to an MKV."""
        cls.add_something_to_mkv(input_file=input_file,
                                 additional_files=audio,
                                 output_file=output_file,
                                 existed_langs=existed_langs,
                                 metadata_type=FFMpeg.MetadataTypes.audio,
                                 debug=debug)

    @classmethod
    def convert_avi_to_mkv(cls, input_file: str, output_file: str, verbose: bool = False) -> None:
        """Convert an AVI file to MKV without re-encoding."""
        commands = ["ffmpeg", "-y", "-fflags", "+genpts", "-i", input_file, "-c:v", "copy", "-c:a", "copy", "-map", "0",
                    output_file]
        if verbose:
            print(" ".join(commands))
        Console.get_output(commands, print_std=True)

    @classmethod
    def convert_to_mkv(cls, input_file: str, output_file: str, verbose: bool = False) -> None:
        """Convert a media file to MKV without re-encoding."""
        commands = [f'ffmpeg -i "{input_file}" -c:v copy -c:a copy -map 0 "{output_file}"']
        if verbose:
            print(" ".join(commands))
        Console.get_output(commands, print_std=True, pure_shell=True)
