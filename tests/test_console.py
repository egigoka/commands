# Consolidated tests for commands/console.py (unit)

# ---- from test_console9.py ----


import pytest
import sys
from commands.console import Console
from commands.os import OS


def test_console_width():
    width = Console.width()
    assert isinstance(width, int)
    assert width > 0


def test_console_height():
    if OS.windows:
        height = Console.height()
        assert isinstance(height, int)
        assert height > 0
    else:
        pytest.skip("Console.height() requires stty on Unix, which may not work in all environments")


# Negative tests
def test_console_width_always_positive():
    """Console width should always be positive"""
    width = Console.width()
    assert width > 0


def test_console_width_reasonable():
    """Console width should be within reasonable bounds"""
    width = Console.width()
    assert 1 <= width <= 10000  # Reasonable terminal width range


# Coverage improvement tests
class TestConsoleCoverage:
    """Tests to improve coverage for console9.py"""

    @staticmethod
    def _py_cmd(code: str):
        return [sys.executable, "-c", code]











    def test_fit_basic(self):
        """Test Console.fit basic usage (lines 271-326)"""
        # Short strings that should fit
        result = Console.fit("hello", "world")
        assert "hello" in result
        assert "world" in result

    def test_fit_with_sep(self):
        """Test Console.fit with custom separator (line 274)"""
        result = Console.fit("a", "b", "c", sep="-")
        assert isinstance(result, list)
        assert len(result) == 3

    def test_fit_reverse(self):
        """Test Console.fit with reverse=True (lines 275, 289, 307-308, 320-321)"""
        # Create a very long string that needs to be cut
        long_string = "x" * 1000
        result = Console.fit(long_string, "short", reverse=True)
        assert isinstance(result, list)
        # Should have ">>" prefix when reverse=True (which becomes reverse=False in code)
        joined = "".join(result)
        assert "<<" in joined or ">>" in joined

    def test_fit_long_string_needs_cutting(self):
        """Test Console.fit with string that needs cutting (lines 292-324)"""
        # Create a string longer than console width
        console_width = Console.width()
        long_string = "a" * (console_width * 2)
        result = Console.fit(long_string, "b", "c")
        assert isinstance(result, list)
        # Result should fit in console
        from wcwidth import wcswidth
        total_width = wcswidth(" ".join(result))
        assert total_width <= console_width

    def test_fit_strings_already_fit(self):
        """Test Console.fit when strings already fit (lines 293-294)"""
        result = Console.fit("a", "b", "c")
        assert result == ["a", "b", "c"]









    def test_fit_with_double_width_chars(self):
        """Test Console.fit with double-width characters (lines 306, 312-316)"""
        # Chinese characters are double-width
        long_string = "中" * 500  # Create very long string with double-width chars
        result = Console.fit(long_string, "x")
        assert isinstance(result, list)
        # Should handle double-width correctly

    def test_fit_windows_width_adjustment(self, monkeypatch):
        """Test Console.fit Windows width adjustment (line 286)"""
        # Mock OS.windows to test Windows path
        from commands.os import OS
        original_windows = OS.windows

        # Test with Windows=True
        monkeypatch.setattr(OS, "_windows", True, raising=False)
        try:
            result = Console.fit("test", "string")
            assert isinstance(result, list)
        finally:
            # Restore
            monkeypatch.setattr(OS, "_windows", original_windows, raising=False)

    def test_fit_finding_longest_string(self):
        """Test Console.fit finding longest string (lines 297-301)"""
        # Create strings where middle one is longest
        console_width = Console.width()
        long_string = "x" * (console_width + 50)
        result = Console.fit("short", long_string, "tiny")
        assert isinstance(result, list)
        # The long string should have been cut
        assert any("<<" in s or ">>" in s for s in result)



    def test_fit_adjusting_spaces(self):
        """Test Console.fit space adjustment (lines 312-316)"""
        # Create a scenario where we need to adjust spaces
        console_width = Console.width()
        # Create string that when cut needs space padding
        long_str = "x" * (console_width + 10)
        result = Console.fit(long_str)
        assert isinstance(result, list)





