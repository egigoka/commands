# Consolidated tests for commands/file.py (integration_negative)

# ---- from test_file_integration_negative.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.file import File
from pathlib import Path
from commands.os import OS
import types
import pathlib
import datetime
from commands.path import Path
import builtins
import hashlib
import stat

def test_file_create_raises_on_existing():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        File.create(filename, verbose=False)
        with pytest.raises(FileExistsError):
            File.create(filename, verbose=False)

def test_file_move_nonexistent():
    """Should raise FileNotFoundError when source doesn't exist"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "nonexistent.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        with pytest.raises(FileNotFoundError):
            File.move(src, dst)

def test_file_copy_nonexistent():
    """Should raise FileNotFoundError when source doesn't exist"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "nonexistent.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        with pytest.raises(FileNotFoundError):
            File.copy(src, dst)

def test_file_read_nonexistent():
    """Should raise FileNotFoundError when file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        File.read("/nonexistent/file.txt")

def test_file_wipe_nonexistent():
    """Should raise FileNotFoundError when file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        File.wipe("/nonexistent/file.txt")

def test_file_delete_directory_guard(tmp_path):
    d = tmp_path / "dir"
    d.mkdir()
    with pytest.raises(IsADirectoryError):
        File.delete(str(d))

def test_file_move_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        File.move(tmp_path / "missing.txt", tmp_path / "out.txt")

def test_file_create_existing(tmp_path):
    fname = tmp_path / "file.txt"
    fname.write_text("x")
    with pytest.raises(FileExistsError):
        File.create(str(fname))

def test_file_delete_directory(tmp_path):
    dirpath = tmp_path / "adir"
    dirpath.mkdir()
    with pytest.raises(IsADirectoryError):
        File.delete(str(dirpath))

def test_file_delete_directory_raises(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    with pytest.raises(IsADirectoryError):
        File.delete(str(d))

def test_file_move_conflict(monkeypatch, tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("data")
    dst.write_text("other")
    def fake_move(s, d):
        raise FileExistsError("exists")

    monkeypatch.setattr("shutil.move", fake_move)
    with pytest.raises(FileExistsError):
        File.move(str(src), str(dst))

def test_file_size_missing_raises():
    with pytest.raises(FileNotFoundError):
        File.get_size("nope.txt")

def test_file_get_encoding_invalid_path(monkeypatch):
    class DummyBytes:
        @staticmethod
        def read(path, count=None):
            raise FileNotFoundError("missing")
    monkeypatch.setattr("commands.bytes.Bytes", DummyBytes)
    with pytest.raises(FileNotFoundError):
        File.get_encoding("missing.txt", count_of_symbols=True)

def test_file_size_errors(monkeypatch):
    with pytest.raises(FileNotFoundError):
        File.get_size("no_such_file.txt")
