#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import curses
    import os
    import random
    import shlex
    import shutil
    import subprocess
    import threading
    import time
    import wcwidth
    from typing import Any, Callable, Dict, Iterable, Iterator, List as ListType, Optional, Sequence, Tuple, Union, cast
    from .const import newline
    from .list import List
    from .os import OS as OSClass
    from .print import Print
    from .str import Str
    from .threading import Threading
    from .windows import Windows
    OS = OSClass()
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty

__version__ = "0.11.16"
if not TYPE_CHECKING:
    os = LazyModule("os")
    shutil = LazyModule("shutil")
    time = LazyModule("time")
    subprocess = LazyModule("subprocess")
    shlex = LazyModule("shlex")
    curses = LazyModule("curses")
    OS = LazyProperty(".os", "OS")
    Str = LazyProperty(".str", "Str")
    Print = LazyProperty(".print", "Print")
    Threading = LazyProperty(".threading", "Threading")
    List = LazyProperty(".list", "List")
    Windows = LazyProperty(".windows", "Windows")
    random = LazyModule("random")
    threading = LazyModule("threading")
    wcwidth = LazyModule("wcwidth", optional=True)
    newline = LazyProperty(".const", "newline")


class _MergedOutput(str):
    out: str
    err: str
    timeout_reached: bool

    def __new__(cls, merged: str, out: str, err: str, timeout_reached: bool) -> "_MergedOutput":
        obj = super().__new__(cls, merged)
        obj.out = out
        obj.err = err
        obj.timeout_reached = timeout_reached
        return obj

    def __iter__(self) -> Iterator[Union[str, bool]]:  # type: ignore[override]
        return iter((self.out, self.err, self.timeout_reached))