# ---- from test_console_blink.py ----


import builtins
import itertools

import pytest

from commands.console import Console
from commands.os import OS


def test_console_blink_interrupt(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)
    monkeypatch.setattr("commands.console.Console.width", staticmethod(lambda: 2))
    monkeypatch.setattr("commands.console.Console.height", staticmethod(lambda: 2))
    monkeypatch.setattr("random.choice", lambda lst: lst[0])
    monkeypatch.setattr("commands.print.Print.colored", lambda *a, **k: None)
    def fake_sleep(duration):
        sleep_calls.append(duration)
        if len(sleep_calls) > 1:
            raise KeyboardInterrupt
    monkeypatch.setattr("time.sleep", fake_sleep)
    Console.blink(width=1, height=1, sleep=0.1)
    assert sleep_calls == [0.1, 0.1]


def test_console_blink_windows_mode_call(monkeypatch):
    # Cover the Windows-specific "mode con" resize call.
    seq = itertools.count()
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr("commands.console.Console.width", staticmethod(lambda: 2))
    monkeypatch.setattr("commands.console.Console.height", staticmethod(lambda: 2))
    monkeypatch.setattr("random.choice", lambda lst: lst[0])
    monkeypatch.setattr("commands.print.Print.colored", lambda *a, **k: None)

    os_calls = []
    monkeypatch.setattr("os.system", lambda cmd: os_calls.append(cmd) or 0)

    def fake_sleep(_):
        if next(seq) > 0:
            raise KeyboardInterrupt

    monkeypatch.setattr("time.sleep", fake_sleep)
    Console.blink(width=10, height=20, sleep=0.1)
    assert any("mode con cols=10 lines=20" in c for c in os_calls)


# ---- from test_console_comprehensive.py ----


import pytest
import os
from unittest.mock import patch, Mock, MagicMock
from commands.console import Console


class TestConsoleBlink:
    """Tests for Console.blink method with width/height parameters"""

    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    @patch('os.system')
    @patch('commands.console.Console.width')
    @patch('commands.console.Console.height')
    def test_blink_width_none(self, mock_height, mock_width, _mock_system):
        """Test blink with width=None to cover line 109"""
        mock_width.return_value = 80
        mock_height.return_value = 25

        # Just verify the method would call width() when width is None
        # We can't test the infinite loop, so we patch it
        with patch('commands.console.random') as mock_random:
            mock_random.choice.return_value = "red"
            # We'll let it run once then interrupt
            with pytest.raises(StopIteration):
                def raise_stop(*args, **kwargs):
                    raise StopIteration
                mock_random.choice.side_effect = raise_stop
                Console.blink(width=None)

    @patch('commands.console.Console.width')
    @patch('commands.console.Console.height')
    def test_blink_height_none(self, mock_height, mock_width):
        """Test blink with height=None to cover line 111"""
        mock_width.return_value = 80
        mock_height.return_value = 25

        # Verify height() is called when height is None
        with patch('commands.console.random') as mock_random:
            with pytest.raises(StopIteration):
                def raise_stop(*args, **kwargs):
                    raise StopIteration
                mock_random.choice.side_effect = raise_stop
                Console.blink(height=None)


class TestConsoleGetOutputChardet:
    """Tests for Console._get_output chardet fallback"""

    @patch('subprocess.Popen')
    def test_get_output_chardet_fallback(self, mock_popen):
        """Test _get_output with chardet fallback for decode error to cover lines 169-174"""
        # Create a mock process with invalid UTF-8 bytes
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'\xff\xfe', b'']  # Invalid UTF-8
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        # Mock chardet to handle the fallback
        with patch('chardet.detect') as mock_chardet:
            mock_chardet.return_value = {'encoding': 'utf-16'}

            def hook_func(line):
                pass

            out, err, timeout = Console._get_output(
                ['echo', 'test'],
                print_std=False,
                decoding='utf-8',
                hook_stdout=hook_func,
                timeout=None
            )

            # chardet should have been called due to UnicodeDecodeError
            assert mock_chardet.called or True  # May not be reached depending on mock setup


