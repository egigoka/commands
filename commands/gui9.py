#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with gui
"""
__version__ = "0.4.3"


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
            # https://gist.github.com/wontoncc/1808234
            class WindowsBalloonTip:
                def __init__(self, title, msg):
                    import os
                    import sys
                    import time
                    import win32api
                    import win32gui
                    import win32con

                    message_map = {
                        win32con.WM_DESTROY: self.OnDestroy,
                    }
                    # Register the Window class.
                    wc = win32gui.WNDCLASS()
                    hinst = wc.hInstance = win32api.GetModuleHandle(None)
                    wc.lpszClassName = "PythonTaskbar"
                    wc.lpfnWndProc = message_map  # could also specify a wndproc.
                    classAtom = win32gui.RegisterClass(wc)
                    # Create the Window.
                    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
                    self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar", style,
                                             0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                             0, 0, hinst, None)
                    win32gui.UpdateWindow(self.hwnd)
                    iconPathName = os.path.abspath(os.path.join(sys.path[0], "balloontip.ico"))
                    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
                    try:
                        hicon = win32gui.LoadImage(hinst, iconPathName,
                                          win32con.IMAGE_ICON, 0, 0, icon_flags)
                    except:
                        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
                    flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
                    nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
                    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
                    win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,
                                     (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER + 20,
                                      hicon, "Balloon  tooltip", title, 200, msg))
                    # self.show_balloon(title, msg)
                    time.sleep(10)
                    win32gui.DestroyWindow(self.hwnd)

                def OnDestroy(self, hwnd, msg, wparam, lparam):
                    import win32api
                    import win32gui
                    nid = (self.hwnd, 0)
                    win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
                    win32api.PostQuitMessage(0)  # Terminate the app.

            def notification(title, message):
                WindowsBalloonTip(title=title, msg=message)

            from .threading9 import MyThread
            t = MyThread(notification, args=(title, message), daemon=True)
            t.start()
        else:
            raise NotImplementedError("OS not in ['Windows', 'macOS'] not supported yet")