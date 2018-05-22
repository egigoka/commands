#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.3"


class Gui:
    @staticmethod
    def warning(message):
        import sys
        from .print8 import Print
        from .os8 import OS
        try:
            try:
                sys.ps1
                sys.ps2
                interactive_mode = True
            except:
                interactive_mode = False
            # Print.debug("interactive_mode", interactive_mode)
            try:
                not_dot_py = sys.argv[0][-3] != ".py"  # todo check logic
            except:
                not_dot_py = True

            if (not_dot_py or (sys.argv[0] != "")) and (not interactive_mode):
                Print.debug("sys.argv", sys.argv)
                Print.debug("Something wrong with sys.argv. Tkinter doesn't like it.")
                input()
        except IndexError:
            Print.debug("sys.argv", sys.argv)
            raise RuntimeError("Something wrong with sys.argv. Tkinter doesn't like it.")
        if OS.macos:
            from .macos8 import macOS
            macOS.notification(message)
        if (not OS.macos) and (OS.python_implementation != "pypy"):
            try:
                import pyautogui
            except ModuleNotFoundError:
                from .installreq8 import pyautogui
            pyautogui.alert(message)
        else:
            Print.debug("PyPy doesn't support pyautogui, so warning is here:", message)
            input("Press Enter to continue")