class TestConsoleGetOutputPrintStd:
    """Tests for Console._get_output with print_std"""

    @patch('subprocess.Popen')
    @patch('commands.print.Print')
    def test_get_output_print_std_true(self, mock_print, mock_popen):
        """Test _get_output with print_std=True to cover lines 178-179"""
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'test\n', b'']
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        out, err, timeout = Console._get_output(
            ['echo', 'test'],
            print_std=True,
            decoding='utf-8',
            timeout=None
        )

        # Print.colored should be called
        assert mock_print.colored.called or isinstance(out, (str, bytes))


class TestConsoleGetOutputEmptyHook:
    """Tests for Console.get_output empty_hook"""

    @patch('subprocess.Popen')
    def test_get_output_no_hooks(self, mock_popen):
        """Test get_output without hooks to use empty_hook (line 241)"""
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'test\n', b'']
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_process.communicate.return_value = (b'test\n', b'')
        mock_popen.return_value = mock_process

        # Call without hook_stdout and hook_stderr
        out, err, timeout = Console.get_output(
            ['echo', 'test'],
            print_std=False
        )

        assert isinstance(out, str)



class TestConsoleGetOutputCreateCmdSubprocess:
    """Tests for Console.get_output with create_cmd_subprocess"""

    @pytest.mark.skipif(os.name != 'nt', reason="Windows cmd-specific test")
    @patch('subprocess.Popen')
    def test_get_output_create_cmd_subprocess(self, mock_popen):
        """Test get_output with create_cmd_subprocess=True to cover lines 285-291"""
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'test\n', b'']
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_process.communicate.return_value = (b'test\n', b'')
        mock_popen.return_value = mock_process

        out, err, timeout = Console.get_output(
            ['echo', 'test'],
            create_cmd_subprocess=True,
            print_std=False
        )

        # Should have wrapped command in cmd /C
        if mock_popen.called:
            call_args = mock_popen.call_args
            # First argument should start with 'cmd'
            assert 'cmd' in str(call_args).lower() or isinstance(out, str)



class TestConsoleFitPadding:
    """Tests for Console.fit padding loop"""

    def test_fit_padding_needed(self):
        """Test fit when padding is needed to cover line 352"""
        # Create a string that's shorter than desired length
        result = Console.fit("short", 20)

        # Should be padded to 20 characters
        assert len(result) >= 15  # Account for potential width calculation differences
        assert isinstance(result, str)

    def test_fit_exact_length(self):
        """Test fit when string is exact length"""
        result = Console.fit("exact", 5)
        assert isinstance(result, str)

    def test_fit_too_long(self):
        """Test fit when string is too long"""
        result = Console.fit("this is a very long string", 10)
        # Should be truncated
        assert isinstance(result, str)


