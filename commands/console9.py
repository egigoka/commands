#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.11.11"


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
    def _get_output_with_timeout(commands, print_std, decoding, timeout):
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

                print(line, end="", flush=True)
            return True

        def save_stderr(stderr):
            if decoding:
                stderr = stderr.decode(decoding)
            State.stderr = stderr
            if print_std and stderr:
                print(f"stderr:\n{stderr}", flush=True)

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
    def _get_output(commands, print_std, decoding, pureshell, universal_newlines, debug=False):
        import subprocess
        from .threading9 import Threading

        is_string = decoding or universal_newlines

        try:
            with subprocess.Popen(commands, shell=pureshell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=universal_newlines) as popen_object:

                def print_out_lines(obj, color, is_string: bool):
                    output = b''
                    if is_string:
                        output = ''
                    for string in popen_object.stdout:
                        if decoding:
                            try:
                                string = string.decode(decoding)
                            except UnicodeDecodeError as e:
                                print(f"line: '{string}', decoding: '{decoding}'")
                                raise
                        output += string
                        if print_std:
                            from .print9 import Print
                            Print.colored(string, end='', flush=True)
                    return output

                pipes = Threading(verbose=debug)

                pipes.add(print_out_lines, "stdout",
                          kwargs={"obj": popen_object.stdout, "color": "green", "is_string": is_string})
                pipes.add(print_out_lines, "stderr",
                          kwargs={"obj": popen_object.stderr, "color": "red", "is_string": is_string})

                pipes.start(wait_for_keyboard_interrupt=True)

                out, err = pipes.get_results()

        except FileNotFoundError as exception:
            if debug:
                from .print9 import Print
                Print.debug("commands", commands, "pureshell", pureshell, "print_std", print_std, "decoding", decoding,
                            "universal_newlines", universal_newlines)
            raise FileNotFoundError(exception)
        return out, err

    windows_cp65001 = False
    windows_cp65001_fail = False

    @classmethod
    def get_output(cls, *commands, pureshell=False, print_std=False, decoding=None, universal_newlines=False,
                   auto_decoding=True, auto_disable_py_buffering=True, return_merged=True, timeout=None, debug=False,
                   create_cmd_subprocess=False):
        """Return output of executing command.
        <br>`param commands` list[string if pureshell is True] with command and arguments
        <br>`param pureshell` boolean, if True, the specified command will be executed through the shell
        <br>`param print_std` boolean, if True, output from command will be printed immideately (also adds argument -u to
        'py' or 'python' firs arg.)
        <br>`return` typle with strings stdout and stderr
        """
        import os
        from .os9 import OS
        if len(commands) == 1:
                commands = commands[0]
        if isinstance(commands, str) and not pureshell:
            import shlex
            commands = shlex.split(commands, posix=False)

        if isinstance(commands, list) or isinstance(commands, tuple):
            from .list9 import List
            commands = List.to_strings(commands)

        if not commands:
            raise IndexError("commands must not be empty")

        # disable buffering for python
        if ("py" in commands or "py" in os.path.split(commands[0])[1]) and print_std and auto_disable_py_buffering:
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
                        win_cp = Windows.fix_unicode_encode_error(safe=False)
                        cls.windows_cp65001 = True
                        decoding = "cp65001"
                    except IOError:  # if cp65001 cannot be setted
                        cls.windows_cp65001_fail = True
                        decoding = f"cp{Windows.get_cmd_code_page()}"
            elif OS.unix_family:
                decoding = "utf8"
            else:
                universal_newlines = True

        if decoding and universal_newlines:
            raise TypeError("can't decode 'str' to 'str', set universal_newlines to False for manually set decoding")
        if timeout and universal_newlines:
            raise NotImplementedError("asyncio.subprocess doesn't support 'universal_newlines', disable 'auto_decoding'"
                                      " or set 'decoding'")

        if (timeout and pureshell and OS.windows) or create_cmd_subprocess:
            commands_old = commands
            commands = list()
            commands.append("cmd")
            # commands.append("/U")  # only cmd applications output in utf16,
            #                          other applications output in default encoding D:
            commands.append("/C")
            commands.append(" ".join(commands_old))

        if timeout:
            output = cls._get_output_with_timeout(commands, print_std=print_std, decoding=decoding,
                                                  timeout=timeout)
            if output[3]:
                raise TimeoutError(fr"Timeout {timeout} reached while running {commands}")
        else:
            output = cls._get_output(commands, print_std=print_std, decoding=decoding, pureshell=pureshell,
                                     universal_newlines=universal_newlines, debug=debug)
        out = output[0]
        err = output[1]
        if return_merged:
            return out + err
        return out, err

    @classmethod
    def fit(cls, *strings: str, sep: str = " "):
        """Fit strings to console
        <br>`return` strings, that can be fit in one line print
        <br> yes, implementation is far beyond good
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
            longest_string = 0
            for cnt, string in enumerate(strings):
                if len(string) > len(strings[longest_string]):
                    longest_string = cnt

            # cut line
            cut_cnt = len_all - console_width
            new_longest_string = strings[longest_string][cut_cnt:]
            new_longest_string = ">>" + new_longest_string[2:]

            # replace
            strings[longest_string] = new_longest_string

        return strings

