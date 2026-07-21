# Consolidated tests for commands/gui.py (unit)

# ---- from test_gui9.py ----


import pytest


def test_gui9_import():
    from commands import Gui
    assert Gui is not None


def test_gui_instance_helper(monkeypatch):
    from commands.gui import Gui
    from commands.macos import macOS
    from commands.print import Print
    from commands.os import OS
    calls = []
    monkeypatch.setattr(macOS, "notification", lambda *a, **k: calls.append(("mac", a, k)))
    monkeypatch.setattr(Print, "debug", lambda *a, **k: calls.append(("debug", a, k)))
    g = Gui("hi")
    # Force macOS path to avoid NotImplementedError on other OSes
    monkeypatch.setattr(OS, "_macos", True)
    monkeypatch.setattr(OS, "_windows", False)
    g.notify(title="t", subtitle="s", sound=None)
    assert calls


# ---- from test_gui_extra.py ----


import sys

import pytest

from commands.gui import Gui
from commands.os import OS




def test_gui_warning_macos_path(monkeypatch):
    calls = []
    from commands import macOS
    monkeypatch.setattr(macOS, "notification", lambda *a, **k: calls.append(("mac", a, k)))
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    monkeypatch.setattr(OS, "_macos", True)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_python_implementation", "cpython")
    Gui.warning("hi")
    assert calls and calls[0][0] == "mac"


def test_gui_warning_non_macos_alert(monkeypatch):
    calls = []

    class DummyPyAutoGui:
        @staticmethod
        def alert(message):
            calls.append(message)

    monkeypatch.setitem(sys.modules, "pyautogui", DummyPyAutoGui)
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_python_implementation", "cpython")
    Gui.warning("hello")
    assert calls == ["hello"]


def test_gui_warning_pypy_debug_path(monkeypatch):
    debug_calls = []
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_python_implementation", "pypy")

    from commands import print as print_module
    monkeypatch.setattr(print_module.Print, "debug", lambda *a, **k: debug_calls.append(a))
    Gui.warning("check")
    assert debug_calls




# ---- from test_gui_macos_path.py ----


import types

import pytest

from commands.gui import Gui
from commands.os import OS


def test_gui_notification_macos(monkeypatch):
    calls = []
    monkeypatch.setattr(OS, "_macos", True)
    monkeypatch.setattr(OS, "_windows", False)
    class DummyMac:
        @staticmethod
        def notification(*args, **kwargs):
            calls.append((args, kwargs))
    monkeypatch.setattr("commands.macos.macOS", DummyMac)
    Gui.notification("msg", title="t")
    assert calls


def test_gui_warning_macos(monkeypatch):
    calls = []
    monkeypatch.setattr(OS, "_macos", True)
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_python_implementation", "pypy")
    monkeypatch.setattr("commands.macos.macOS.notification", lambda *a, **k: calls.append(a))
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    Gui.warning("msg")
    assert calls


# ---- from test_gui_more_coverage.py ----


import sys
import types

import pytest

from commands.gui import Gui
from commands.os import OS


def test_gui_warning_instance_uses_stored_message(monkeypatch):
    called = {}

    def fake_class_warning(msg):
        called["msg"] = msg

    monkeypatch.setattr(Gui, "_warning_class", classmethod(lambda cls, message: fake_class_warning(message)))
    g = Gui("hello")
    g.warning()
    assert called["msg"] == "hello"