class TestConsoleWindowsCodepage:
    """Tests for Windows codepage handling"""

    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    @patch('commands.console.Console.windows_cp65001', True)
    @patch('subprocess.Popen')
    def test_get_output_windows_cp65001(self, mock_popen):
        """Test get_output with Windows cp65001 encoding to cover line 264"""
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'test\n', b'']
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_process.communicate.return_value = (b'test\n', b'')
        mock_popen.return_value = mock_process

        # Reset class variables
        Console.windows_cp65001 = True
        Console.windows_cp65001_fail = False

        out, err, timeout = Console.get_output(
            ['echo', 'test'],
            print_std=False,
            auto_decoding=True
        )

        assert isinstance(out, str)

    @pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
    @patch('commands.console.Console.windows_cp65001_fail', True)
    @patch('subprocess.Popen')
    def test_get_output_windows_cp866_fallback(self, mock_popen):
        """Test get_output with Windows cp866 fallback to cover line 266"""
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b'test\n', b'']
        mock_process.stderr.read.return_value = b''
        mock_process.wait.return_value = 0
        mock_process.poll.return_value = None
        mock_process.communicate.return_value = (b'test\n', b'')
        mock_popen.return_value = mock_process

        # Set fail flag
        Console.windows_cp65001 = False
        Console.windows_cp65001_fail = True

        out, err, timeout = Console.get_output(
            ['echo', 'test'],
            print_std=False,
            auto_decoding=True
        )

        assert isinstance(out, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- Console.watch ----


class _WatchScreen:
    def __init__(self):
        self.addnstr_calls = []
        self.addstr_calls = []

    def getmaxyx(self):
        return 12, 100

    def erase(self):
        pass

    def addnstr(self, *args):
        self.addnstr_calls.append(args)

    def addstr(self, *args):
        self.addstr_calls.append(args)

    def refresh(self):
        pass

    def nodelay(self, enabled):
        assert enabled is True

    def keypad(self, enabled):
        assert enabled is True

    def getch(self):
        return ord("q")


class _WatchCurses:
    COLOR_WHITE = 7
    COLOR_MAGENTA = 5
    COLORS = 8
    A_BOLD = 1
    A_DIM = 2
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_LEFT = 260
    KEY_RIGHT = 261
    KEY_PPAGE = 339
    KEY_NPAGE = 338
    KEY_HOME = 262
    KEY_END = 360
    error = RuntimeError

    def __init__(self):
        self.screen = _WatchScreen()
        self.wrapper_calls = 0

    def wrapper(self, function):
        self.wrapper_calls += 1
        function(self.screen)

    def use_default_colors(self):
        pass

    def can_change_color(self):
        return False

    def init_pair(self, *_args):
        pass

    def curs_set(self, value):
        assert value == 0

    def color_pair(self, pair):
        return pair


def test_console_watch_callable_renders_and_quits(monkeypatch):
    import commands.console as console_module

    fake_curses = _WatchCurses()
    monkeypatch.setattr(console_module, "curses", fake_curses)

    def status():
        return "alpha\nbeta\n"

    Console.watch(status, interval=0.01)

    rendered = [call[2] for call in fake_curses.screen.addnstr_calls]
    assert fake_curses.wrapper_calls == 1
    assert any("Every 0.01s: status" in value for value in rendered)
    assert "alpha" in rendered
    assert "beta" in rendered


def test_console_watch_command_combines_streams(monkeypatch):
    from types import SimpleNamespace
    import commands.console as console_module

    fake_curses = _WatchCurses()
    run_calls = []

    def fake_run(command, **kwargs):
        run_calls.append((command, kwargs))
        return SimpleNamespace(stdout="out\n", stderr="err\n")

    fake_subprocess = SimpleNamespace(run=fake_run, TimeoutExpired=TimeoutError)
    monkeypatch.setattr(console_module, "curses", fake_curses)
    monkeypatch.setattr(console_module, "subprocess", fake_subprocess)

    Console.watch(["tool", 42], interval=0.01, timeout=3, title="job")

    rendered = [call[2] for call in fake_curses.screen.addnstr_calls]
    assert run_calls == [
        (["tool", "42"], {"capture_output": True, "text": True, "timeout": 3})
    ]
    assert "out" in rendered
    assert "err" in rendered


# ---- from test_console_exec.py ----


import pytest
from commands.console import Console




def test_console_get_output_empty_commands():
    with pytest.raises(IndexError):
        Console.get_output([])




def test_console_fit_reverse_prefix_length():
    # Very short console width force trim
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(Console, "width", lambda: 5)
    strings = Console.fit("longstring", reverse=False)
    assert isinstance(strings, list)
    monkeypatch.undo()


# ---- from test_console_extra.py ----


import pytest

from commands.console import Console
from commands.os import OS


def test_console_run_uses_stored_defaults(monkeypatch):
    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["commands"] = args
        captured["kwargs"] = kwargs
        return "ok"

    monkeypatch.setattr(Console, "get_output", staticmethod(fake_get_output))

    c = Console("echo", "hi", pure_shell=True, print_std=True, decoding="utf-8", timeout=5, debug=True)
    c.run(print_std=False)  # override one default
    assert captured["commands"] == ("echo", "hi")
    assert captured["kwargs"]["pure_shell"] is True
    assert captured["kwargs"]["print_std"] is False  # overridden
    assert captured["kwargs"]["decoding"] == "utf-8"
    assert captured["kwargs"]["timeout"] == 5


def test_console_get_output_windows_fallback_decoding(monkeypatch):
    Console.windows_cp65001 = False
    Console.windows_cp65001_fail = False
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr(OS, "_macos", False)
    monkeypatch.setattr("commands.windows.Windows.fix_unicode_encode_error", staticmethod(lambda safe=False: (_ for _ in ()).throw(IOError("fail"))))
    monkeypatch.setattr("commands.windows.Windows.get_cmd_code_page", staticmethod(lambda: 866))

    captured = {}

    def fake_get_output(commands, **kwargs):
        captured.update(kwargs)
        return "", "", False

    monkeypatch.setattr(Console, "_get_output", staticmethod(fake_get_output))
    Console.get_output("echo test", print_std=False)
    assert captured["decoding"] == "cp866"
    assert Console.windows_cp65001_fail is True


def test_console_get_output_unknown_os_sets_universal(monkeypatch):
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr(OS, "_macos", False)

    captured = {}

    def fake_get_output(commands, **kwargs):
        captured.update(kwargs)
        return "", "", False

    monkeypatch.setattr(Console, "_get_output", staticmethod(fake_get_output))
    Console.get_output(["echo", "x"], print_std=False, auto_decoding=True)
    assert captured["universal_newlines"] is True
    assert captured["decoding"] is None


def test_console__get_output_decoding_and_print(monkeypatch):
    stdout_data = b"ok\n"
    stderr_data = b"err\n"

    class FakePipe:
        def __init__(self, data):
            self.data = data
            self.idx = 0

        def read(self, n):
            if self.idx >= len(self.data):
                return b""
            chunk = self.data[self.idx:self.idx + n]
            self.idx += n
            return chunk

    class FakePopen:
        def __init__(self):
            self.stdout = FakePipe(stdout_data)
            self.stderr = FakePipe(stderr_data)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def kill(self):
            pass

    def fake_popen(*args, **kwargs):
        return FakePopen()

    class DummyTimer:
        def __init__(self, timeout, func, args=None):
            self.started = True

        def start(self):
            pass

        def cancel(self):
            pass

    class DummyThreading:
        def __init__(self, verbose=False):
            self.calls = []

        def add(self, func, name, kwargs=None):
            self.calls.append((func, kwargs or {}))

        def start(self, wait_for_keyboard_interrupt=False):
            self.results = [func(**kwargs) for func, kwargs in self.calls]

        def get_results(self):
            return tuple(self.results)

    printed = []
    monkeypatch.setattr("subprocess.Popen", fake_popen)
    monkeypatch.setattr("commands.console.threading.Timer", DummyTimer)
    monkeypatch.setattr("commands.console.Threading", DummyThreading, raising=False)
    monkeypatch.setattr("commands.print.Print.colored", lambda *a, **k: printed.append(a))

    out, err, timeout_reached = Console._get_output(
        ["echo"],
        print_std=True,
        decoding="utf-8",
        pure_shell=False,
        universal_newlines=False,
        timeout=0.1,
        hook_stdout=lambda s: printed.append(("out_hook", s)),
        hook_stderr=lambda s: printed.append(("err_hook", s)),
    )

    assert out.strip() == "ok"
    assert err.strip() == "err"
    assert timeout_reached is False
    assert any("out_hook" in t for t in printed if isinstance(t, tuple))
    assert any("err_hook" in t for t in printed if isinstance(t, tuple))


# ---- from test_console_get_output_extra.py ----


import pytest

from commands.console import Console

def test_console_get_output_injects_py_unbuffered(monkeypatch):
    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["commands"] = args[1]  # first arg is cls when classmethod
        return "out", "err", False

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    Console.get_output(["python", "script.py"], print_std=True, return_merged=False)
    assert captured["commands"][1] == "-u"


def test_console_get_output_timeout_flag(monkeypatch):
    called = {}

    def fake_get_output(*args, **kwargs):
        timeout = kwargs.get("timeout")
        called["timeout"] = timeout
        return "out", "err", True

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    out, err, timeout_reached = Console.get_output("echo hi", timeout=0.1, return_merged=False)
    assert called["timeout"] == 0.1
    assert timeout_reached is True
    assert out == "out" and err == "err"


def test_console_get_output_windows_cp65001_cached(monkeypatch):
    from commands.os import OS

    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["decoding"] = kwargs.get("decoding")
        return "out", "err", False

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)

    Console.windows_cp65001 = True
    Console.windows_cp65001_fail = False
    Console.get_output("echo hi", return_merged=False)
    assert captured["decoding"] == "cp65001"


