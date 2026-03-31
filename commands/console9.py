#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.11.16"

import threading


class Console:
    """Class to interact with terminal|console
    """

    @staticmethod
    def clean():
        """Wipe terminal output. Not tested on linux
        todo test on linux, make better
        <br>`return` None
        """
        import os
        from .os9 import OS
        if OS.windows:
            os.system("cls")
        elif OS.linux:
            import shutil
            from .const9 import newline
            print(newline * shutil.get_terminal_size().lines)
        elif OS.macos:
            os.system(r"clear && printf '\e[3J'")

    @staticmethod
    def width():
        """
        <br>`return` int width of opened console in chars
        """
        import shutil
        return shutil.get_terminal_size().columns

    @staticmethod
    def height():
        """
        <br>`return` int height of opened console in chars
        """
        from .os9 import OS
        height = None
        if OS.windows:
            import shutil
            height = shutil.get_terminal_size().lines
        elif OS.unix_family:
            from .str9 import Str
            sttysize = Console.get_output("stty size")
            height = Str.get_integers(sttysize)[0]
        return int(height)

    @classmethod
    def blink(cls, width=None, height=None, symbol="#", sleep=0.5):  # pylint: disable=too-many-locals
        """Print to terminal rectangle with random color. Complete shit. Arguments width and height changing size of
        terminal, works only in Windows.
        <br>`param width` int width of blinking rectangle
        <br>`param height` int height of blinking rectangle
        <br>`param symbol` string of characters, that fill blinking rectangle
        <br>`param sleep` int|float define sleep between print new colored rectangle
        <br>`return`
        """
        import random
        from .os9 import OS
        from .print9 import Print
        from .const9 import newline
        if (width is not None) and (height is not None) and OS.windows:
            import os
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
                import time
                string = string * height
                Print.colored(newline + string, color, highlight, end = "")
                time.sleep(sleep)
            except KeyboardInterrupt:
                Print.colored("OK", "white", "on_grey")
                cls.clean()
                break

    @staticmethod
    def _get_output(commands, print_std, decoding, pure_shell, universal_newlines, debug=False,
                    hook_stdout=None, hook_stderr=None, timeout=None):
        import subprocess
        from .threading9 import Threading

        is_string = decoding or universal_newlines

        class State:
            timeout_reached = False

        def kill_popen(popen_obj):
            State.timeout_reached = True
            popen_obj.kill()

        try:
            with subprocess.Popen(commands, shell=pure_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=universal_newlines) as popen_object:
                def print_out_lines(obj: popen_object, stderr: bool, hook):
                    if timeout is not None:
                        timer = threading.Timer(timeout, kill_popen, args=[popen_object])
                        timer.start()
                    color = "red" if stderr else "green"
                    output = b''
                    if is_string:
                        output = ''
                    finished = False
                    # for string in obj:
                    while not finished:
                        string_input = b''
                        while True:
                            sym = obj.read(1)
                            if not sym:
                                finished = True
                                break
                            string_input += sym
                            if sym in [b'\r', b'\n']:
                                break
                        string_current = string_input
                        if decoding:
                            try:
                                string_current = string_input.decode(decoding)
                            except UnicodeDecodeError:
                                # fallback to chardet
                                import chardet
                                string_current = string_input.decode(chardet.detect(string_input)['encoding'])
                        hook(string_current)
                        output += string_current
                        if print_std:
                            from .print9 import Print
                            Print.colored(string_current, color, end='', flush=True)
                    if timeout is not None:
                        timer.cancel()
                    return output

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

        except FileNotFoundError as exception:
            if debug:
                from .print9 import Print
                Print.debug("commands", commands,
                            "pure_shell", pure_shell,
                            "print_std", print_std,
                            "decoding", decoding,
                            "universal_newlines", universal_newlines)
            raise FileNotFoundError(exception)
        return out, err, State.timeout_reached

    windows_cp65001 = False
    windows_cp65001_fail = False

    @classmethod
    def get_output(cls, *commands, pure_shell=False, print_std=False, decoding=None, universal_newlines=False,
                   auto_decoding=True, auto_disable_py_buffering=True, return_merged=True, timeout=None, debug=False,
                   create_cmd_subprocess=False, hook_stdout=None, hook_stderr=None):
        """Return output of executing command.
        <br>`param commands` list[string if pure_shell is True] with command and arguments
        <br>`param pure_shell` boolean, if True, the specified command will be executed through the shell
        <br>`param print_std` boolean, if True, output from command will be printed immediately
            (also adds argument -u to
        'py' or 'python' firs arg.)
        <br>`return` tuple with strings stdout and stderr
        """
        import os
        from .os9 import OS
        if len(commands) == 1:
            commands = commands[0]
        if isinstance(commands, str) and not pure_shell:
            import shlex
            commands = shlex.split(commands, posix=False)

        if isinstance(commands, list) or isinstance(commands, tuple):
            from .list9 import List
            commands = List.to_strings(commands)

        if not commands:
            raise IndexError("commands must not be empty")

        def empty_hook(_):
            pass

        if hook_stdout is None:
            hook_stdout = empty_hook
        if hook_stderr is None:
            hook_stderr = empty_hook

        # disable buffering for python
        if ("py" in commands
            or "py" in os.path.split(commands[0])[1]
            or "python" in commands
            or "python" in os.path.split(commands[0])[1]
            or "python3" in commands
            or "python3" in os.path.split(commands[0])[1]
        ) and print_std and auto_disable_py_buffering:
            if "-u" not in commands:
                list_commands = list(commands)
                list_commands.insert(1, "-u")
                commands = list_commands
        # set decoding and init
        if auto_decoding and not decoding and not universal_newlines:
            if OS.windows:
                if cls.windows_cp65001:
                    decoding = "cp65001"
                elif cls.windows_cp65001_fail:
                    decoding = "cp866"
                else:
                    from .windows9 import Windows
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
            commands_old = commands
            commands = list()
            commands.append("cmd")
            # commands.append("/U")  # only cmd applications output in utf16,
            #                          other applications output in default encoding D:
            commands.append("/C")
            commands.append(" ".join(commands_old))

        out, err, timeout_reached = cls._get_output(commands, print_std=print_std, decoding=decoding,
                                                    pure_shell=pure_shell,
                                                    universal_newlines=universal_newlines, debug=debug,
                                                    hook_stdout=hook_stdout,
                                                    hook_stderr=hook_stderr,
                                                    timeout=timeout)
        if return_merged:
            return out + err
        if timeout:
            return out, err, timeout_reached
        else:
            return out, err

    @classmethod
    def fit(cls, *strings: str, sep: str = " ", reverse=False):
        """Fit strings to console
        <br>`param strings` list of strings
        <br>`param sep` string to join strings
        <br>`param reverse` boolean, if True, cut from end of string
        <br>`return` strings, that can be fit in one line print
        <br> yes, implementation is far beyond good
        """
        from .os9 import OS
        from .list9 import List
        from wcwidth import wcswidth

        console_width = cls.width()
        
        if OS.windows:  # windows adds symbol to end of string :(
            console_width -= 1
        strings = List.to_strings(strings)  # replace all to strings
        len_all = wcswidth(sep.join(strings))  # count len of all
        reverse = not reverse
        prefix = ">>" if reverse else "<<"
        
        # check for fit
        if len_all <= console_width:
            pass
        else:
            # get the longest line
            longest_string_index = 0
            for cnt, string in enumerate(strings):
                if wcswidth(string) > wcswidth(strings[longest_string_index]):
                    longest_string_index = cnt
            longest_string = strings[longest_string_index]
            
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

            
            strings[longest_string_index] = longest_string

        return strings

    @staticmethod
    def watch(command, interval=1, fade_duration=5, fade_steps=12, timeout=5, title=None):
        """Watch the output of a command or callable, refreshing periodically with fading diff highlights.
        <br>`param command` string command, list/tuple of strings, or callable returning str
        <br>`param interval` int|float seconds between refreshes
        <br>`param fade_duration` int|float seconds for a changed cell highlight to fully fade out
        <br>`param fade_steps` int number of distinct background shades in the fade
        <br>`param timeout` int|float per-command timeout in seconds (ignored when command is callable)
        <br>`param title` string header text; defaults to the command string
        <br>`return` None
        """
        import curses
        import shlex
        import subprocess
        import time

        if callable(command):
            source = command
            if title is None:
                title = command.__name__ if hasattr(command, "__name__") else "watch"
        else:
            if isinstance(command, str):
                cmd_list = shlex.split(command)
            else:
                cmd_list = [str(a) for a in command]
            if title is None:
                title = shlex.join(cmd_list)

            def source():
                try:
                    r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
                    out = r.stdout
                    if r.stderr:
                        out += r.stderr
                    return out
                except subprocess.TimeoutExpired:
                    return f"[timeout: {shlex.join(cmd_list)}]\n"
                except Exception as e:
                    return f"[error: {e}]\n"

        def setup_colors(stdscr):
            curses.use_default_colors()
            stages = []
            if curses.can_change_color() and curses.COLORS >= 256:
                for i in range(fade_steps):
                    t = i / (fade_steps - 1) if fade_steps > 1 else 0
                    r = int(600 - t * 550)
                    g = 0
                    b = int(1000 - t * 920)
                    color_id = 20 + i
                    pair_id = 10 + i
                    curses.init_color(color_id, r, g, b)
                    curses.init_pair(pair_id, curses.COLOR_WHITE, color_id)
                    stages.append((pair_id, 0))
            else:
                curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
                stages = [(10, 0)] * fade_steps
            return stages

        def detect_changes(cur_lines, prev_lines, change_times, now):
            for li, line in enumerate(cur_lines):
                prev = prev_lines[li] if li < len(prev_lines) else ""
                if line == prev:
                    continue
                for ci, ch in enumerate(line):
                    if ci >= len(prev) or ch != prev[ci]:
                        change_times[(li, ci)] = now
                for ci in range(len(line), len(prev)):
                    change_times.pop((li, ci), None)
            stale = [k for k in change_times if k[0] >= len(cur_lines)]
            for k in stale:
                del change_times[k]

        def expire_old(change_times, now):
            cutoff = now - fade_duration
            stale = [k for k, t in change_times.items() if t < cutoff]
            for k in stale:
                del change_times[k]

        def fade_attr(age, stages):
            step_dur = fade_duration / len(stages)
            idx = int(age / step_dur)
            if idx < len(stages):
                return stages[idx]
            return 0, 0

        def handle_keys(stdscr, scroll_y, scroll_x, max_y, max_x, body_h, body_w, at_bottom):
            while True:
                key = stdscr.getch()
                if key == -1:
                    break
                if key in (ord("q"), ord("Q"), 27):
                    return scroll_y, scroll_x, True, at_bottom
                elif key == curses.KEY_UP:
                    scroll_y = max(0, scroll_y - 1)
                    at_bottom = scroll_y >= max(0, max_y - body_h)
                elif key == curses.KEY_DOWN:
                    scroll_y = min(max(0, max_y - body_h), scroll_y + 1)
                    at_bottom = scroll_y >= max(0, max_y - body_h)
                elif key == curses.KEY_LEFT:
                    scroll_x = max(0, scroll_x - 4)
                elif key == curses.KEY_RIGHT:
                    scroll_x = min(max(0, max_x - body_w), scroll_x + 4)
                elif key == curses.KEY_PPAGE:
                    scroll_y = max(0, scroll_y - body_h)
                    at_bottom = scroll_y >= max(0, max_y - body_h)
                elif key == curses.KEY_NPAGE:
                    scroll_y = min(max(0, max_y - body_h), scroll_y + body_h)
                    at_bottom = scroll_y >= max(0, max_y - body_h)
                elif key == curses.KEY_HOME:
                    scroll_y = 0
                    scroll_x = 0
                    at_bottom = False
                elif key == curses.KEY_END:
                    scroll_y = max(0, max_y - body_h)
                    at_bottom = True
            return scroll_y, scroll_x, False, at_bottom

        def draw(stdscr, cur_lines, change_times, scroll_y, scroll_x, now, stages):
            height, width = stdscr.getmaxyx()
            body_h = height - 2
            if body_h < 1:
                return
            stdscr.erase()

            ts = time.strftime("%a %b %d %H:%M:%S %Y")
            header_left = f"Every {interval}s: {title}"
            header_right = ts
            pad = width - len(header_left) - len(header_right)
            if pad < 1:
                header_left = header_left[:width - len(header_right) - 1]
                pad = 1
            header = header_left + " " * pad + header_right
            try:
                stdscr.addnstr(0, 0, header, width, curses.A_BOLD)
            except curses.error:
                pass

            for vi in range(body_h):
                li = vi + scroll_y
                row = vi + 2
                if li >= len(cur_lines):
                    break
                line = cur_lines[li]
                visible = line[scroll_x: scroll_x + width]
                has_highlights = any((li, ci) in change_times for ci in range(scroll_x, scroll_x + len(visible)))
                if has_highlights:
                    try:
                        for col, ch in enumerate(visible):
                            src_col = col + scroll_x
                            ct = change_times.get((li, src_col))
                            if ct is not None:
                                age = now - ct
                                pair, attr = fade_attr(age, stages)
                                stdscr.addstr(row, col, ch, curses.color_pair(pair) | attr)
                            else:
                                stdscr.addstr(row, col, ch)
                    except curses.error:
                        pass
                else:
                    try:
                        stdscr.addnstr(row, 0, visible, width)
                    except curses.error:
                        pass

            max_y = len(cur_lines)
            if max_y > body_h or scroll_x > 0:
                indicator = f" [{scroll_y + 1}-{min(scroll_y + body_h, max_y)}/{max_y}  x:{scroll_x}] "
                ix = width - len(indicator)
                if ix >= 0:
                    try:
                        stdscr.addnstr(height - 1, ix, indicator, len(indicator), curses.A_DIM)
                    except curses.error:
                        pass
            stdscr.refresh()

        def _main(stdscr):
            curses.curs_set(0)
            stages = setup_colors(stdscr)
            stdscr.nodelay(True)
            stdscr.keypad(True)

            prev_lines = None
            change_times = {}
            scroll_y = 0
            scroll_x = 0
            at_bottom = True  # start pinned to bottom

            while True:
                now = time.monotonic()
                output = source()
                cur_lines = output.splitlines()

                if prev_lines is not None:
                    detect_changes(cur_lines, prev_lines, change_times, now)
                expire_old(change_times, now)
                prev_lines = cur_lines

                height, width = stdscr.getmaxyx()
                body_h = max(1, height - 2)
                max_y = len(cur_lines)
                max_x = max((len(l) for l in cur_lines), default=0)

                if at_bottom:
                    scroll_y = max(0, max_y - body_h)
                else:
                    scroll_y = max(0, min(scroll_y, max(0, max_y - body_h)))
                scroll_x = max(0, min(scroll_x, max(0, max_x - width)))

                draw(stdscr, cur_lines, change_times, scroll_y, scroll_x, now, stages)

                deadline = time.monotonic() + interval
                while time.monotonic() < deadline:
                    scroll_y, scroll_x, quit_, at_bottom = handle_keys(
                        stdscr, scroll_y, scroll_x, max_y, max_x, body_h, width, at_bottom)
                    if quit_:
                        return
                    now = time.monotonic()
                    expire_old(change_times, now)
                    draw(stdscr, cur_lines, change_times, scroll_y, scroll_x, now, stages)
                    time.sleep(0.03)

        try:
            curses.wrapper(_main)
        except KeyboardInterrupt:
            pass
