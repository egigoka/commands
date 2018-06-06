#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing processes.
"""
__version__ = "0.1.3"


class Process:
    """Class with functions for managing processes.
    """
    @staticmethod
    def kill(process):
        """
        :param process: process name or PID
        :return: None
        """
        import os
        from .os8 import OS
        if OS.windows:
            try:
                int(process)
                command_ = "taskkill /f /pid " + str(process)
            except ValueError:
                if not process.endswith(".exe"):
                    process = process + ".exe"
                command_ = "taskkill /f /im " + process
        elif OS.macos:
            command_ = "killall " + str(process)
            try:
                int(process)
                command_ = "kill " + str(process)
            except ValueError:
                pass
        else:
            from .gui8 import Gui
            Gui.warning("OS not supported")
        os.system(command_)

    @staticmethod
    def start(*arguments, new_window=False, debug=False, pureshell=False):  # pylint: disable=too-many-branches
        """
        :param arguments: strings, arguments to start process, include name
        :param new_window: boolean, open process in new window
        :param debug: boolean, debug
        :param pureshell: boolean, use only first argument from *arguments, not processing others
        :return: None
        """
        import os
        from .list8 import List
        from .os8 import OS
        from .str8 import Str
        arguments = List.flatterize(arguments)
        if debug:
            from .print8 import Print
            Print.debug("Process.start arguments", arguments)
        if new_window or pureshell:
            for argument_ in arguments:
                if " " in argument_ and argument_[:1] != "-":
                    if OS.windows:
                        argument_ = Str.to_quotes(argument_)
                    else:
                        argument_ = Str.to_quotes_2(argument_)
                try:
                    command = command + " " + argument_  # pylint: disable=used-before-assignment
                except NameError:
                    if new_window:
                        if OS.windows:
                            command = 'start "" ' + argument_
                        elif OS.macos:
                            from .gui8 import Gui
                            Gui.warning("macOS doesn't support creating new window now")
                            # command = "" +
                    else:
                        command = argument_
            os.system(command)
        else:
            if OS.windows:
                import subprocess
                commands = []
                for argument_ in arguments:
                    commands.append(str(argument_))
                subprocess.call(commands)
            elif OS.macos:
                commands = ""
                for argument_ in arguments:
                    commands += str(argument_) + " "
                # print(commands)
                os.system(commands)