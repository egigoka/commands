#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with gui
"""
__version__ = "0.4.2"


class Gui:  # pylint: disable=too-few-public-methods
    """Class to interact with gui
    """
    @staticmethod
    def warning(message):
        """Starts Tkinter window with message to user
        <br>`param message` string with message to user
        <br>`return` None
        """
        import sys
        from .print9 import Print
        from .os9 import OS
        try:
            try:
                not_dot_py = sys.argv[0][-3:] != ".py"  # todo check logic
            except IndexError:
                not_dot_py = True
            # if (not_dot_py or (sys.argv[0] != "")) and (not OS.running_in_repl()):  # I forgot why sys.argv[0] must not be empty, so ... 06/13/2018
                # Print.debug("sys.argv", sys.argv)
                # Print.debug("Something wrong with sys.argv. Tkinter doesn't like it.")
        except IndexError:
            Print.debug("sys.argv", sys.argv)
            raise RuntimeError("Something wrong with sys.argv. Tkinter doesn't like it!")
        if OS.macos:
            from .macos9 import macOS
            macOS.notification(message)
        if (not OS.macos) and (OS.python_implementation != "pypy"):
            import pyautogui
            pyautogui.alert(message)
        else:
            Print.debug("PyPy doesn't support pyautogui, so warning is here:", message)
            input("Press Enter to continue")

    @classmethod
    def notification(cls, message, title="python3", subtitle=None, sound=None):
        from .os9 import OS
        if OS.macos:
            from .macos9 import macOS
            macOS.notification(cls, message, title=title, subtitle=subtitle, sound=sound)
        elif OS.windows:
            if OS.windows_version >= 10:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()

                from .threading9 import MyThread
                t = MyThread(toaster.show_toast, args=(title, message), kwargs={"icon_path":None, "threaded":False}, daemon=True)
                t.start()

            else:
                raise NotImplementedError("Windows below 10 not supported yet")
        else:
            raise NotImplementedError("OS not in ['Windows', 'macOS'] not supported yet")