def test_gui_windows_notification_covers_on_destroy_and_loadimage_except(monkeypatch):
    calls = []

    class DummyWin32Con:
        WM_DESTROY = 1
        WM_USER = 100
        NIM_ADD = 1
        NIM_MODIFY = 2
        NIM_DELETE = 3
        WS_OVERLAPPED = 1
        WS_SYSMENU = 2
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 1
        LR_DEFAULTSIZE = 2
        CW_USEDEFAULT = 0
        IDI_APPLICATION = 1

    class DummyWin32Gui:
        NIF_ICON = 1
        NIF_MESSAGE = 2
        NIF_TIP = 4
        NIF_INFO = 8
        NIM_ADD = 1
        NIM_MODIFY = 2
        NIM_DELETE = 3

        _wndproc_map = None

        class WNDCLASS:
            def __init__(self):
                self.hInstance = None
                self.lpszClassName = ""
                self.lpfnWndProc = None

        @staticmethod
        def RegisterClass(wc):
            DummyWin32Gui._wndproc_map = wc.lpfnWndProc
            return 1

        @staticmethod
        def CreateWindow(*_a, **_k):
            return 123

        @staticmethod
        def UpdateWindow(hwnd):
            calls.append(("update", hwnd))

        @staticmethod
        def LoadImage(*_a, **_k):
            raise RuntimeError("force icon load failure")

        @staticmethod
        def LoadIcon(*_a, **_k):
            calls.append(("loadicon",))
            return 7

        @staticmethod
        def Shell_NotifyIcon(*a, **k):
            calls.append(("notify", a, k))

        @staticmethod
        def DestroyWindow(hwnd):
            calls.append(("destroy", hwnd))
            # Simulate WM_DESTROY to cover OnDestroy() branch.
            if DummyWin32Gui._wndproc_map is not None:
                handler = DummyWin32Gui._wndproc_map[DummyWin32Con.WM_DESTROY]
                handler(hwnd, DummyWin32Con.WM_DESTROY, None, None)

    class DummyWin32Api:
        @staticmethod
        def GetModuleHandle(_arg):
            return 1

        @staticmethod
        def PostQuitMessage(code):
            calls.append(("quit", code))

    monkeypatch.setitem(sys.modules, "win32api", DummyWin32Api)
    monkeypatch.setitem(sys.modules, "win32gui", DummyWin32Gui)
    monkeypatch.setitem(sys.modules, "win32con", DummyWin32Con)
    monkeypatch.setitem(sys.modules, "pywintypes", types.SimpleNamespace(error=RuntimeError))

    class DummyThread:
        def __init__(self, func, args=(), daemon=False):
            self.func = func
            self.args = args
            self.daemon = daemon

        def start(self):
            self.func(*self.args)

    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr("commands.threading.MyThread", DummyThread)
    monkeypatch.setattr("time.sleep", lambda *_: None)

    Gui.notification("msg", title="t")

    assert any(c[0] == "loadicon" for c in calls)
    assert any(c[0] == "quit" for c in calls)


# ---- from test_gui_warning_inputs.py ----


import sys

import pytest

from commands.gui import Gui
from commands.os import OS


def test_gui_warning_sysargv_error(monkeypatch):
    # Force sys.argv IndexError path
    monkeypatch.setattr(sys, "argv", [])
    called = []

    class DummyPrint:
        @staticmethod
        def debug(*args, **kwargs):
            called.append(args)

    monkeypatch.setattr("commands.print.Print", DummyPrint)
    monkeypatch.setattr("commands.os.OS._macos", False)
    monkeypatch.setattr("commands.os.OS._windows", False)
    monkeypatch.setattr("commands.os.OS._python_implementation", "pypy")
    monkeypatch.setattr("builtins.input", lambda *a, **k: "")
    Gui.warning("msg")
    assert called  # Print.debug invoked in PyPy path


def test_gui_class_warning_pypy(monkeypatch):
    debug_calls = []
    input_calls = []
    monkeypatch.setattr("commands.os.OS._macos", False)
    monkeypatch.setattr("commands.os.OS._windows", False)
    monkeypatch.setattr("commands.os.OS._python_implementation", "pypy")
    monkeypatch.setattr("commands.print.Print.debug", lambda *args, **_kwargs: debug_calls.append(args))
    monkeypatch.setattr("builtins.input", lambda prompt: input_calls.append(prompt) or "")
    Gui.warning("hello")
    assert debug_calls == [("PyPy doesn't support pyautogui, so warning is here:", "hello")]
    assert input_calls == ["Press Enter to continue"]




# ---- from test_gui_windows_notification.py ----


import sys
import types

import pytest

from commands.gui import Gui
from commands.os import OS


