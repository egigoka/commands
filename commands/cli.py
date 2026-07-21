#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with commandline interfaces."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import datetime
    from typing import Any, List, Optional, Union, cast
    from .console import Console
    from .const import backslash
    from .keyboard import Keyboard
    from .os import OS as OSClass
    from .print import Print
    from .str import Str
    from .time import Time
    OS = OSClass()
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty

__version__ = "0.5.1"
if not TYPE_CHECKING:
    Keyboard = LazyProperty(".keyboard", "Keyboard")
    Str = LazyProperty(".str", "Str")
    Print = LazyProperty(".print", "Print")
    Console = LazyProperty(".console", "Console")
    OS = LazyProperty(".os", "OS")
    Time = LazyProperty(".time", "Time")
    datetime = LazyModule("datetime")
    backslash = LazyProperty(".const", "backslash")


class CLI:
    """Class to work with commandline interfaces."""

    def __init__(self, default_answer: Optional[Any] = None) -> None:
        self.default_answer: Optional[Any] = default_answer

    def __call__(self, question: str) -> bool:
        """Alias for get_yes_no for terse prompting."""
        return self.get_yes_no(question)

    def get_yes_no(self, question: str) -> bool:
        """Prompt the user for a yes/no response."""
        return self.__class__.get_y_n(question, default=self.default_answer)

    @classmethod
    def get_y_n(cls, question: str, default: Optional[Any] = None) -> bool:
        """Obtain answer yes or no from user in commandline.

        <br>`param question` string with question to user
        <br>`param answer` predefined string with answer, must be "y" or "n"
        <br>`return` boolean
        """

        def get_key() -> str:
            import sys
            if not sys.stdin.isatty():
                raise OSError("stdin is not a terminal")

            if OS.windows:
                import msvcrt  # pylint: disable=import-error,import-outside-toplevel
                getwch = getattr(msvcrt, "getwch")
                key = str(getwch())
                if key in ("\x00", "\xe0"):
                    key = str(getwch())
                return key

            import termios
            import tty
            file_descriptor = sys.stdin.fileno()
            old_settings = termios.tcgetattr(file_descriptor)
            try:
                tty.setraw(file_descriptor)
                return str(sys.stdin.read(1))
            finally:
                termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)

        def check_answer(string: Optional[Any]) -> Optional[bool]:  # pylint: disable=inconsistent-return-statements
            """Check input from user or argument "answer".

            <br>`param string` input string, check answer for "y" or "n", for other values return None
            <br>`return` True|False|None
            """
            if string is None:
                return None

            if string == "\x03":
                raise KeyboardInterrupt

            string = string.lower()
            string_t = Keyboard.translate_string(string)

            if string != string_t:
                print(" > " + string_t, end="")
                string = string_t

            if string == "y":
                return True
            if string == "n":
                return False
            return None

        while True:
            print_str = f"{question} (y/n)? "
            if default:
                print_str += f" default '{default}'"
            try:
                print(print_str, end="", flush=True)
                input_str = get_key()
                print(input_str, end="")
            except Exception:
                input_str = input(print_str)
                input_str = input_str.strip()
            output = check_answer(input_str)
            print()
            if output is not None:
                return output
            else:
                default_value = check_answer(default)
                if default_value is not None:
                    return default_value

    @classmethod
    def get_ints(cls, question: str, count_of_ints: int) -> Union[int, List[Union[int, float]]]:
        """Obtain answer with integers from user in commandline.

        <br>`param question` string with question to user
        <br>`param count_of_ints` int of ints must be in answer
        <br>`param answer` predefined string with answer
        <br>`return` integer or list of integers
        """
        while True:
            input_str = input(f"{question} (answer {count_of_ints} integer_s): ")
            ints = Str.get_integers(input_str, float_support=False)
            output: Optional[Union[int, List[Union[int, float]]]] = None
            if len(ints) == count_of_ints:
                if count_of_ints == 1:
                    output = cast(int, ints[0])
                else:
                    output = ints
            if output is not None:
                return output

    @classmethod
    def get_int(cls, question: str) -> Union[int, List[Union[int, float]]]:
        """Prompt the user for a single integer."""
        return cls.get_ints(question=question, count_of_ints=1)

    @classmethod
    def get_integer(cls, question: str) -> Union[int, List[Union[int, float]]]:
        """Alias for get_int."""
        return cls.get_int(question=question)

    @classmethod
    def get_integers(cls, question: str, count_of_ints: int) -> Union[int, List[Union[int, float]]]:
        """Alias for get_ints."""
        return cls.get_ints(question=question, count_of_ints=count_of_ints)

    wait_update_pos = 0

    @classmethod
    def wait_update(cls, verbose: bool = False) -> str:
        """Print a rotating progress stick for long processes.

        Print 'spinning' (if function called multiple times) stick, used for long processes to show user that some
        progress are going.
        <br>`param verbose` boolean, suppress print to console
        <br>`return` string with 'stick' in new position
        """
        stick = "|"
        if cls.wait_update_pos == 0:
            stick = "|"
        elif cls.wait_update_pos == 1:
            stick = "/"
        elif cls.wait_update_pos == 2:
            stick = "-"
        elif cls.wait_update_pos == 3:
            stick = backslash
            cls.wait_update_pos = -1
        cls.wait_update_pos += 1
        if verbose:
            Print.rewrite(stick)
        return stick

    @classmethod
    def progressbar(
        cls,
        done: Union[int, float],
        total: Union[int, float],
        done_repr: str = "",
        total_repr: str = "",
        reverse: bool = False
    ) -> str:
        """Generate a progress bar string with text representation of progress.

        :param done: Number of completed units.
        :param total: Total number of units.
        :param done_repr: String representing completed units.
        :param total_repr: String representing total units.
        :param reverse: If True, progress will be counting backwards (from total to 0).
        :return: A string representing the progress bar.
        """
        console_width = Console.width()

        if OS.windows:  # windows add symbol to end of string :(
            console_width -= 1

        if reverse:
            done = total - done
        if done > total:
            done = total

        if done < 0:
            done = 0

        add_split = done_repr != "" and total_repr != ""
        add_space = done_repr != "" or total_repr != ""

        done_repr = str(done_repr)
        total_repr = str(total_repr)

        proportion_done = done / total if total else 0

        additional_space = (3 if add_split else 0) + (1 if add_space else 0)

        text_length = len(done_repr) + len(total_repr) + additional_space
        bar_length = console_width - text_length

        full_blocks = int(proportion_done * bar_length)
        remainder = (proportion_done * bar_length) % 1
        blocks = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
        medium_shade = blocks[int(remainder * 8)]

        split = " / " if add_split else ""
        space = " " if add_space else ""

        progress_bar = (f"{done_repr}{split}{total_repr}{space}"
                        + f"{'█' * full_blocks}{medium_shade}"
                        + f"{' ' * (bar_length - full_blocks - len(medium_shade))}")

        return progress_bar

    @classmethod
    def multiline_input(cls, question: str) -> str:
        """Collect multiline user input until EOF."""
        print("\nEnter|paste your content. Ctrl-D or Ctrl-Z (Windows) to save it.")
        print(question)
        lines = []
        while True:
            try:
                lines.append(input())
            except EOFError:
                print()
                break
        return "\n".join(lines)

    @classmethod
    def get_date(cls, date_name: str, always_return_date: bool = False) -> Optional[datetime.datetime]:
        """Get a date from user input.

        :param date_name: string, name of date for user
        :param always_return_date: bool, ask user a date until valid is entered
        :return None if date is not entered and always_return_date is False
        :return datetime.datetime if correct data is entered (time is 00:00:00)
        """
        date = None
        while date is None:
            date_str = input(f"Enter date of {date_name} like \"{str(Time.datetime().day).zfill(2)}\" "
                             f"or with month \"{str(Time.datetime().day).zfill(2)}"
                             f"{str(Time.datetime().month).zfill(2)}\" "
                             f"or with year \"{str(Time.datetime().day).zfill(2)}"
                             f"{str(Time.datetime().month).zfill(2)}"
                             f"{str(Time.datetime().year).zfill(4)}\": ").strip()
            if date_str:
                date = Time.datetime()
                try:
                    day = int(date_str[:2])
                except ValueError:
                    day = date.day
                try:
                    month = int(date_str[2:4])
                except ValueError:
                    month = date.month
                try:
                    year = int(date_str[4:])
                    if len(str(year)) == 2:
                        year += 2000
                except ValueError:
                    year = date.year

                try:
                    date = date.replace(day=day, month=month, year=year, hour=0, minute=0, second=0, microsecond=0)
                    break
                except ValueError:
                    print("Wrong date.")
                    date = None
            else:
                if always_return_date:
                    print("Please, enter date.")
                    continue
                else:
                    break

        return date