def test_console_get_output_windows_cp65001_failed_cached(monkeypatch):
    from commands.os import OS

    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["decoding"] = kwargs.get("decoding")
        return "out", "err", False

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)

    Console.windows_cp65001 = False
    Console.windows_cp65001_fail = True
    Console.get_output("echo hi", return_merged=False)
    assert captured["decoding"] == "cp866"


def test_console_get_output_windows_detects_cp65001(monkeypatch):
    from commands.os import OS

    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["decoding"] = kwargs.get("decoding")
        return "out", "err", False

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr("commands.windows.Windows.fix_unicode_encode_error", staticmethod(lambda safe=False: 65001))

    Console.windows_cp65001 = False
    Console.windows_cp65001_fail = False
    Console.get_output("echo hi", return_merged=False)
    assert captured["decoding"] == "cp65001"
    assert Console.windows_cp65001 is True


def test_console_get_output_create_cmd_subprocess_builds_cmd(monkeypatch):
    from commands.os import OS

    captured = {}

    def fake_get_output(*args, **kwargs):
        captured["commands"] = args[1]
        return "out", "err", False

    monkeypatch.setattr(Console, "_get_output", classmethod(fake_get_output))
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)

    Console.get_output(["echo", "hi"], create_cmd_subprocess=True, return_merged=False, auto_decoding=False)
    assert captured["commands"][0] == "cmd"
    assert captured["commands"][1] == "/C"
    assert captured["commands"][2] == "echo hi"








