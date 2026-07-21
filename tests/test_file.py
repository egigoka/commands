# Consolidated tests for commands/file.py (unit)

# ---- from test_file9.py ----


import pytest
import tempfile
import os
from commands.file import File


























# Negative tests












# Coverage improvement tests
class TestFileCoverage:
    """Tests to improve coverage for file.py"""

    def test_create_verbose_true(self, capsys):
        """Test File.create with verbose=True (lines 28, 39)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            File.create(filename, verbose=True)
            captured = capsys.readouterr()
            assert "Creating file" in captured.out
            assert "created" in captured.out

    def test_create_invalid_verbose_type(self):
        """Test File.create with invalid verbose type (line 24)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            with pytest.raises(TypeError, match="argument 'verbose' must be boolean"):
                File.create(filename, verbose="not a bool")

    def test_delete_verbose_true(self, capsys):
        """Test File.delete with verbose=True (lines 58-61)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            File.create(filename, verbose=False)
            File.delete(filename, verbose=True, no_sleep=True)
            captured = capsys.readouterr()
            assert "deleted" in captured.out

    def test_delete_nonexistent_verbose_true(self, capsys):
        """Test File.delete nonexistent with verbose=True (lines 58-59)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "nonexistent.txt")
            File.delete(filename, verbose=True, no_sleep=True)
            captured = capsys.readouterr()
            assert "not exist" in captured.out

    def test_delete_with_sleep_check(self):
        """Test File.delete with sleep and existence check (lines 62-65)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            File.create(filename, verbose=False)
            # Test with default no_sleep=False
            File.delete(filename, verbose=False, no_sleep=False)
            assert not File.exist(filename)

    def test_get_encoding(self):
        """Test File.get_encoding (lines 204-206, 208-215)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Hello, world!")
            encoding = File.get_encoding(filename)
            assert isinstance(encoding, str)
            assert encoding.lower() in ["utf-8", "ascii", "utf-16"]

    def test_get_encoding_with_count(self):
        """Test File.get_encoding with specific count"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Test content")
            encoding = File.get_encoding(filename, count_of_symbols=100)
            assert isinstance(encoding, str)

    def test_read_with_auto_detect_encoding(self):
        """Test File.read with auto_detect_encoding"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            test_content = "Test content with UTF-8"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(test_content)
            content = File.read(filename, auto_detect_encoding=True)
            assert content == test_content

    def test_read_with_specific_encoding(self):
        """Test File.read with specific encoding parameter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            test_content = "ASCII content"
            with open(filename, "w", encoding="ascii") as f:
                f.write(test_content)
            content = File.read(filename, encoding="ascii", auto_detect_encoding=False)
            assert content == test_content

    def test_backup(self):
        """Test File.backup function (lines 134-158)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            with open(filename, "w") as f:
                f.write("backup content")

            # Test backup with default parameters
            backup_path = File.backup(filename, subdirectory="bak", hide=False, verbose=False)
            assert os.path.exists(backup_path)
            assert "bak" in backup_path
            assert ".bak" in backup_path

    def test_backup_verbose_true(self, capsys):
        """Test File.backup with verbose=True"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.txt")
            with open(filename, "w") as f:
                f.write("backup content")

            backup_path = File.backup(filename, hide=False, verbose=True)
            captured = capsys.readouterr()
            assert "backup" in captured.out

    def test_hide_unix(self):
        """Test File.hide on Unix (lines 108-123)"""
        from commands.os import OS
        if OS.unix_family:
            with tempfile.TemporaryDirectory() as tmpdir:
                filename = os.path.join(tmpdir, "visible.txt")
                File.create(filename, verbose=False)
                hidden_filename = File.hide(filename, verbose=False)
                assert os.path.basename(hidden_filename).startswith(".")
        else:
            pytest.skip("Unix-only test")

    def test_hide_verbose_true(self, capsys):
        """Test File.hide with verbose=True"""
        from commands.os import OS
        if OS.unix_family:
            with tempfile.TemporaryDirectory() as tmpdir:
                filename = os.path.join(tmpdir, "visible.txt")
                File.create(filename, verbose=False)
                File.hide(filename, verbose=True)
                captured = capsys.readouterr()
                assert "hidden" in captured.out
        else:
            pytest.skip("Unix-only test")


# ---- from test_file_accessors_and_home.py ----


import pytest

from pathlib import Path

from commands.file import File
from commands.os import OS


def test_file_string_property_pathlike(tmp_path):
    f = File(tmp_path / "a.txt")
    assert f.string.endswith("a.txt")




# ---- from test_file_backup_hide_branches.py ----


import types

from commands.file import File


def test_file_hide_windows(monkeypatch, tmp_path):
    import commands.file as file_module

    fake_attrs = {}

    class DummyWin32Con:
        FILE_ATTRIBUTE_HIDDEN = "hidden"

    class DummyWin32Api:
        @staticmethod
        def SetFileAttributes(path, attr):
            fake_attrs[path] = attr

    from commands.os import OS
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)
    monkeypatch.setattr(file_module, "win32api", DummyWin32Api)
    monkeypatch.setattr(file_module, "win32con", DummyWin32Con)
    path = tmp_path / "f.txt"
    path.write_text("data")
    res = File.hide(path)
    assert fake_attrs[str(path)] == "hidden"
    assert res == str(path)








# ---- from test_file_encoding_and_format.py ----


import pytest

from commands.file import File


def test_file_read_by_line_lookup_error(tmp_path, monkeypatch):
    path = tmp_path / "data.txt"
    path.write_text("line1\nline2")

    real_open = __builtins__["open"]

    def fake_open(path_to_open, mode="r", encoding=None):
        if encoding == "EUC-TW":
            raise LookupError("bad encoding")
        return real_open(path_to_open, mode, encoding=encoding)

    monkeypatch.setattr("builtins.open", fake_open)
    gen = File.read_by_line(path, strip_newline=True, encoding="EUC-TW", auto_detect_encoding=False)
    lines = list(gen)
    # fallback branch uses alternate encoding and should still read data
    assert lines == ["line1", "line2"]


def test_file_format_size_human_readable_boundaries():
    assert File.format_size_human_readable(500) == "500b"
    assert File.format_size_human_readable(2048).split()[0].endswith("KiB")
    assert "MiB" in File.format_size_human_readable(5 * 1024 * 1024)
    assert "GiB" in File.format_size_human_readable(5 * 1024 * 1024 * 1024)


# ---- from test_file_extra.py ----


import os
import pathlib
import datetime

import pytest

from commands.file import File
from commands.path import Path






















def test_file_mime_failure_returns_unknown(monkeypatch, tmp_path):
    import sys
    import types
    from commands.os import OS
    target = tmp_path / "t.txt"
    target.write_text("data")
    class DummyMagic:
        @staticmethod
        def from_file(_path, mime=True):
            raise OSError("magic unavailable")

    monkeypatch.setattr(OS, "_windows", True, raising=False)
    monkeypatch.setitem(sys.modules, "winmagic", types.SimpleNamespace(magic=DummyMagic))
    assert File.get_mime(target) == "unknown"


# ---- from test_file_instance.py ----


import os
import tempfile
import pytest
from commands.file import File














# ---- from test_file_instance_direct_methods.py ----


from commands.file import File






# ---- from test_file_instance_more_coverage.py ----


import pytest

from commands.file import File


def test_file_string_property():
    f = File("x.txt")
    assert isinstance(f.string, str)
    assert f.string.endswith("x.txt")







# ---- from test_file_move_conflicts.py ----


import os
import pytest

from commands.file import File






# ---- from test_file_read_and_misc_fallbacks.py ----


import builtins
from pathlib import Path

import pytest

from commands.file import File


def test_read_lookuperror_falls_back_to_tis620(monkeypatch, tmp_path):
    target = tmp_path / "text.txt"
    target.write_text("ok")

    def fake_read(cls, path, encoding):
        if encoding == "EUC-TW":
            raise LookupError("unsupported encoding")
        return f"{encoding}-content"

    monkeypatch.setattr(File, "_read_with_encoding", classmethod(fake_read))

    result = File.read(target, encoding="EUC-TW", auto_detect_encoding=False)
    assert result == "TIS-620-content"


def test_read_unicode_decode_error_uses_cp1251(monkeypatch, tmp_path):
    target = tmp_path / "broken.txt"
    target.write_bytes(b"\xff\xfe\xfa")

    def raising_read(cls, path, encoding):
        raise UnicodeDecodeError(encoding, b"\xff", 0, 1, "fail")

    monkeypatch.setattr(File, "_read_with_encoding", classmethod(raising_read))
    content = File.read(target, encoding="utf-8", auto_detect_encoding=False)
    assert isinstance(content, str)
    assert content  # fallback replaced characters




def test_format_size_handles_tib_boundary():
    tib = 1 << 40
    assert "1TiB" in File.format_size_human_readable(tib)
    assert "2TiB" in File.format_size_human_readable(2 * tib)


def test_get_mime_windows_failure_skips_executable_fallback(monkeypatch, tmp_path):
    dummy = tmp_path / "file.bin"
    dummy.write_bytes(b"\x00\x01")

    class FakeMagic:
        @staticmethod
        def from_file(path, mime=True):
            raise OSError("boom")

    # Pretend Windows path to exercise winmagic import branch
    monkeypatch.setattr("commands.os.OS", type("StubOS", (), {"windows": True}))

    import sys
    winmagic_module = type("winmagic", (), {"magic": FakeMagic})
    monkeypatch.setitem(sys.modules, "winmagic", winmagic_module)

    captured = {"called": False}

    def fake_get_output(*args, **kwargs):
        captured["called"] = True
        raise AssertionError("executable fallback must not run")

    monkeypatch.setattr("commands.console.Console.get_output", staticmethod(fake_get_output))
    result = File.get_mime(dummy)
    assert not captured["called"]
    assert result == "unknown"


# ---- from test_file_read_by_line_auto_detect.py ----


import pytest

from commands.file import File




# ---- from test_file_sha256_checksum.py ----


import hashlib

from commands.file import File




# ---- from test_file_size_and_existence.py ----


import pytest

from commands.file import File






# ---- from test_file_wipe_and_truncate.py ----


import os
import pytest

from commands.file import File
