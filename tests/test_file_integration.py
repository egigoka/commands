# Consolidated tests for commands/file.py (integration)

# ---- from test_file_integration.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.file import File
from pathlib import Path as LibPath
from commands.os import OS
import types
import pathlib
import datetime
import builtins
import hashlib

def test_file_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        File.create(filename, verbose=False)
        assert os.path.exists(filename)

def test_file_create_with_subdirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "subdir", "test.txt")
        File.create(filename, verbose=False)
        assert os.path.exists(filename)

def test_file_delete():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        File.create(filename, verbose=False)
        File.delete(filename, verbose=False, no_sleep=True)
        assert not os.path.exists(filename)

def test_file_copy():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        File.create(src, verbose=False)
        with open(src, "w") as f:
            f.write("content")
        File.copy(src, dst)
        assert os.path.exists(dst)
        with open(dst, "r") as f:
            assert f.read() == "content"

def test_file_move():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        File.create(src, verbose=False)
        File.move(src, dst)
        assert not os.path.exists(src)
        assert os.path.exists(dst)

def test_file_rename():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "old.txt")
        dst = os.path.join(tmpdir, "new.txt")
        File.create(src, verbose=False)
        File.rename(src, dst)
        assert not os.path.exists(src)
        assert os.path.exists(dst)

def test_file_wipe():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        with open(filename, "w") as f:
            f.write("content to be wiped")
        File.wipe(filename)
        with open(filename, "r") as f:
            assert f.read() == ""

def test_file_exist():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        assert not File.exist(filename)
        File.create(filename, verbose=False)
        assert File.exist(filename)

def test_file_read():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("test content")
        content = File.read(filename)
        assert content == "test content"

def test_file_write():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        File.write(filename, "test data")
        with open(filename, "r", encoding="utf-8") as f:
            assert f.read() == "test data"

def test_file_read_by_chunk_and_line():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.txt")
        content = "line1\nline2\nline3"
        File.write(filename, content, mode="w", verbose=False)

        chunks = list(File.read_by_chunk(filename, chunk_size=5, mode="r"))
        assert "".join(chunks) == content

        lines = list(File.read_by_line(filename))
        assert lines == ["line1", "line2", "line3"]

        lines_with_newline = list(File.read_by_line(filename, strip_newline=False))
        assert lines_with_newline == ["line1\n", "line2\n", "line3"]

def test_file_instance_shortcuts(tmp_path):
    file_path = tmp_path / "a.txt"
    File.write(file_path, "data", mode="w")

    f = File(file_path)
    moved_path = f.move(tmp_path / "b.txt")
    assert moved_path == str(tmp_path / "b.txt")
    assert os.path.exists(moved_path)

def test_file_move_and_rename_update_instance_path(tmp_path):
    original = tmp_path / "original.txt"
    original.write_text("content")

    f = File(original)
    moved = tmp_path / "moved.txt"
    assert f.move(moved) == str(moved)
    assert f.string == str(moved)

    renamed = tmp_path / "renamed.txt"
    assert f.rename(renamed) == str(renamed)
    assert f.string == str(renamed)

