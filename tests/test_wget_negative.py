# Consolidated tests for commands/wget.py (negative)

# ---- from test_wget_error_paths.py ----


import pytest

from commands.wget import Wget


def test_wget_download_raises_on_missing_wget(monkeypatch):
    def fake_console(*a, **k):
        raise FileNotFoundError("missing")
    monkeypatch.setattr("commands.console.Console.get_output", fake_console)
    with pytest.raises(OSError):
        Wget.download("http://example.com/file.txt", "out.txt", wget_path="custom_wget")

def test_wget_callable_requires_url():
    w = Wget()
    with pytest.raises(ValueError):
        w()

def test_wget_fetch_requires_output():
    w = Wget(url="http://example.com")
    with pytest.raises(ValueError):
        w.fetch()

def test_wget_instance_requires_url_output():
    w = Wget()
    with pytest.raises(ValueError):
        w.fetch("out")
    w.url = "http://example.com"
    with pytest.raises(ValueError):
        w.fetch()

def test_wget_download_custom_path_error(monkeypatch, tmp_path):
    def fake_console(commands, **kwargs):
        raise FileNotFoundError("missing custom")

    monkeypatch.setattr("commands.console.Console.get_output", fake_console)
    monkeypatch.setattr("commands.dir.Dir.exist", staticmethod(lambda p: True))
    with pytest.raises(OSError):
        Wget.download("http://example.com/file", tmp_path / "out.txt", wget_path="custom_bin")
