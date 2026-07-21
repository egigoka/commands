# Consolidated tests for commands/wget.py (unit)

# ---- from test_wget9.py ----


import pytest
from commands.wget import Wget


def test_wget_import():
    from commands import Wget as W
    assert W is not None




def test_wget_callable_sets_url(monkeypatch):
    from commands.console import Console
    called = {}
    monkeypatch.setattr(Console, "get_output", lambda *a, **k: called.update({"args": a, "kwargs": k}) or "")

    w = Wget(url="http://example.com", output_filename="out")
    w()
    assert "wget" in called["args"][0][0] or called["args"][0][0] == "wget"




# ---- from test_wget_extra.py ----


import pytest

from commands.wget import Wget




def test_wget_download_creates_dir_and_handles_missing(monkeypatch, tmp_path):
    cmds = {}

    class DummyConsole:
        @staticmethod
        def get_output(commands, **kwargs):
            cmds["commands"] = commands
            return "ok"

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    monkeypatch.setattr("commands.dir.Dir.exist", staticmethod(lambda p: False))
    monkeypatch.setattr("commands.dir.Dir.create", lambda p: cmds.setdefault("created", p))

    out = Wget.download("http://example.com/file.txt", tmp_path / "out" / "file.txt", verbose=False)
    assert "wget" in cmds["commands"][0]
    assert "created" in cmds and "out" in str(cmds["created"])
    assert out == "ok"


def test_wget_download_missing_executable(monkeypatch, tmp_path):
    attempts = []

    def fake_console(commands, **kwargs):
        attempts.append(commands[0])
        raise FileNotFoundError("no wget")

    monkeypatch.setattr("commands.console.Console.get_output", fake_console)
    monkeypatch.setattr("commands.dir.Dir.exist", staticmethod(lambda p: True))

    with pytest.raises(OSError, match="wget executable not found"):
        Wget.download("http://example.com/a", tmp_path / "a.txt")

    assert attempts == ["wget"]


def test_wget_instance_call_merges_defaults(monkeypatch):
    captured = {}
    monkeypatch.setattr("commands.wget.Wget.fetch", lambda self, **kwargs: captured.update(kwargs) or "done")
    w = Wget(url="http://example.com", output_filename="out.txt")
    result = w(verbose=True, timeout=5)
    assert result == "done"
    assert captured["verbose"] is True
    assert captured["timeout"] == 5


def test_wget_download_no_check_certificate(monkeypatch, tmp_path):
    captured = {}

    class DummyConsole:
        @staticmethod
        def get_output(commands, **kwargs):
            captured["commands"] = commands
            return "done"

    monkeypatch.setattr("commands.console.Console", DummyConsole)
    monkeypatch.setattr("commands.dir.Dir.exist", staticmethod(lambda p: True))
    out = Wget.download("http://example.com/file", tmp_path / "out.txt", no_check_certificate=True, verbose=True)
    assert out == "done"
    # Should insert switch near start and still keep trailing one
    assert captured["commands"].count("--no-check-certificate") == 2




def test_wget_instance_sets_attrs_and_calls(monkeypatch):
    captured = {}

    def fake_download(self, url, output_filename, **kwargs):
        captured["url"] = url
        captured["out"] = output_filename
        captured["kwargs"] = kwargs
        return "ok"

    monkeypatch.setattr("commands.wget.Wget.download", classmethod(fake_download))
    w = Wget()
    result = w(url="http://example.com/new", output_filename="out.bin", timeout=1)
    assert result == "ok"
    assert captured["url"] == "http://example.com/new"
    assert captured["out"] == "out.bin"
