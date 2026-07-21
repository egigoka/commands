#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for print to console."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pprint
    from contextlib import suppress
    from threading import Lock
    from typing import Any, List, Optional, Sequence, Tuple, Union, cast
    from .console import Console
    from .list import List as ListUtils
    from .os import OS as OSClass
    OS = OSClass()
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty

__version__ = "0.13.0"
if not TYPE_CHECKING:
    pprint = LazyModule("pprint")
    Lock = LazyProperty("threading", "Lock")
    Console = LazyProperty(".console", "Console")
    OS = LazyProperty(".os", "OS")
    suppress = LazyProperty("contextlib", "suppress")
    ListUtils = LazyProperty(".list", "List")

termcolor = LazyModule("termcolor")
colorama = LazyModule("colorama", optional=True)


class __Print:
    """Class with functions for print to console."""

    def __init__(self) -> None:
        self.s_print_lock = Lock()
        self.colorama_inited = False
        self._color_output_enabled: Optional[bool] = None
        self._prefix: Optional[str] = None

    def prefix(self, *args: Any, sep: str = " ") -> "__Print":
        """Return a Print instance that prefixes all output with given strings."""
        clone = self.__class__()
        clone._prefix = sep.join(map(str, args))
        return clone

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        if self._prefix:
            args = (self._prefix, *args)
        self.multithread_safe(*args, **kwargs)

    def multithread_safe(self, *args: Any, **kwargs: Any) -> None:
        """Print with a thread-safe lock."""
        with self.s_print_lock:
            print(*args, **kwargs)

    def debug(self, *strings: Union[str, bytes], raw: bool = False) -> None:
        """Print a debug sheet.

        <br>`param strings` prints separately
        <br>`param raw` print representation of strings
        <br>`return`
        """
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
        """Print a rewritable line.

        <br>`param strings` work as builtin print()
        <br>`param sep` sep as builtin print(sep)
        <br>`param fit` try to fit output in one line
        """
        line = " " * Console.width()
        if OS.windows:  # windows add symbol to end of string :(
            line = line[:-1]
        self.multithread_safe(line, end="\r")
        strings_out: Sequence[str]
        if fit:
            strings_out = Console.fit(*strings, sep=sep)
        else:
            strings_out = strings
        self.multithread_safe(*strings_out, sep=sep, end="\r")

    def prettify(self, object_: Union[list, dict, tuple], indent: int = 4, verbose: bool = True) -> str:  # type: ignore[type-arg]
        """Pretty print lists, dicts, and tuples.

        <br>`param object_` object to print
        <br>`param indent` indent to new nested level
        <br>`param verbose` suppress print to console
        <br>`return` from pprint.pformat
        """
        pretty_printer = pprint.PrettyPrinter(indent=indent)
        pretty_string = pretty_printer.pformat(object=object_)
        if verbose:
            self.multithread_safe(pretty_string)
        return pretty_string

    @property
    def color_output_enabled(self) -> bool:
        if self._color_output_enabled is None:
            self._color_output_enabled = "NO_COLOR" not in OS.env.keys()
        return self._color_output_enabled

    def colored(
        self,
        *strings: Union[str, int, list, dict],  # type: ignore[type-arg]
        attributes: Optional[List[str]] = None,
        end: str = "\n",
        sep: str = " ",
        flush: bool = False,
        verbose: bool = True
    ) -> str:
        """Wrap termcolor.cprint with convenience parsing.

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
        termcolor.COLORS["gray"] = termcolor.COLORS["black"] = 30
        termcolor.HIGHLIGHTS["on_gray"] = termcolor.HIGHLIGHTS["on_black"] = 40
        if OS.windows and not self.colorama_inited and self.color_output_enabled:
            colorama.init()
            self.colorama_inited = True
        # check for colors in input
        highlight: Optional[Any] = None
        color: Optional[Any] = None
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
        strings_to_process: Tuple[Union[str, int, list, dict], ...]  # type: ignore[type-arg]
        if color_args:
            strings_to_process = strings[:-color_args]
        else:
            strings_to_process = strings

        strings_list = ListUtils.to_strings(strings_to_process)

        string = sep.join(strings_list)

        colored_string: str
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
