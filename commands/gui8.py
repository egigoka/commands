#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with gui
"""
__version__ = "0.3.1"


class Gui:  # pylint: disable=too-few-public-methods
    """Class to interact with gui
    """
    @staticmethod
    def warning(message):
        """Starts Tkinter window with message to user
        :param message: string with message to user
        :return: None
        """
        import sys
        from .print8 import Print
        from .os8 import OS
        try:
            try:
                not_dot_py = sys.argv[0][-3:] != ".py"  # todo check logic
            except IndexError:
                not_dot_py = True
            Print.debug("not_dot_py", not_dot_py)
            # if (not_dot_py or (sys.argv[0] != "")) and (not OS.running_in_repl()):  # I forgot why sys.argv[0] must not be empty, so ... 06/13/2018
                # Print.debug("sys.argv", sys.argv)
                # Print.debug("Something wrong with sys.argv. Tkinter doesn't like it.")
        except IndexError:
            Print.debug("sys.argv", sys.argv)
            raise RuntimeError("Something wrong with sys.argv. Tkinter doesn't like it!")
        if OS.macos:
            from .macos8 import macOS
            macOS.notification(message)
        if (not OS.macos) and (OS.python_implementation != "pypy"):
            import pyautogui
            pyautogui.alert(message)
        else:
            Print.debug("PyPy doesn't support pyautogui, so warning is here:", message)
            input("Press Enter to continue")
