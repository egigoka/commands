# Consolidated tests for commands/file.py (negative)

# ---- from test_file_error_paths_more.py ----


import builtins
import os

import pytest

from commands.file import File


import tempfile
from pathlib import Path
from commands.os import OS
import types
import pathlib
import datetime
from commands.path import Path
import hashlib

def test_file_create_raises_when_still_not_exists(monkeypatch, tmp_path):
    target = tmp_path / "x.txt"

    monkeypatch.setattr(File, "exist", staticmethod(lambda _p: False))
    monkeypatch.setattr("commands.dir.Dir.create", staticmethod(lambda _p: None))
    monkeypatch.setattr("os.utime", lambda *_a, **_k: None)

    # Let open succeed but file will still be reported as non-existent by our patch.
    with pytest.raises(FileNotFoundError):
        File.create(str(target), verbose=False)


def test_file_delete_raises_when_not_deleted(monkeypatch, tmp_path):
    target = tmp_path / "x.txt"
    target.write_text("x")

    monkeypatch.setattr("os.remove", lambda _p: None)
    monkeypatch.setattr(File, "exist", staticmethod(lambda _p: True))
    monkeypatch.setattr("time.sleep", lambda _s: None)

    with pytest.raises(FileExistsError):
        File.delete(str(target), no_sleep=False)


def test_file_backup_raises_when_backup_missing(monkeypatch, tmp_path):
    src = tmp_path / "x.txt"
    src.write_text("x")

    monkeypatch.setattr("os.path.isfile", lambda _p: False)
    monkeypatch.setattr("shutil.copy2", lambda *_a, **_k: None)
    monkeypatch.setattr("commands.dir.Dir.create", staticmethod(lambda _p: None))
    monkeypatch.setattr(File, "hide", staticmethod(lambda p, verbose=False: p))

    with pytest.raises(FileNotFoundError):
        File.backup(str(src), hide=True, verbose=False)



# ---- from test_file_get_encoding_invalid.py ----


import pytest

from commands.file import File




# ---- from test_file_instance_errors.py ----


import pytest

from commands.file import File


def test_file_instance_ensure_path_errors():
    f = File()
    with pytest.raises(ValueError):
        f.move("out.txt")
    with pytest.raises(ValueError):
        f.delete()
    with pytest.raises(ValueError):
        f.copy("out.txt")
    with pytest.raises(ValueError):
        f.backup()
    with pytest.raises(ValueError):
        f.hide()



# ---- from test_file_permissions_and_errors.py ----


import os
import stat
import builtins
import pytest

from commands.file import File


def test_file_delete_permission_error(monkeypatch, tmp_path):
    path = tmp_path / "locked.txt"
    path.write_text("data")
    os.chmod(path, stat.S_IRUSR)  # read-only
    def raise_perm(path_to_delete, verbose=False):
        raise PermissionError("denied")
    monkeypatch.setattr(os, "remove", raise_perm)
    with pytest.raises(PermissionError):
        File.delete(str(path), verbose=False)


def test_file_copy_handles_permission(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("hi")
    called = {}
    def raise_perm(src_path, dst_path, follow_symlinks=True):
        called["copy_attempt"] = (src_path, dst_path)
        raise PermissionError("denied")
    monkeypatch.setattr(os, "replace", raise_perm)
    monkeypatch.setattr("shutil.copy2", lambda s, d: called.setdefault("fallback", (s, d)))
    File.copy(src, dst)
    assert "fallback" in called






def test_file_read_permission_error(monkeypatch):
    def fake_open(path, mode="r", encoding=None):
        raise PermissionError("denied")
    monkeypatch.setattr(builtins, "open", fake_open)
    with pytest.raises(PermissionError):
        File.read("some.txt")


# ---- from test_file_read_by_chunk_errors.py ----


import pytest

from commands.file import File


def test_file_read_by_chunk_bad_mode(tmp_path):
    path = tmp_path / "new.bin"  # file does not exist
    gen = File.read_by_chunk(path, mode="x")  # opens in exclusive write, yields nothing
    with pytest.raises(Exception):
        next(gen)


# ---- from test_file_read_by_line_invalid_encoding.py ----


import pytest

from commands.file import File


def test_file_read_by_line_invalid_encoding(tmp_path):
    path = tmp_path / "enc.txt"
    path.write_text("hello")
    with pytest.raises(UnicodeDecodeError):
        # force invalid decode by passing bogus encoding
        list(File.read_by_line(path, encoding="utf-32-le", auto_detect_encoding=False))

@pytest.mark.parametrize(
    ("method", "args"),
    [
        ("delete", ()),
        ("move", ("out.txt",)),
        ("rename", ("out.txt",)),
        ("copy", ("out.txt",)),
        ("backup", ()),
        ("hide", ()),
    ],
)
def test_file_requires_path_before_actions(method, args):
    f = File()
    with pytest.raises(ValueError):
        getattr(f, method)(*args)

def test_file_hide_unsupported(monkeypatch, tmp_path):
    from commands.os import OS
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", False)
    path = tmp_path / "f.txt"
    path.write_text("data")
    with pytest.raises(NotImplementedError):
        File.hide(path)

def test_file_instance_delete_missing_path():
    f = File()
    with pytest.raises(ValueError):
        f.delete()

def test_file_create_invalid_verbose():
    with pytest.raises(TypeError):
        File.create("dummy.txt", verbose="yes")

def test_file_read_invalid_mode(monkeypatch):
    def fake_open(path, mode="r", encoding=None):
        raise ValueError("bad mode")
    monkeypatch.setattr("builtins.open", fake_open)
    with pytest.raises(ValueError):
        next(File.read_by_line("file", encoding="utf-8", auto_detect_encoding=False))
