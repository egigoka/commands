#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.7.2"


class Console:
    """Class to interact with terminal|console
    """
    @staticmethod
    def clean():
        """Wipe terminal output. Not tested on linux
        todo test on linux, make better
        :return: None
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
        :return: int width of opened console in chars
        """
        from .os9 import OS
        if OS.windows:
            import shutil
            width_ = shutil.get_terminal_size().columns
        elif OS.unix_family:
            from .str9 import Str
            io_string = Console.get_output("stty size")
            width_ = Str.get_integers(io_string)[1]
        return int(width_)

    @staticmethod
    def height():
        """
        :return: int height of opened console in chars
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
        :param width: int width of blinking rectangle
        :param height: int height of blinking rectangle
        :param symbol: string of characters, that fill blinking rectangle
        :param sleep: int|float define sleep between print new colored rectangle
        :return:
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
    def get_output(*commands, pureshell=False, print_std=False, decoding=None, universal_newlines=False,
                   auto_decoding=True, auto_disable_py_buffering=True, return_merged=True):
        """Return output of executing command.
        :param commands: list[string if pureshell is True] with command and arguments
        :param pureshell: boolean, if True, the specified command will be executed through the shell
        :param print_std: boolean, if True, output from command will be printed immideately (also adds argument -u to
        'py' or 'python' firs arg.)
        :return: typle with strings stdout and stderr
        """
        import subprocess
        from .os9 import OS
        if len(commands) == 1:
                commands = commands[0]

        # disable buffering for python
        if ("py" in commands or "py" in commands[0]) and print_std and auto_disable_py_buffering:
            if "-u" not in commands:
                from .print9 import Print
                Print.debug("Console.get_output", "type(commands)", type(commands))
                if isinstance(commands, str):
                    import shlex
                    list_commands = shlex.split(commands, posix=False)
                else:
                    list_commands = list(commands)

                list_commands.insert(1, "-u")
                commands = list_commands

                if isinstance(commands, str):
                    commands = " ".join(list_commands)
        # end disabling buffering for python

        # set decoding and init
        if auto_decoding and not decoding and not universal_newlines:
            if OS.windows:
                decoding = "cp866"
            elif OS.unix_family:
                decoding = "utf8"
            else:
                universal_newlines = True

        if decoding and universal_newlines:
            raise TypeError("can't decode str to str, set universal_newlines to False for manually set decoding")

        if decoding:
            out = ""
            err = ""
        else:
            out = b''
            err = b''
        # end setting decoding and init

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

        if return_merged:
            return out + err
        return out, err

    @staticmethod
    def get_output_old(*commands, pureshell=False):
        """Return output of executing command. Doesn't output it to terminal in
        realtime.
        :param commands: list with command and arguments
        :return: single string with output of executing command.
        """
        import subprocess
        from .os9 import OS
        out, err = subprocess.Popen(commands, shell=pureshell, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if OS.windows:
            output = out.decode("cp866") + err.decode("cp866")
        elif OS.unix_family:
            output = out.decode("utf8") + err.decode("utf8")
        else:
            output = out.decode() + err.decode()
        return output

    @classmethod
    def fit(cls, *strings, sep=" "):
        """Fit strings to console
        :return: strings, that can be fit in one line print
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