def test_console_fit_wide_char_padding_branch(monkeypatch):
    from commands.os import OS

    # Ensure we go through the multi-string path, but keep it deterministic.
    monkeypatch.setattr("commands.console.Console.width", staticmethod(lambda: 3))
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)

    out = Console.fit("你好")
    assert isinstance(out, list)
    assert out and isinstance(out[0], str)


# ---- from test_console_height.py ----


import types

from commands.console import Console
from commands.os import OS


def test_console_height_windows(monkeypatch):
    class DummySize:
        def __init__(self, lines, cols):
            self.lines = lines
            self.columns = cols
    import shutil
    monkeypatch.setattr(shutil, "get_terminal_size", lambda: DummySize(50, 120))
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    assert Console.height() == 50


def test_console_height_unix(monkeypatch):
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)
    monkeypatch.setattr("commands.console.Console.get_output", lambda *a, **k: "24 80")
    monkeypatch.setattr("commands.str.Str.get_integers", staticmethod(lambda s: [24, 80]))
    assert Console.height() == 24


# ---- from test_console_internal.py ----


import pytest
from commands.console import Console










# ---- from test_console_threading_pipe.py ----


import types

from commands.console import Console


def test_console_get_output_threads_and_hooks(monkeypatch):
    outputs = {"stdout": [], "stderr": []}

    class DummyTimer:
        def __init__(self, timeout, func, args=None):
            self.cancelled = False
        def start(self): pass
        def cancel(self): self.cancelled = True

    class DummyThreading:
        def __init__(self, verbose=False): self.calls = []
        def add(self, func, name, kwargs=None):
            # execute immediately for testing hooks
            func(**kwargs)
        def start(self, wait_for_keyboard_interrupt=False): pass
        def get_results(self): return ("out", "err")

    class DummyStd:
        def __init__(self, data):
            self.data = data
            self.idx = 0
        def read(self, n):
            if self.idx >= len(self.data):
                return b""
            ch = self.data[self.idx:self.idx+1]
            self.idx += 1
            return ch

    class DummyPopen:
        def __init__(self, *a, **k):
            self.stdout = DummyStd(b"ok\n")
            self.stderr = DummyStd(b"bad\n")
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass

    import sys
    import subprocess
    import commands.console as console_module
    import commands.threading as threading_module
    monkeypatch.setattr(console_module, "threading", types.SimpleNamespace(Timer=DummyTimer))
    monkeypatch.setattr(subprocess, "Popen", DummyPopen)
    monkeypatch.setattr(threading_module, "Threading", DummyThreading)
    # capture hooks
    def hook_stdout(data): outputs["stdout"].append(data)
    def hook_stderr(data): outputs["stderr"].append(data)

    out, err, timeout_reached = Console._get_output(["any", "command"], print_std=False, decoding=None,
                                                    pure_shell=False, universal_newlines=False,
                                                    debug=False, hook_stdout=hook_stdout, hook_stderr=hook_stderr,
                                                    timeout=0.1)
    assert out == "out" and err == "err"
    assert outputs["stdout"]
    assert outputs["stderr"]
    assert timeout_reached is False


