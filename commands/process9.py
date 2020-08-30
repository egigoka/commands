#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing processes.
"""
__version__ = "2.0.0"


class Process:
    """Class with functions for managing processes.
    """
    @staticmethod
    def kill(process):
        """
        <br>`param process` process name or PID
        <br>`return` None
        """
        from .os9 import OS
        from .console9 import Console
        if OS.windows:
            try:
                int(process)
                command_ = "taskkill /f /pid " + str(process)
            except ValueError:
                if not process.endswith(".exe"):
                    process = process + ".exe"
                command_ = "taskkill /f /im " + process
        elif OS.unix:
            command_ = "killall " + str(process)
            try:
                int(process)
                command_ = "kill " + str(process)
            except ValueError:
                pass
        else:
            raise NotImplementedError("OS not supported, now only Windows and macOS")
        return Console.get_output(command_)
