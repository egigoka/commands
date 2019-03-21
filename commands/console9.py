#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.8.9"


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
        from .os9 import OS
        if OS.windows:
            import shutil
            width_ = shutil.get_terminal_size().columns
        elif OS.unix_family:
            from .str9 import Str
            io_string = Console.get_output("stty", "size")
            width_ = Str.get_integers(io_string)[1]
        return int(width_)

    @staticmethod
    def height():
        """
        <br>`return` int height of opened console in chars
        """
        from .os9 import OS
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
        """Print to terminal reactangle with random color. Completely shit. Arguments width and height changing size of
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
    def _get_output_with_timeout(*commands, print_std, decoding, timeout):
        import asyncio
        import sys
        import time
        import psutil
        from asyncio.subprocess import PIPE
        from contextlib import suppress

        class State:
            #debug#
            temp = b''
            # debug#
            if decoding:
                stdout = ""
                stderr = ""
            else:
                stdout = b''
                stderr = b''
            timeout_exception = False
            stderr_timeout = 1

        def do_something(line):
            if decoding:
                try:
                    line = line.decode(decoding)
                # if it's output from Windows cmd and utf-16 cant decode last byte (truncated data)
                except UnicodeDecodeError:
                    if line[:-1]:
                        line = line[:-1].decode(decoding) + '\n'
                    else:
                        line = ''
            State.stdout += line
            if print_std:
                print(line, end="")
            return True

        def save_stderr(stderr):
            if decoding:
                stderr = stderr.decode(decoding)
            State.stderr = stderr
            if print_std and stderr:
                print(f"stderr:\n{stderr}")

        async def run_command(*args, timeout):
            # start child process
            # NOTE: universal_newlines parameter is not supported
            process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)

            # read line (sequence of bytes ending with b'\n') asynchronously
            end_time = time.monotonic() + timeout
            with suppress(ProcessLookupError, psutil.NoSuchProcess):
                # it throws if process already killed, but python try to kill it one more time

                def kill_by_pid(proc_pid):
                    process = psutil.Process(proc_pid)
                    for proc in process.children(recursive=True):
                        proc.kill()
                    process.kill()

                while True:
                    timeout = end_time - time.monotonic()
                    try:
                        line = await asyncio.wait_for(process.stdout.readline(), timeout)
                    except asyncio.TimeoutError as exc:
                        kill_by_pid(process.pid)
                        process.kill()
                        from .print9 import Print
                        save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=State.stderr_timeout))
                        State.timeout_exception = True
                        break
                    else:
                        if not line:  # EOF
                            try:
                                kill_by_pid(process.pid)
                                process.kill()
                                from .print9 import Print
                                save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=State.stderr_timeout))
                            except TimeoutError:
                                pass
                            break
                        elif do_something(line):
                            continue  # while some criterium is satisfied
                    try:
                        kill_by_pid(process.pid)
                        process.kill()
                        from .print9 import Print
                        save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=State.stderr_timeout))
                    except TimeoutError:
                        pass
                    process.kill()  # timeout or some criterium is not satisfied
                    await process.communicate()
                    break
            return await process.wait()  # wait for the child process to exit

        if sys.platform == "win32":
            loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        return_code = loop.run_until_complete(run_command(*commands, timeout=timeout))
        loop.close()
        return State.stdout, State.stderr, return_code, State.timeout_exception

    @staticmethod
    def _get_output(*commands, print_std, decoding, pureshell, universal_newlines):
        import subprocess
        if decoding:
            out = ""
            err = ""
        else:
            out = b''
            err = b''
        # end setting decoding and init

        try:
            with subprocess.Popen(commands, shell=pureshell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                  universal_newlines=universal_newlines) as popen_object:

                for line in popen_object.stdout:
                    if decoding:
                        line = line.decode(decoding)
                    out += line
                    if print_std:
                        print(line, end='')

                for line in popen_object.stderr:
                    if decoding:
                        line = line.decode(decoding)
                    err += line
                    if print_std:
                        print(line, end='')
        except FileNotFoundError as exception:
            from .print9 import Print
            Print.debug("commands", commands, "pureshell", pureshell, "print_std", print_std, "decoding", decoding,
                        "universal_newlines", universal_newlines)
            raise FileNotFoundError(exception)
        return out, err

    windows_utf8 = False

    @classmethod
    def get_output(cls, *commands, pureshell=False, print_std=False, decoding=None, universal_newlines=False,
                   auto_decoding=True, auto_disable_py_buffering=True, return_merged=True, timeout=None):
        """Return output of executing command.
        <br>`param commands` list[string if pureshell is True] with command and arguments
        <br>`param pureshell` boolean, if True, the specified command will be executed through the shell
        <br>`param print_std` boolean, if True, output from command will be printed immideately (also adds argument -u to
        'py' or 'python' firs arg.)
        <br>`return` typle with strings stdout and stderr
        """
        from .os9 import OS
        if len(commands) == 1:
                commands = commands[0]
        if isinstance(commands, str):
            import shlex
            commands = shlex.split(commands, posix=False)

        try:
            commands[0]
        except IndexError:
            raise IndexError("commands must not be empty")

        # disable buffering for python
        if ("py" in commands or "py" in commands[0]) and print_std and auto_disable_py_buffering:
            if "-u" not in commands:
                list_commands = list(commands)

                list_commands.insert(1, "-u")
                commands = list_commands

        # end disabling buffering for python

        # set decoding and init
        if auto_decoding and not decoding and not universal_newlines:
            if OS.windows:
                if not cls.windows_utf8:
                    from .windows9 import Windows
                    Windows.fix_unicode_encode_error(quiet=True)
                    cls.windows_utf8 = True
                decoding = "utf_8"
            elif OS.unix_family:
                decoding = "utf8"
            else:
                universal_newlines = True

        if decoding and universal_newlines:
            raise TypeError("can't decode 'str' to 'str', set universal_newlines to False for manually set decoding")
        if timeout and universal_newlines:
            raise NotImplementedError("asyncio.subprocess doesn't support 'universal_newlines', disable 'auto_decoding'"
                                      " or set 'decoding'")

        if timeout:
            if pureshell:
                if OS.windows:
                    from .const9 import backslash
                    commands_old = commands
                    commands = []
                    commands.append("cmd")
                    # commands.append("/U")  # only cmd applications output in utf16,
                    #                          other applications output in default encoding D:
                    commands.append("/C")
                    commands.append(" ".join(commands_old))
            from .print9 import Print
            output = cls._get_output_with_timeout(*commands, print_std=print_std, decoding=decoding,
                                                  timeout=timeout)
        else:
            output = cls._get_output(*commands, print_std=print_std, decoding=decoding, pureshell=pureshell,
                                     universal_newlines=universal_newlines)

        out = output[0]
        err = output[1]
        if return_merged:
            return out + err
        return out, err

    @classmethod
    def fit(cls, *strings, sep=" "):
        """Fit strings to console
        <br>`return` strings, that can be fit in one line print
        """
        from .os9 import OS
        from .list9 import List
        console_width = cls.width()
        if OS.windows:  # windows add symbol to end of string :(
            console_width -= 1
        strings = List.to_strings(strings)  # replace all to strings
        len_all = len(sep.join(strings))  # count len of all

        # check for fit
        if len_all <= console_width:
            pass
        else:
            # get longest line
            longest_string = ""
            for string in strings:
                string = str(string)
                if len(string) > len(longest_string):
                    longest_string = string

            # cut line
            cut_cnt = len_all - console_width
            new_longest_string = longest_string[cut_cnt:]
            new_longest_string = ">>" + new_longest_string[2:]

            # replace
            strings = List.replace_string(strings, longest_string, new_longest_string)

        return strings

