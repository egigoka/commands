#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.11.14"

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
                Print.colored(string, color, highlight)
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