def test_gui_windows_notification_spawn(monkeypatch):
    calls = []

    class DummyWin32Con:
        WM_DESTROY = 1
        WM_USER = 1
        NIM_ADD = 1
        NIM_MODIFY = 1
        NIM_DELETE = 1
        WS_OVERLAPPED = 1
        WS_SYSMENU = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 1
        LR_DEFAULTSIZE = 1
        CW_USEDEFAULT = 1
        IDI_APPLICATION = 1

    class DummyWin32Gui:
        NIF_ICON = 1
        NIF_MESSAGE = 2
        NIF_TIP = 4
        NIF_INFO = 8
        NIM_ADD = 1
        NIM_MODIFY = 2
        NIM_DELETE = 3
        class WNDCLASS:
            def __init__(self):
                self.hInstance = None
                self.lpszClassName = ""
                self.lpfnWndProc = None

        @staticmethod
        def RegisterClass(wc):
            return 1

        @staticmethod
        def CreateWindow(*args, **kwargs):
            return 1

        @staticmethod
        def UpdateWindow(hwnd):
            calls.append(("update", hwnd))

        @staticmethod
        def LoadImage(*a, **k):
            return 1

        @staticmethod
        def LoadIcon(*a, **k):
            return 1

        @staticmethod
        def Shell_NotifyIcon(*a, **k):
            calls.append(("notify", a, k))

        @staticmethod
        def DestroyWindow(hwnd):
            calls.append(("destroy", hwnd))

    class DummyWin32Api:
        @staticmethod
        def GetModuleHandle(arg):
            return 1

        @staticmethod
        def PostQuitMessage(code):
            calls.append(("quit", code))

    monkeypatch.setitem(sys.modules, "win32api", DummyWin32Api)
    monkeypatch.setitem(sys.modules, "win32gui", DummyWin32Gui)
    monkeypatch.setitem(sys.modules, "win32con", DummyWin32Con)
    monkeypatch.setitem(sys.modules, "pywintypes", types.SimpleNamespace(error=RuntimeError))

    class DummyThread:
        def __init__(self, func, args=(), daemon=False):
            self.func = func
            self.args = args
            calls.append(("thread_init", func, args, daemon))

        def start(self):
            self.func(*self.args)

    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr("commands.gui.MyThread", DummyThread, raising=False)
    monkeypatch.setattr("time.sleep", lambda *_: None)

    Gui.notification("msg", title="t")
    assert any(entry[0] == "notify" for entry in calls)




# ---- from test_gui_windows_retry.py ----


import sys
import types

import pytest

from commands.gui import Gui
from commands.os import OS




def test_gui_notification_windows_retry_and_destroy(monkeypatch):
    calls = {"notify": 0, "destroy": 0}

    class DummyWin32Con:
        WM_DESTROY = 1
        WM_USER = 1
        NIM_ADD = 1
        NIM_MODIFY = 2
        NIM_DELETE = 3
        WS_OVERLAPPED = 1
        WS_SYSMENU = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 1
        LR_DEFAULTSIZE = 1
        CW_USEDEFAULT = 1
        IDI_APPLICATION = 1
        NIF_ICON = 1
        NIF_MESSAGE = 2
        NIF_TIP = 4
        NIF_INFO = 8

    class DummyWin32Gui:
        class WNDCLASS:
            def __init__(self):
                self.hInstance = None
                self.lpszClassName = ""
                self.lpfnWndProc = None

        NIF_ICON = 1
        NIF_MESSAGE = 2
        NIF_TIP = 4
        NIF_INFO = 8
        NIM_ADD = 1
        NIM_MODIFY = 2
        NIM_DELETE = 3

        def __init__(self):
            self._register_calls = 0

        def RegisterClass(self, wc):
            self._register_calls += 1
            if self._register_calls == 1:
                raise DummyError("fail register")
            return 1

        @staticmethod
        def CreateWindow(*args, **kwargs):
            return 1

        @staticmethod
        def UpdateWindow(hwnd):
            calls["update"] = hwnd

        @staticmethod
        def LoadImage(*a, **k):
            return 1

        @staticmethod
        def LoadIcon(*a, **k):
            return 1

        @staticmethod
        def Shell_NotifyIcon(*a, **k):
            calls["notify"] += 1

        @staticmethod
        def DestroyWindow(hwnd):
            calls["destroy"] += 1

    class DummyWin32Api:
        @staticmethod
        def GetModuleHandle(arg):
            return 1

        @staticmethod
        def PostQuitMessage(code):
            calls["quit"] = code

    class DummyError(Exception):
        pass

    dummy_gui = DummyWin32Gui()
    monkeypatch.setitem(sys.modules, "win32api", DummyWin32Api)
    monkeypatch.setitem(sys.modules, "win32gui", dummy_gui)
    monkeypatch.setitem(sys.modules, "win32con", DummyWin32Con)
    monkeypatch.setitem(sys.modules, "pywintypes", types.SimpleNamespace(error=DummyError))
    monkeypatch.setattr("commands.random.Random.string", staticmethod(lambda length: "x" * length))
    monkeypatch.setattr("time.sleep", lambda *_: None)
    monkeypatch.setattr("os.path.abspath", lambda p: p)
    monkeypatch.setattr("os.path.join", lambda *parts: "/".join(parts))
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr("commands.threading.MyThread", lambda func, args=(), daemon=False: types.SimpleNamespace(start=lambda: func(*args)))

    Gui.notification("hello", title="t")
    assert calls["notify"] >= 1
    assert calls["destroy"] >= 1