class Console:
    """Class to interact with terminal|console."""

    def __init__(
        self,
        *commands: Any,
        pure_shell: bool = False,
        print_std: bool = False,
        decoding: Optional[str] = None,
        universal_newlines: bool = False,
        auto_decoding: bool = True,
        auto_disable_py_buffering: bool = True,
        return_merged: bool = True,
        timeout: Optional[float] = None,
        debug: bool = False,
        create_cmd_subprocess: bool = False,
        hook_stdout: Optional[Callable[[Any], None]] = None,
        hook_stderr: Optional[Callable[[Any], None]] = None
    ) -> None:
        """Optionally store a command and default options for quick reuse."""
        self._commands: Optional[Sequence[Any]] = list(commands) if commands else None
        self._defaults: Dict[str, Any] = {
            "pure_shell": pure_shell,
            "print_std": print_std,
            "decoding": decoding,
            "universal_newlines": universal_newlines,
            "auto_decoding": auto_decoding,
            "auto_disable_py_buffering": auto_disable_py_buffering,
            "return_merged": return_merged,
            "timeout": timeout,
            "debug": debug,
            "create_cmd_subprocess": create_cmd_subprocess,
            "hook_stdout": hook_stdout,
            "hook_stderr": hook_stderr,
        }

    def _resolve_commands(self, commands: Optional[Sequence[Any]]) -> Sequence[Any]:
        resolved = commands if commands else self._commands
        if not resolved:
            raise ValueError("commands must be provided either at init or call time")
        return resolved

    def run(self, *commands: Any, **kwargs: Any) -> Any:
        """Run a command using stored defaults unless overridden."""
        resolved_commands = self._resolve_commands(list(commands) if commands else None)
        options: Dict[str, Any] = {}
        for key, default in self._defaults.items():
            options[key] = kwargs.get(key, default)
        return self.get_output(*resolved_commands, **options)  # pylint: disable=not-an-iterable

    __call__ = run

    @classmethod
    def clean(cls) -> None:
        """Wipe terminal output. Not tested on linux.

        todo test on linux, make better
        <br>`return` None
        """
        if OS.windows:
            os.system("cls")
        elif OS.linux:
            print(newline * shutil.get_terminal_size().lines)
        elif OS.macos:
            os.system(r"clear && printf '\e[3J'")

    @classmethod
    def width(cls) -> int:
        """Return console width in characters."""
        return shutil.get_terminal_size().columns

    @classmethod
    def height(cls) -> int:
        """Return console height in characters."""
        height_value: Optional[int] = None
        if OS.windows:
            height_value = shutil.get_terminal_size().lines
        elif OS.unix_family:
            sttysize = Console.get_output("stty size")
            height_value = int(Str.get_integers(sttysize)[0])
        assert height_value is not None
        return int(height_value)

    @classmethod
    def blink(
        cls,
        width: Optional[int] = None,
        height: Optional[int] = None,
        symbol: str = "#",
        sleep: float = 0.5
    ) -> None:  # pylint: disable=too-many-locals
        """Print to terminal rectangle with random color. Complete shit.

        Arguments width and height changing size of
        terminal, works only in Windows.
        <br>`param width` int width of blinking rectangle
        <br>`param height` int height of blinking rectangle
        <br>`param symbol` string of characters, that fill blinking rectangle
        <br>`param sleep` int|float define sleep between print new colored rectangle
        <br>`return`
        """
        if (width is not None) and (height is not None) and OS.windows:
            os.system("mode con cols=" + str(width) + " lines=" + str(height))
        if width is None:
            width = cls.width()
        if height is None:
            height = cls.height()
        while True:
            colors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
            highlights = ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_white"]
            string = symbol * width
            color = random.choice(colors)
            colors.pop(colors.index(color))
            highlight = random.choice(highlights)
            try:  # New version with one long line. Works perfect, as I see.
                string = string * height
                Print.colored(newline + string, color, highlight, end = "")
                time.sleep(sleep)
            except KeyboardInterrupt:
                Print.colored("OK", "white", "on_grey")
                cls.clean()
                break

    @classmethod
    def _get_output(
        cls,
        commands: Any,
        print_std: bool,
        decoding: Optional[str],
        pure_shell: bool = False,
        universal_newlines: bool = False,
        debug: bool = False,
        hook_stdout: Optional[Callable[[Any], None]] = None,
        hook_stderr: Optional[Callable[[Any], None]] = None,
        timeout: Optional[float] = None
    ) -> Tuple[Union[str, bytes], Union[str, bytes], bool]:

        is_string = decoding or universal_newlines
        if hook_stdout is None:
            hook_stdout = lambda _line: None
        if hook_stderr is None:
            hook_stderr = lambda _line: None

        class State:
            timeout_reached = False

        def kill_popen(popen_obj: Any) -> None:
            State.timeout_reached = True
            popen_obj.kill()

        try:
            popen_object = subprocess.Popen(
                commands,
                shell=pure_shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=universal_newlines,
            )
            try:
                def print_out_lines(obj: Any, stderr: bool, hook: Callable[[Any], None]) -> Union[str, bytes]:
                    if timeout is not None:
                        timer = threading.Timer(timeout, kill_popen, args=[popen_object])
                        timer.start()
                    color = "red" if stderr else "green"
                    if is_string:
                        output_str = ""
                        finished = False
                        while not finished:
                            string_input = ""
                            while True:
                                sym = obj.read(1)
                                if not sym:
                                    finished = True
                                    break
                                if isinstance(sym, bytes):
                                    sym = sym.decode(decoding or "utf-8", errors="replace")
                                string_input += sym
                                if sym in ["\r", "\n"]:
                                    break
                            string_current = string_input
                            hook(string_current)
                            output_str += string_current
                            if print_std:
                                Print.colored(str(string_current), color, end='', flush=True)
                        if timeout is not None:
                            timer.cancel()
                        return output_str
                    output_bytes = b""
                    finished = False
                    while not finished:
                        bytes_input = b""
                        while True:
                            sym = obj.read(1)
                            if not sym:
                                finished = True
                                break
                            bytes_input += sym
                            if sym in [b'\r', b'\n']:
                                break
                        hook(bytes_input)
                        output_bytes += bytes_input
                        if print_std:
                            Print.colored(str(bytes_input), color, end='', flush=True)
                    if timeout is not None:
                        timer.cancel()
                    return output_bytes

                pipes = Threading(verbose=debug)

                pipes.add(print_out_lines, "stdout",
                          kwargs={"obj": popen_object.stdout,
                                  "stderr": False,
                                  "hook": hook_stdout})
                pipes.add(print_out_lines, "stderr",
                          kwargs={"obj": popen_object.stderr,
                                  "stderr": True,
                                  "hook": hook_stderr})

                pipes.start(wait_for_keyboard_interrupt=True)

                out, err = pipes.get_results()
                wait = getattr(popen_object, "wait", None)
                if callable(wait):
                    wait()
            finally:
                try:
                    if popen_object.stdout:
                        popen_object.stdout.close()
                except Exception:
                    pass
                try:
                    if popen_object.stderr:
                        popen_object.stderr.close()
                except Exception:
                    pass

        except FileNotFoundError as exception:
            if debug:
                Print.debug(
                    "commands", str(commands),
                    "pure_shell", str(pure_shell),
                    "print_std", str(print_std),
                    "decoding", str(decoding),
                    "universal_newlines", str(universal_newlines)
                )
            raise FileNotFoundError(exception)
        return out, err, State.timeout_reached

    windows_cp65001 = False
    windows_cp65001_fail = False

    @classmethod
    def get_output(
        cls,
        *commands: Any,
        pure_shell: bool = False,
        print_std: bool = False,
        decoding: Optional[str] = None,
        universal_newlines: bool = False,
        auto_decoding: bool = True,
        auto_disable_py_buffering: bool = True,
        return_merged: bool = True,
        timeout: Optional[float] = None,
        debug: bool = False,
        create_cmd_subprocess: bool = False,
        hook_stdout: Optional[Callable[[Any], None]] = None,
        hook_stderr: Optional[Callable[[Any], None]] = None
    ) -> Any:
        """Return output of executing command.

        <br>`param commands` list[string if pure_shell is True] with command and arguments
        <br>`param pure_shell` boolean, if True, the specified command will be executed through the shell
        <br>`param print_std` boolean, if True, output from command will be printed immediately
            (also adds argument -u to
        'py' or 'python' firs arg.)
        <br>`return` tuple with strings stdout and stderr
        """
        if len(commands) == 1:
            commands = commands[0]
        if isinstance(commands, str) and not pure_shell:
            commands = shlex.split(commands, posix=False)

        if isinstance(commands, list) or isinstance(commands, tuple):
            commands_list = List.to_strings(commands)
        else:
            commands_list = [str(commands)]

        if not commands_list:
            raise IndexError("commands must not be empty")

        def empty_hook(_: Any) -> None:
            pass

        if hook_stdout is None:
            hook_stdout = empty_hook
        if hook_stderr is None:
            hook_stderr = empty_hook

        # disable buffering for python
        if ("py" in commands_list
            or "py" in os.path.split(commands_list[0])[1]
            or "python" in commands_list
            or "python" in os.path.split(commands_list[0])[1]
            or "python3" in commands_list
            or "python3" in os.path.split(commands_list[0])[1]
        ) and print_std and auto_disable_py_buffering:
            if "-u" not in commands_list:
                commands_list.insert(1, "-u")
        # set decoding and init
        if auto_decoding and not decoding and not universal_newlines:
            if OS.windows:
                if cls.windows_cp65001:
                    decoding = "cp65001"
                elif cls.windows_cp65001_fail:
                    decoding = "cp866"
                else:
                    try:
                        Windows.fix_unicode_encode_error(safe=False)
                        cls.windows_cp65001 = True
                        decoding = "cp65001"
                    except IOError:  # if cp65001 cannot be set
                        cls.windows_cp65001_fail = True
                        decoding = f"cp{Windows.get_cmd_code_page()}"
            elif OS.unix_family:
                decoding = "utf8"
            else:
                universal_newlines = True

        if decoding and universal_newlines:
            raise TypeError("can't decode 'str' to 'str', set universal_newlines to False for manually set decoding")

        if create_cmd_subprocess:
            commands_old = list(commands_list)
            commands_list = []
            commands_list.append("cmd")
            # commands.append("/U")  # only cmd applications output in utf16,
            #                          other applications output in default encoding D:
            commands_list.append("/C")
            commands_list.append(" ".join(commands_old))

        out, err, timeout_reached = cls._get_output(commands_list, print_std=print_std, decoding=decoding,
                                                    pure_shell=pure_shell,
                                                    universal_newlines=universal_newlines, debug=debug,
                                                    hook_stdout=hook_stdout,
                                                    hook_stderr=hook_stderr,
                                                    timeout=timeout)
        if return_merged:
            def to_text(value: Union[str, bytes]) -> str:
                if isinstance(value, bytes):
                    return value.decode(decoding or "utf-8", errors="replace")
                return value

            out_text = to_text(out)
            err_text = to_text(err)
            return _MergedOutput(out_text + err_text, out_text, err_text, timeout_reached)
        if timeout is not None:
            return out, err, timeout_reached
        return out, err

    @classmethod
    def fit(cls, *strings: str, sep: str = " ", reverse: bool = False) -> ListType[str]:
        """Fit strings to console.

        <br>`param strings` list of strings
        <br>`param sep` string to join strings
        <br>`param reverse` boolean, if True, cut from end of string
        <br>`return` strings, that can be fit in one line print
        <br> yes, implementation is far beyond good
        """
        wcswidth = wcwidth.wcswidth if wcwidth else len
        if len(strings) == 2 and isinstance(strings[1], int):
            console_width = int(strings[1])
            string = str(strings[0])
            if console_width <= 0:
                return ""
            while wcswidth(string) > console_width:
                string = string[:-1]
            while wcswidth(string) < console_width:
                string += " "
            return string

        console_width = cls.width()

        if OS.windows:  # windows adds symbol to end of string :(
            console_width -= 1
        strings_list = List.to_strings(strings)  # replace all to strings
        len_all = wcswidth(sep.join(strings_list))  # count len of all
        reverse = not reverse
        prefix = ">>" if reverse else "<<"

        # check for fit
        if len_all <= console_width:
            pass
        else:
            # get the longest line
            longest_string_index = 0
            for cnt, string in enumerate(strings_list):
                if wcswidth(string) > wcswidth(strings_list[longest_string_index]):
                    longest_string_index = cnt
            longest_string = strings_list[longest_string_index]

            # cut line
            cut_cnt = len_all - console_width + wcswidth(prefix)
            desired_length = wcswidth(longest_string) - cut_cnt
            lendiff = wcswidth(longest_string) - len(longest_string)  # add buffer for double characters
            if reverse:
                longest_string = longest_string[::-1]

            longest_string = longest_string[:int(-cut_cnt+lendiff)]

            while wcswidth(longest_string) > desired_length:
                longest_string = longest_string[:-1]

            while wcswidth(longest_string) < desired_length:
                longest_string += " "

            longest_string += prefix

            if reverse:
                longest_string = longest_string[::-1]


            strings_list[longest_string_index] = longest_string

        return strings_list

    @classmethod
    def watch(
        cls,
        command: Union[str, Sequence[Any], Callable[[], str]],
        interval: float = 1,
        fade_duration: float = 5,
        fade_steps: int = 12,
        timeout: Optional[float] = 5,
        title: Optional[str] = None,
    ) -> None:
        """Continuously display command output with fading change highlights.

        Arrow keys and page keys scroll. Home and End jump to bounds. Press Q or
        Escape to exit. A callable may be supplied instead of a subprocess command.
        """
        if interval <= 0:
            raise ValueError("interval must be greater than zero")
        if fade_duration <= 0:
            raise ValueError("fade_duration must be greater than zero")
        if fade_steps <= 0:
            raise ValueError("fade_steps must be greater than zero")

        def join_command(parts: Sequence[str]) -> str:
            join = getattr(shlex, "join", None)
            if callable(join):
                return str(join(parts))
            return " ".join(shlex.quote(part) for part in parts)

        if callable(command):
            source = command
            if title is None:
                title = getattr(command, "__name__", "watch")
        else:
            if isinstance(command, str):
                command_parts = shlex.split(command)
            else:
                command_parts = [str(part) for part in command]
            command_title = join_command(command_parts)
            if title is None:
                title = command_title

            def source() -> str:
                try:
                    result = subprocess.run(
                        command_parts,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )
                    return result.stdout + (result.stderr or "")
                except subprocess.TimeoutExpired:
                    return f"[timeout: {command_title}]\n"
                except Exception as exception:  # subprocess errors belong in watch output
                    return f"[error: {exception}]\n"

        def setup_colors(stdscr: Any) -> ListType[Tuple[int, int]]:
            curses.use_default_colors()
            stages: ListType[Tuple[int, int]] = []
            if curses.can_change_color() and curses.COLORS >= 256:
                for index in range(fade_steps):
                    fraction = index / (fade_steps - 1) if fade_steps > 1 else 0
                    red = int(600 - fraction * 550)
                    blue = int(1000 - fraction * 920)
                    color_id = 20 + index
                    pair_id = 10 + index
                    curses.init_color(color_id, red, 0, blue)
                    curses.init_pair(pair_id, curses.COLOR_WHITE, color_id)
                    stages.append((pair_id, 0))
            else:
                curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
                stages = [(10, 0)] * fade_steps
            return stages

        def detect_changes(
            current_lines: Sequence[str],
            previous_lines: Sequence[str],
            change_times: Dict[Tuple[int, int], float],
            now: float,
        ) -> None:
            for line_index, line in enumerate(current_lines):
                previous = previous_lines[line_index] if line_index < len(previous_lines) else ""
                if line == previous:
                    continue
                for column_index, character in enumerate(line):
                    if column_index >= len(previous) or character != previous[column_index]:
                        change_times[(line_index, column_index)] = now
                for column_index in range(len(line), len(previous)):
                    change_times.pop((line_index, column_index), None)
            stale = [key for key in change_times if key[0] >= len(current_lines)]
            for key in stale:
                del change_times[key]

        def expire_old(change_times: Dict[Tuple[int, int], float], now: float) -> None:
            cutoff = now - fade_duration
            stale = [key for key, changed_at in change_times.items() if changed_at < cutoff]
            for key in stale:
                del change_times[key]

        def fade_attr(age: float, stages: Sequence[Tuple[int, int]]) -> Tuple[int, int]:
            step_duration = fade_duration / len(stages)
            index = int(age / step_duration)
            if index < len(stages):
                return stages[index]
            return 0, 0

        def handle_keys(
            stdscr: Any,
            scroll_y: int,
            scroll_x: int,
            max_y: int,
            max_x: int,
            body_height: int,
            body_width: int,
            at_bottom: bool,
        ) -> Tuple[int, int, bool, bool]:
            while True:
                key = stdscr.getch()
                if key == -1:
                    break
                if key in (ord("q"), ord("Q"), 27):
                    return scroll_y, scroll_x, True, at_bottom
                if key == curses.KEY_UP:
                    scroll_y = max(0, scroll_y - 1)
                    at_bottom = scroll_y >= max(0, max_y - body_height)
                elif key == curses.KEY_DOWN:
                    scroll_y = min(max(0, max_y - body_height), scroll_y + 1)
                    at_bottom = scroll_y >= max(0, max_y - body_height)
                elif key == curses.KEY_LEFT:
                    scroll_x = max(0, scroll_x - 4)
                elif key == curses.KEY_RIGHT:
                    scroll_x = min(max(0, max_x - body_width), scroll_x + 4)
                elif key == curses.KEY_PPAGE:
                    scroll_y = max(0, scroll_y - body_height)
                    at_bottom = scroll_y >= max(0, max_y - body_height)
                elif key == curses.KEY_NPAGE:
                    scroll_y = min(max(0, max_y - body_height), scroll_y + body_height)
                    at_bottom = scroll_y >= max(0, max_y - body_height)
                elif key == curses.KEY_HOME:
                    scroll_y = 0
                    scroll_x = 0
                    at_bottom = False
                elif key == curses.KEY_END:
                    scroll_y = max(0, max_y - body_height)
                    at_bottom = True
            return scroll_y, scroll_x, False, at_bottom

        def draw(
            stdscr: Any,
            current_lines: Sequence[str],
            change_times: Dict[Tuple[int, int], float],
            scroll_y: int,
            scroll_x: int,
            now: float,
            stages: Sequence[Tuple[int, int]],
        ) -> None:
            height, width = stdscr.getmaxyx()
            body_height = height - 2
            if body_height < 1:
                return
            stdscr.erase()

            timestamp = time.strftime("%a %b %d %H:%M:%S %Y")
            header_left = f"Every {interval}s: {title}"
            header_right = timestamp
            padding = width - len(header_left) - len(header_right)
            if padding < 1:
                header_left = header_left[:width - len(header_right) - 1]
                padding = 1
            header = header_left + " " * padding + header_right
            try:
                stdscr.addnstr(0, 0, header, width, curses.A_BOLD)
            except curses.error:
                pass

            for visible_index in range(body_height):
                line_index = visible_index + scroll_y
                row = visible_index + 2
                if line_index >= len(current_lines):
                    break
                line = current_lines[line_index]
                visible = line[scroll_x:scroll_x + width]
                highlighted = any(
                    (line_index, column_index) in change_times
                    for column_index in range(scroll_x, scroll_x + len(visible))
                )
                try:
                    if highlighted:
                        for column, character in enumerate(visible):
                            source_column = column + scroll_x
                            changed_at = change_times.get((line_index, source_column))
                            if changed_at is not None:
                                pair, attr = fade_attr(now - changed_at, stages)
                                stdscr.addstr(row, column, character, curses.color_pair(pair) | attr)
                            else:
                                stdscr.addstr(row, column, character)
                    else:
                        stdscr.addnstr(row, 0, visible, width)
                except curses.error:
                    pass

            max_y = len(current_lines)
            if max_y > body_height or scroll_x > 0:
                indicator = f" [{scroll_y + 1}-{min(scroll_y + body_height, max_y)}/{max_y}  x:{scroll_x}] "
                indicator_x = width - len(indicator)
                if indicator_x >= 0:
                    try:
                        stdscr.addnstr(height - 1, indicator_x, indicator, len(indicator), curses.A_DIM)
                    except curses.error:
                        pass
            stdscr.refresh()

        def main(stdscr: Any) -> None:
            curses.curs_set(0)
            stages = setup_colors(stdscr)
            stdscr.nodelay(True)
            stdscr.keypad(True)

            previous_lines: Optional[ListType[str]] = None
            change_times: Dict[Tuple[int, int], float] = {}
            scroll_y = 0
            scroll_x = 0
            at_bottom = True

            while True:
                now = time.monotonic()
                current_lines = source().splitlines()

                if previous_lines is not None:
                    detect_changes(current_lines, previous_lines, change_times, now)
                expire_old(change_times, now)
                previous_lines = current_lines

                height, width = stdscr.getmaxyx()
                body_height = max(1, height - 2)
                max_y = len(current_lines)
                max_x = max((len(line) for line in current_lines), default=0)

                if at_bottom:
                    scroll_y = max(0, max_y - body_height)
                else:
                    scroll_y = max(0, min(scroll_y, max(0, max_y - body_height)))
                scroll_x = max(0, min(scroll_x, max(0, max_x - width)))

                draw(stdscr, current_lines, change_times, scroll_y, scroll_x, now, stages)

                deadline = time.monotonic() + interval
                while time.monotonic() < deadline:
                    scroll_y, scroll_x, should_quit, at_bottom = handle_keys(
                        stdscr,
                        scroll_y,
                        scroll_x,
                        max_y,
                        max_x,
                        body_height,
                        width,
                        at_bottom,
                    )
                    if should_quit:
                        return
                    now = time.monotonic()
                    expire_old(change_times, now)
                    draw(stdscr, current_lines, change_times, scroll_y, scroll_x, now, stages)
                    time.sleep(0.03)

        try:
            curses.wrapper(main)
        except KeyboardInterrupt:
            pass