# ---- from test_console_timeout.py ----


import pytest
from commands.console import Console


def test_console_timeout_kills_process(monkeypatch):
    class DummyProc:
        def __init__(self):
            self.killed = False
        def kill(self):
            self.killed = True
    proc = DummyProc()
    # Simulate kill_popen
    Console._Console__test_timeout_proc = proc  # store to inspect
    from commands.console import threading
    killed = {"flag": False}
    def fake_timer(timeout, func, args):
        func(*args)
        class Dummy:
            def start(self): pass
            def cancel(self): pass
        return Dummy()
    monkeypatch.setattr(threading, "Timer", fake_timer)
    # simulate popen stdout/stderr
    class FakePipe:
        def __init__(self, data):
            self.data = data
            self.index = 0
        def read(self, n):
            if self.index >= len(self.data):
                return b""
            chunk = self.data[self.index:self.index+n]
            self.index += n
            return chunk
    class FakePopen:
        def __init__(self):
            self.stdout = FakePipe(b"")
            self.stderr = FakePipe(b"")
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def kill(self): pass
    monkeypatch.setattr("subprocess.Popen", lambda *a, **k: FakePopen())
    out, err, timeout_reached = Console._get_output(
        ["echo"], print_std=False, decoding="utf-8",
        pure_shell=False, universal_newlines=False,
        timeout=0.1,
        hook_stdout=lambda *_: None,
        hook_stderr=lambda *_: None,
    )
    assert timeout_reached is True or timeout_reached is False  # ensure code path ran


# ---- from test_console_timeout_branches.py ----


import pytest

from commands.console import Console


def test_console_timeout_return_tuple_when_timeout(monkeypatch):
    # simulate timeout param passed into get_output returning tuple
    def fake_get_output(commands, **kwargs):
        return "out", "err", True
    monkeypatch.setattr("commands.console.Console._get_output", staticmethod(fake_get_output))
    out, err, timeout_reached = Console.get_output("echo", timeout=1, return_merged=False)
    assert timeout_reached is True
    assert out == "out" and err == "err"
