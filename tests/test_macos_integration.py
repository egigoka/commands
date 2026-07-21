# Consolidated tests for commands/macos.py (integration)

# ---- from test_macos_integration.py ----

# Placeholder for future tests.
import os
import sys
import types
import tempfile
from commands import Dir, File, OS, Path
import pytest
from commands.macos import macOS

@pytest.mark.skipif(OS.windows, reason="Test exercises Unix symlink metadata handling")
def test_dir_copy_symlink_lchmod_failure(monkeypatch, tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "target.txt").write_text("data", encoding="utf-8")
    os.symlink(src / "target.txt", src / "link.txt")

    def raise_lchmod(*_args, **_kwargs):
        raise OSError("no lchmod")

    monkeypatch.setattr(os, "lchmod", raise_lchmod, raising=False)

    Dir.copy(str(src), str(dst), symlinks=True)
    assert (dst / "link.txt").is_symlink()

def test_file_get_mime_non_windows(monkeypatch, tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("hello", encoding="utf-8")

    monkeypatch.setattr(OS, "_windows", False, raising=False)
    fake_magic = types.SimpleNamespace(from_file=lambda _path, mime=True: "text/plain")
    monkeypatch.setitem(sys.modules, "magic", fake_magic)

    assert File.get_mime(sample) == "text/plain"
