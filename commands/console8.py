#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with terminal|console
"""
__version__ = "0.1.10"


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
        from .os8 import OS
        if OS.windows:
            os.system("cls")
        elif OS.linux:
            import shutil
            from .const8 import newline
            print(newline * shutil.get_terminal_size().lines)
        elif OS.macos:
            os.system(r"clear && printf '\e[3J'")

    @staticmethod
    def width():
        """
        :return: int width of opened console in chars
        """
        from .os8 import OS
        if OS.windows:
            import shutil
            width_ = shutil.get_terminal_size().columns
        elif OS.unix_family:
            from .str8 import Str
            io_string = Console.get_output("stty size")
            width_ = Str.get_integers(io_string)[1]
        return int(width_)

    @staticmethod
    def height():
        """
        :return: int height of opened console in chars
        """
        from .os8 import OS
        if OS.windows:
            import shutil
            height = shutil.get_terminal_size().lines
        elif OS.unix_family:
            from .str8 import Str
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
        from .os8 import OS
        if (width is not None) and (height is not None) and OS.windows:
            import os
            os.system("mode con cols=" + str(width) + " lines=" + str(height))
        if width is None:
            width = cls.width()
        if height is None:
            height = cls.height()
        try:
            import colorama
        except ModuleNotFoundError:
            from .installreq8 import colorama
        colorama.init()
        while True:
            colors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
            highlights = ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_white"]
            string = symbol * width
            color = random.choice(colors)
            colors.pop(colors.index(color))
            highlight = random.choice(highlights)
            try:  # New version with one long line. Works perfect, as I see.
                import time
                try:
                    import termcolor
                except ModuleNotFoundError:
                    from .installreq8 import termcolor
                string = string * height
                print(termcolor.colored(string, color, highlight))
                time.sleep(sleep)
            except KeyboardInterrupt:
                print(termcolor.colored("OK", "white", "on_grey"))
                colorama.deinit()
                cls.clean()
                break


    @staticmethod
    def get_output(command):
        """Return output of executing command. Doesn't output it to terminal in
        realtime.
        :param command: single string with command
        :return: single string with output of executing command.
        """
        import subprocess
        from .os8 import OS
        io_string = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        if OS.windows:
            output = io_string.decode("cp866")
        elif OS.unix_family:
            output = io_string.decode("utf8")
        return output
