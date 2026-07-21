# Consolidated tests for commands/keyboard.py (unit)

# ---- from test_keyboard9.py ----


import pytest


def require_pyautogui():
    try:
        return pytest.importorskip("pyautogui")
    except Exception as exc:  # pragma: no cover - environment dependent
        pytest.skip(f"pyautogui unavailable: {exc}")


def test_keyboard9_import():
    from commands import Keyboard
    assert Keyboard is not None


# Coverage improvement tests
class TestKeyboardCoverage:
    """Tests to improve coverage for keyboard9.py"""

    def test_hotkey_with_verbose(self, monkeypatch, capsys):
        """Test Keyboard.hotkey with verbose=True (lines 13-14)"""
        # Skip if pyautogui is not available
        pyautogui = require_pyautogui()

        from commands.keyboard import Keyboard

        # Mock pyautogui.hotkey to avoid actual keyboard input
        def mock_hotkey(*args, **kwargs):
            return None

        monkeypatch.setattr(pyautogui, "hotkey", mock_hotkey)

        Keyboard.hotkey("ctrl", "c", verbose=True)
        captured = capsys.readouterr()
        assert "Keyboard.hotkey" in captured.out
        assert "args=" in captured.out

    def test_hotkey_without_verbose(self, monkeypatch):
        """Test Keyboard.hotkey with verbose=False"""
        pyautogui = require_pyautogui()

        from commands.keyboard import Keyboard

        # Mock pyautogui.hotkey
        called = []
        def mock_hotkey(*args, **kwargs):
            called.append((args, kwargs))
            return None

        import pyautogui
        monkeypatch.setattr(pyautogui, "hotkey", mock_hotkey)

        Keyboard.hotkey("ctrl", "v", verbose=False)
        assert len(called) == 1
        assert "ctrl" in called[0][0]

    def test_translate_cyrillic_to_qwerty(self):
        """Test Keyboard.translate for Cyrillic characters"""
        from commands.keyboard import Keyboard

        # Test basic Cyrillic characters
        assert Keyboard.translate("й") == "q"
        assert Keyboard.translate("ц") == "w"
        assert Keyboard.translate("у") == "e"
        assert Keyboard.translate("к") == "r"
        assert Keyboard.translate("е") == "t"

    def test_translate_special_characters(self):
        """Test Keyboard.translate for special Cyrillic characters"""
        from commands.keyboard import Keyboard

        # Test special characters
        assert Keyboard.translate("\"") == "@"
        assert Keyboard.translate("№") == "#"
        assert Keyboard.translate(";") == "$"

    def test_translate_uppercase_cyrillic(self):
        """Test Keyboard.translate for uppercase Cyrillic"""
        from commands.keyboard import Keyboard

        assert Keyboard.translate("Й") == "Q"
        assert Keyboard.translate("Ц") == "W"
        assert Keyboard.translate("У") == "E"

    def test_keyboard_instance_helpers(self, monkeypatch, capsys):
        pyautogui = require_pyautogui()
        from commands.keyboard import Keyboard

        called = []
        monkeypatch.setattr(pyautogui, "hotkey", lambda *a, **k: called.append((a, k)))
        monkeypatch.setattr(pyautogui, "write", lambda *a, **k: called.append((a, k)))

        k = Keyboard()
        k.hotkey_do("ctrl", "c", verbose=True)
        k.type("abc", verbose=True)
        captured = capsys.readouterr()
        assert called
        assert "Keyboard.hotkey" in captured.out

    def test_translate_unmapped_characters(self):
        """Test Keyboard.translate returns unmapped characters as-is"""
        from commands.keyboard import Keyboard

        # ASCII characters should pass through unchanged
        assert Keyboard.translate("a") == "a"
        assert Keyboard.translate("1") == "1"
        assert Keyboard.translate(" ") == " "

    def test_translate_string_basic(self):
        """Test Keyboard.translate_string function"""
        from commands.keyboard import Keyboard

        # Test translating a string
        result = Keyboard.translate_string("йцукен")
        assert result == "qwerty"

    def test_translate_string_mixed(self):
        """Test Keyboard.translate_string with mixed characters"""
        from commands.keyboard import Keyboard

        result = Keyboard.translate_string("привет123")
        # Should translate Cyrillic but leave numbers unchanged
        assert "123" in result
        assert len(result) == 9

    def test_translate_string_empty(self):
        """Test Keyboard.translate_string with empty string"""
        from commands.keyboard import Keyboard

        result = Keyboard.translate_string("")
        assert result == ""

    def test_write_with_verbose(self, monkeypatch, capsys):
        """Test Keyboard.write with verbose=True (lines 42-43)"""
        pyautogui = require_pyautogui()

        from commands.keyboard import Keyboard

        # Mock pyautogui.write
        def mock_write(text):
            return None

        import pyautogui
        monkeypatch.setattr(pyautogui, "write", mock_write)

        Keyboard.write("тест", verbose=True)
        captured = capsys.readouterr()
        assert "Keyboard.write" in captured.out
        assert "тест" in captured.out
        assert "pyautogui.write" in captured.out

    def test_write_without_verbose(self, monkeypatch):
        """Test Keyboard.write with verbose=False"""
        pyautogui = require_pyautogui()

        from commands.keyboard import Keyboard

        # Mock pyautogui.write
        written = []
        def mock_write(text):
            written.append(text)
            return None

        import pyautogui
        monkeypatch.setattr(pyautogui, "write", mock_write)

        Keyboard.write("hello", verbose=False)
        assert len(written) == 1
        assert "hello" in written[0]