def test_file_copy_and_delete_via_instance(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("payload")
    f = File(source)

    copy_path = tmp_path / "copy.txt"
    f.copy(copy_path)
    assert copy_path.read_text() == "payload"

    f.delete(no_sleep=True)
    assert not source.exists()

def test_file_backup_and_hide_instance_wrappers(tmp_path):
    import os
    target = tmp_path / "data.txt"
    target.write_text("data")
    f = File(target)

    backup_path = f.backup(subdirectory="bak", hide=False)
    assert LibPath(backup_path).exists()

    hidden_path = f.hide()
    assert LibPath(hidden_path).exists()
    if OS.windows:
        assert hidden_path.endswith("data.txt")
        assert target.exists()
        assert os.stat(hidden_path).st_file_attributes & 0x02  # FILE_ATTRIBUTE_HIDDEN
    else:
        assert hidden_path.endswith(".data.txt")
        assert not target.exists()

def test_file_backup_empty_subdir(monkeypatch, tmp_path):
    import os
    called = {}
    monkeypatch.setattr("commands.path.Path.full", staticmethod(lambda p: str(p)))
    monkeypatch.setattr("commands.dir.Dir.create", lambda p: (called.setdefault("dir", p), os.makedirs(p, exist_ok=True)))
    monkeypatch.setattr("commands.time.Time.dotted", staticmethod(lambda: "stamp"))
    def fake_hide(p, verbose=False):
        open(p + ".hidden", "w").write("hidden")
        return p + ".hidden"
    monkeypatch.setattr("commands.file.File.hide", staticmethod(fake_hide))
    monkeypatch.setattr("shutil.copy2", lambda src, dst: (os.makedirs(os.path.dirname(dst), exist_ok=True),
                                                         open(dst, "w").write("x")))
    path = tmp_path / "file.txt"
    path.write_text("data")
    out = File.backup(path, subdirectory="", hide=True, verbose=True)
    assert "bak" in out
    assert out.endswith(".hidden")

def test_file_backup_hide_false(monkeypatch, tmp_path):
    import os
    called = {}
    monkeypatch.setattr("commands.path.Path.full", staticmethod(lambda p: str(p)))
    monkeypatch.setattr("commands.dir.Dir.create", lambda p: (called.setdefault("dir", p), os.makedirs(p, exist_ok=True)))
    monkeypatch.setattr("commands.time.Time.dotted", staticmethod(lambda: "stamp"))
    monkeypatch.setattr("shutil.copy2", lambda src, dst: (os.makedirs(os.path.dirname(dst), exist_ok=True),
                                                         open(dst, "w").write("x"),
                                                         called.setdefault("copied", (src, dst))))
    path = tmp_path / "file.txt"
    path.write_text("data")
    out = File.backup(path, subdirectory="sub", hide=False, verbose=False)
    assert "sub" in out
    assert called["copied"][0] == str(path)
    assert "stamp" in called["copied"][1]

def test_file_instance_wrappers(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hi")
    inst = File(f)
    # move updates path
    new_path = inst.move(tmp_path / "b.txt")
    assert inst.path == str(tmp_path / "b.txt")
    # copy leaves original
    inst.copy(tmp_path / "c.txt")
    assert (tmp_path / "c.txt").exists()
    # hide renames (unix path)
    hidden = inst.hide()
    assert hidden.endswith(".b.txt") or hidden.startswith(str(tmp_path))

def test_file_create_and_exists(tmp_path):
    target = tmp_path / "nested" / "file.txt"
    File.create(target, verbose=False)
    assert File.exist(target)
    with pytest.raises(FileExistsError):
        File.create(target)
    with pytest.raises(TypeError):
        File.create(target, verbose="yes")

def test_file_backup_and_set_mod_time(tmp_path, monkeypatch):
    target = tmp_path / "t.txt"
    target.write_text("data")
    monkeypatch.setattr("commands.time.Time.dotted", lambda: "stamp")
    backup = File.backup(target, subdirectory="bak", hide=False, verbose=False)
    assert pathlib.Path(backup).exists()
    # set modification time
    dt = datetime.datetime(2020, 1, 1, 0, 0)
    File.set_modification_time(backup, dt)
    assert abs(File.get_modification_time(backup) - dt.timestamp()) < 2

def test_file_get_encoding_and_read_write(tmp_path):
    target = tmp_path / "t.txt"
    File.write(target, "hello", mode="w", encoding="utf-8")
    assert File.read(target) == "hello"
    # ascii detection is fine for simple text
    assert File.get_encoding(target, count_of_symbols=10).lower() in {"utf-8", "ascii"}

def test_file_format_size_and_size(tmp_path):
    target = tmp_path / "t.bin"
    target.write_bytes(b"\x00" * 2048)
    human = File.get_size(target, human_readable=True)
    assert "KiB" in human

def test_file_get_extension_and_checksum(tmp_path):
    target = tmp_path / "t.txt"
    target.write_text("abc")
    assert File.get_extension(target) == ".txt"
    assert len(File.sha256_checksum(target)) == 64

def test_file_write_binary_and_text_paths(tmp_path):
    binary_path = tmp_path / "bin.dat"
    File.write(binary_path, "text", mode="wb", encoding="utf-8")
    assert binary_path.read_bytes() == b"text"

    binary_path2 = tmp_path / "bin2.dat"
    File.write(binary_path2, bytearray(b"ab"), mode="wb", encoding="utf-8")
    assert binary_path2.read_bytes() == b"ab"

    binary_path3 = tmp_path / "bin3.dat"
    File.write(binary_path3, 123, mode="wb", encoding="utf-8")
    assert binary_path3.read_bytes() == b"123"

    text_path1 = tmp_path / "text1.txt"
    File.write(text_path1, b"hello", mode="w", encoding="utf-8")
    assert text_path1.read_text(encoding="utf-8") == "hello"

    text_path2 = tmp_path / "text2.txt"
    File.write(text_path2, bytearray(b"yo"), mode="w", encoding="utf-8")
    assert text_path2.read_text(encoding="utf-8") == "yo"

def test_file_instance_move_and_rename():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "a.txt")
        dst = os.path.join(tmpdir, "b.txt")
        open(src, "w").close()
        f = File(src)
        f.rename(dst)
        assert f.path == dst

def test_file_hide_unix(monkeypatch, tmp_path):
    from commands.os import OS
    monkeypatch.setattr(OS, "_windows", False)
    monkeypatch.setattr(OS, "_unix_family", True)
    fname = tmp_path / "visible.txt"
    fname.write_text("data")
    hidden = File.hide(str(fname), verbose=False)
    assert hidden.endswith(".visible.txt")
    assert not fname.exists()

def test_read_binary_mode_and_write_int(tmp_path):
    target = tmp_path / "numbers.bin"
    File.write(target, 123, mode="a")
    assert target.read_text() == "123"

    content = File.read(target, mode="rb")
    assert b"123" in content

    chunks = list(File.read_by_chunk(target, chunk_size=2, mode="rb"))
    assert b"12" in chunks[0]

def test_read_by_line_fallback_strip_control(monkeypatch, tmp_path):
    target = tmp_path / "fallback.txt"
    target.write_text("line1\nline2\n")

    monkeypatch.setattr(File, "get_encoding", classmethod(lambda cls, path, count_of_symbols=True: "EUC-TW"))

    lines = list(File.read_by_line(target, strip_newline=False))
    assert lines == ["line1\n", "line2\n"]

def test_file_instance_move_updates_path(monkeypatch, tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x")
    dest = tmp_path / "b.txt"

    # Use real filesystem ops but under tmp_path.
    f = File(str(src))
    new_path = f.move(str(dest))
    assert new_path.endswith("b.txt")
    assert f.path.endswith("b.txt")
    assert dest.exists()
    assert not src.exists()

def test_file_copy_symlink(monkeypatch, tmp_path):
    # ensure copy deals with IsADirectoryError path
    src = tmp_path / "src.txt"
    src.write_text("data")
    dst = tmp_path / "dst.txt"
    monkeypatch.setattr("shutil.copy2", lambda s, d: (_ for _ in ()).throw(IsADirectoryError("dir")))
    with pytest.raises(IsADirectoryError):
        File.copy(src, dst)

def test_write_verbose_and_binary_mode(tmp_path, capsys):
    target = tmp_path / "data.bin"
    File.write(target, b"abc", mode="wb", verbose=True)
    out = capsys.readouterr().out
    assert "Writing to file" in out
    assert "Written to file" in out
    assert target.read_bytes() == b"abc"

def test_file_read_by_line_auto_detect_false(monkeypatch, tmp_path):
    p = tmp_path / "data.txt"
    p.write_text("abc")
    # When auto_detect_encoding=False, provided encoding is used directly
    lines = list(File.read_by_line(p, encoding="utf-8", auto_detect_encoding=False))
    assert lines == ["abc"]

def test_file_sha256_checksum(tmp_path):
    path = tmp_path / "data.bin"
    data = b"abc123"
    path.write_bytes(data)
    expected = hashlib.sha256(data).hexdigest()
    assert File.sha256_checksum(path) == expected

def test_file_exist_and_format_size(tmp_path):
    path = tmp_path / "small.bin"
    path.write_bytes(b"\x00" * 600)
    assert File.exist(path)
    human = File.get_size(str(path), human_readable=True)
    assert isinstance(human, str) and human

def test_file_wipe_truncates(tmp_path):
    path = tmp_path / "wipe.txt"
    path.write_text("data")
    File.wipe(path)
    assert path.read_text() == ""
