#! python3
# -*- coding: utf-8 -*-
from typing import Union

"""Internal module with functions for print to console.
"""
__version__ = "0.13.0"


class __Print:
    """Class with functions for print to console.
    """

    def __init__(self):
        from threading import Lock
        self.s_print_lock = Lock()
        self.colorama_inited = False
        self._color_output_enabled = None

    def __call__(self, *args, **kwargs) -> None:
        self.multithread_safe(*args, **kwargs)

    def multithread_safe(self, *args, **kwargs) -> None:
        """Thread safe print function"""
        with self.s_print_lock:
            print(*args, **kwargs)

    def debug(self, *strings: Union[str, bytes], raw: bool = False) -> None:
        """More notable print, used only for debugging
        <br>`param strings` prints separately
        <br>`param raw` print representation of strings
        <br>`return`
        """
        from .console9 import Console
        line = "-" * Console.width()
        self.multithread_safe("<<<Debug sheet:>>>")
        for str_ in strings:
            self.multithread_safe(line, end="")
            if raw:
                self.multithread_safe(repr(str_))
            else:
                self.multithread_safe(str_)
            self.multithread_safe(line)
        self.multithread_safe("<<<End of debug sheet>>>")

    def rewrite(self, *strings: str, sep: str = " ", fit: bool = True) -> None:
        """Print rewritable string. note, that you need to rewrite string to remove previous characters
        <br>`param strings` work as builtin print()
        <br>`param sep` sep as builtin print(sep)
        <br>`param fit` try to fit output in one line
        """
        from .os9 import OS
        from .console9 import Console
        line = " " * Console.width()
        if OS.windows:  # windows add symbol to end of string :(
            line = line[:-1]
        self.multithread_safe(line, end="\r")
        if fit:
            strings = Console.fit(*strings, sep=sep)
        self.multithread_safe(*strings, sep=sep, end="\r")

    def prettify(self, object_: Union[list, dict, tuple], indent: int = 4, quiet: bool = False) -> str:
        """Pretty print of list, dicts, tuples
        <br>`param object_` object to print
        <br>`param indent` indent to new nested level
        <br>`param quiet` suppress print to console
        <br>`return` from pprint.pformat
        """
        import pprint
        pretty_printer = pprint.PrettyPrinter(indent=indent)
        pretty_string = pretty_printer.pformat(object=object_)
        if not quiet:
            self.multithread_safe(pretty_string)
        return pretty_string

    @property
    def color_output_enabled(self):
        if self._color_output_enabled is None:
            from .os9 import OS
            self._color_output_enabled = "NO_COLOR" not in OS.env.keys()
        return self._color_output_enabled

    def colored(self, *strings: Union[str, int, list, dict], attributes: list = None, end: str = "\n",
                sep: str = " ", flush: bool = False, verbose: bool = True) -> None:
        """Wrapper for termcolor.cprint, added some smartness
        <br>Usage` Print.colored("text1", "text2", "red") or Print.colored("text", "text2", "red", "on_white")
        <br>even Print.colored("text", "text2", "on_white", "red") now.
        You can pick colors from termcolor.COLORS, highlights from termcolor.HIGHLIGHTS.
        When environment variable NO_COLOR present (regardless of its value), prevents the addition of ANSI color.
        <br>`param strings` work as builtin print(*strings)
        <br>`param attributes` going to termcolor.cprint(attrs) argument
        <br>`param end` same as builtin print(end)
        <br>`param sep` same as builtin print(sep)
        <br>`param flush` same as builtin print(flush)
        """
        import termcolor
        from contextlib import suppress
        from .list9 import List
        termcolor.COLORS["gray"] = termcolor.COLORS["black"] = 30
        termcolor.HIGHLIGHTS["on_gray"] = termcolor.HIGHLIGHTS["on_black"] = 40
        from .os9 import OS
        if OS.windows and not self.colorama_inited and self.color_output_enabled:
            import colorama
            colorama.init()
            self.colorama_inited = True
        # check for colors in input
        highlight = None
        color = None
        color_args = 0
        try:
            if str(strings[-1]) in termcolor.HIGHLIGHTS:
                highlight = strings[-1]
                color_args += 1
                if str(strings[-2]) in termcolor.COLORS:
                    color = strings[-2]
                    color_args += 1
            elif str(strings[-1]) in termcolor.COLORS:
                color = strings[-1]
                color_args += 1
                if str(strings[-2]) in termcolor.HIGHLIGHTS:
                    highlight = strings[-2]
                    color_args += 1
        except KeyError:
            pass
        # create single string to pass it into termcolor
        string = ""
        if color_args:
            strings = strings[:-color_args]

        strings = List.to_strings(strings)

        string = sep.join(strings)

        if self.color_output_enabled:
            colored_string = termcolor.colored(string, color=color, on_color=highlight, attrs=attributes)
        else:
            colored_string = string
        if verbose:
            self.multithread_safe(colored_string, end=end, flush=flush)

        with suppress(KeyError):  # for work with multithreading
            termcolor.COLORS.pop("gray")
            termcolor.COLORS.pop("black")
            termcolor.HIGHLIGHTS.pop("on_gray")
            termcolor.HIGHLIGHTS.pop("on_black")

        return colored_string


Print = __Print()