# ---- from test_keyboard_extra.py ----


import sys

from commands.keyboard import Keyboard


def test_keyboard_translate_mapping():
    # Russian letters should map to qwerty symbols
    assert Keyboard.translate("й") == "q"
    assert Keyboard.translate("!") == "!"
    assert Keyboard.translate("A") == "A"


def test_keyboard_translate_string():
    assert Keyboard.translate_string("йцу") == "qwe"


def test_keyboard_write_and_hotkey(monkeypatch):
    calls = []

    class DummyPyAutoGui:
        @staticmethod
        def write(value):
            calls.append(("write", value))

        @staticmethod
        def hotkey(*args, **kwargs):
            calls.append(("hotkey", args, kwargs))
            return "ran"

    monkeypatch.setitem(sys.modules, "pyautogui", DummyPyAutoGui)
    Keyboard.write("йц")
    assert calls[0] == ("write", "qw")

    res = Keyboard.hotkey("ctrl", "c")
    assert res == "ran"
    assert calls[-1][0] == "hotkey"


def test_keyboard_instance_helpers(monkeypatch):
    calls = []

    class DummyPyAutoGui:
        @staticmethod
        def write(value):
            calls.append(("write", value))

        @staticmethod
        def hotkey(*args, **kwargs):
            calls.append(("hotkey", args, kwargs))
            return "ok"

    monkeypatch.setitem(sys.modules, "pyautogui", DummyPyAutoGui)

    kb = Keyboard()
    kb.type("й")
    kb.hotkey_do("alt", "tab")
    assert calls == [("write", "q"), ("hotkey", ("alt", "tab"), {})]


# ---- from test_keyboard_verbose.py ----


import sys
import types

from commands.keyboard import Keyboard


def test_keyboard_hotkey_verbose_prints(monkeypatch, capsys):
    calls = []

    def fake_hotkey(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setitem(sys.modules, "pyautogui", types.SimpleNamespace(hotkey=fake_hotkey, write=lambda *_a, **_k: None))

    Keyboard.hotkey("ctrl", "c", verbose=True)
    out = capsys.readouterr().out
    assert "Keyboard.hotkey" in out
    assert calls


def test_keyboard_write_verbose_prints(monkeypatch, capsys):
    calls = []

    def fake_write(text):
        calls.append(text)

    monkeypatch.setitem(sys.modules, "pyautogui", types.SimpleNamespace(hotkey=lambda *_a, **_k: None, write=fake_write))

    Keyboard.write("abc", verbose=True)
    out = capsys.readouterr().out
    assert "Keyboard.write" in out
    assert calls
