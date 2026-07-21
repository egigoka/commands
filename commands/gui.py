#! python3
# -*- coding: utf-8 -*-
"""Internal module to interact with gui."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value

from .module import LazyModule, LazyProperty

__version__ = "0.4.6"
sys = LazyModule("sys")
os = LazyModule("os")
time = LazyModule("time")
Print = LazyProperty(".print", "Print")
OS = LazyProperty(".os", "OS")
macOS = LazyProperty(".macos", "macOS")
Random = LazyProperty(".random", "Random")
MyThread = LazyProperty(".threading", "MyThread")

pyautogui = LazyModule("pyautogui", optional=True)
win32api = LazyModule("win32api", optional=True)
win32gui = LazyModule("win32gui", optional=True)
win32con = LazyModule("win32con", optional=True)
pywintypes = LazyModule("pywintypes", optional=True)


class Gui:  # pylint: disable=too-few-public-methods
    """Class to interact with gui."""

    warning: "Gui._DualMethod"

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def _warning_instance(self, message: Optional[str] = None) -> None:
        msg = self.message if message is None else message
        if msg is None:
            raise ValueError("Message is not set")
        self.__class__.warning(msg)

    def notify(
        self,
        title: str = "python3",
        subtitle: Optional[str] = None,
        sound: Optional[str] = None
    ) -> None:
        """Send a notification using stored message."""
        if self.message is None:
            raise ValueError("Message is not set")
        self.__class__.notification(self.message, title=title, subtitle=subtitle, sound=sound)

    @classmethod
    def _warning_class(cls, message: str) -> None:
        """Start a warning UI with a message.

        <br>`param message` string with message to user
        <br>`return` None
        """
        try:
            _ = sys.argv[0][-3:] != ".py"  # todo check logic
        except IndexError:
            pass
        if OS.macos:
            macOS.notification(message)
        if (not OS.macos) and (OS.python_implementation != "pypy"):
            pyautogui.alert(message)
        else:
            Print.debug("PyPy doesn't support pyautogui, so warning is here:", message)
            input("Press Enter to continue")

    class _DualMethod:
        def __init__(self, instance_attr: str, class_attr: str) -> None:
            self._instance_attr = instance_attr
            self._class_attr = class_attr

        def __get__(self, instance: Optional["Gui"], owner: type) -> Any:
            if instance is None:
                return getattr(owner, self._class_attr)
            return getattr(instance, self._instance_attr)

    @classmethod
    def notification(
        cls,
        message: str,
        title: str = "python3",
        subtitle: Optional[str] = None,
        sound: Optional[str] = None
    ) -> None:
        """Send a GUI notification."""
        if OS.macos:
            macOS.notification(message, title=title, subtitle=subtitle, sound=sound)
        elif OS.windows:
            # https://gist.github.com/wontoncc/1808234
            class WindowsBalloonTip:
                def __init__(self, title: str, msg: str) -> None:

                    message_map = {
                        win32con.WM_DESTROY: self.OnDestroy,
                    }
                    # Register the Window class.
                    wc = win32gui.WNDCLASS()
                    hinst = wc.hInstance = win32api.GetModuleHandle(None)
                    # fucc
                    wc.lpszClassName = "PythonTaskbar" + Random.string(100)
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
                    time.sleep(60)
                    win32gui.DestroyWindow(self.hwnd)

                def OnDestroy(self, hwnd: Any, msg: Any, wparam: Any, lparam: Any) -> None:
                    nid = (self.hwnd, 0)
                    win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
                    win32api.PostQuitMessage(0)  # Terminate the app.

            def notification(title: str, message: str) -> None:
                cnt = 0
                while cnt < 10:
                    cnt += 1
                    try:
                        WindowsBalloonTip(title=title, msg=message)
                        return
                    except pywintypes.error as err:
                        print(err)
                        pass

            t = MyThread(notification, args=(title, message), daemon=True)
            t.start()
        else:
            raise NotImplementedError("OS not in ['Windows', 'macOS'] not supported yet")


Gui.warning = Gui._DualMethod("_warning_instance", "_warning_class")
