#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Process:
    @staticmethod
    def kill(process):
        import os
        from .os8 import OS
        if OS.windows:
            command_ = "taskkill /f /im " + str(process) + ".exe"
            try:
                int(process)
                command_ = "taskkill /f /pid " + str(process)
            except:
                pass
        elif OS.macos:
            command_ = "killall " + str(process)
            try:
                int(process)
                command_ = "kill " + str(process)
            except:
                pass
        else:
            from .gui8 import Gui
            Gui.warning("OS not supported")
        os.system(command_)

    @staticmethod
    def start(*arguments, new_window=False, debug=False, pureshell=False):
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
                    command = command + " " + argument_
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