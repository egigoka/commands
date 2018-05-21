#! python3
# -*- coding: utf-8 -*-
# http://python.su/forum/topic/15531/?page=1#post-93316
__version__ = "0.1.3"


class Console():
    @staticmethod
    def clean():
        """Wipe terminal output. Not tested on linux
        todo test on linux
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
    def width():  # return width of terminal window in characters
        from .os8 import OS
        if OS.windows:
            import shutil
            width_ = shutil.get_terminal_size().columns
        elif OS.unix_family:
            io = Console.get_output("stty size")
            width_ = Str.get_integers(io)[1]
        return int(width_)

    @staticmethod
    def height():
        """Return height of terminal window in characters
        """
        from .os8 import OS
        if OS.windows:
            import shutil
            height = width_ = shutil.get_terminal_size().lines
        elif OS.unix_family:
            sttysize = Console.get_output("stty size")
            height = Str.get_integers(sttysize)[0]
        if height > 100:
            height = 100
        return int(height)

    @classmethod
    def blink(cls, width=None, height=None, symbol="#", sleep=0.5):
        """fastly print to terminal characters with random color. Completely
        shit. Arguments width and height changing size of terminal, works only
        in Windows.
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
        import colorama
        colorama.init()
        while True:
            colors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
            highlights = ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan", "on_white"]
            string = symbol * width
            color = random.choice(colors)
            colors.pop(colors.index(color))
            highlight = random.choice(highlights)
            try: # New version with one long line. Works perfect, as I see.
                import time
                import termcolor
                string = string * height
                print(termcolor.colored(string, color, highlight))
                time.sleep(sleep)
            except KeyboardInterrupt as err:
                print(termcolor.colored("OK", "white", "on_grey"))
                colorama.deinit()
                cls.clean()
                break


    @staticmethod
    def get_output(command):
        """Return output of executing command. Doesn't output it to terminal in
        realtime. Can be output after done if "quiet" argument activated.
        """
        import subprocess
        from .os8 import OS
        p = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        if OS.windows:
            output = p.decode("cp866")
        elif OS.family == "unix":
            output = p.decode("utf8")
        return output
