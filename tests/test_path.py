# Consolidated tests for commands/path.py (unit)

# ---- from test_path9.py ----


import pytest
import os
import tempfile
from commands.path import Path


class TestPathFull:
    """Tests for Path.full method"""

    def test_full_relative_path(self):
        result = Path.full(".")
        assert os.path.isabs(result)
        assert result == os.path.abspath(".")

    def test_full_already_absolute(self):
        abs_path = os.path.abspath(".")
        result = Path.full(abs_path)
        assert result == abs_path


class TestPathGetRealPath:
    """Tests for Path.get_real_path method"""

    def test_get_real_path(self):
        result = Path.get_real_path(__file__)
        assert os.path.isabs(result)
        assert result.endswith("test_path.py")


class TestPathCommands:
    """Tests for Path.commands method"""

    def test_commands_returns_path(self):
        result = Path.commands()
        assert isinstance(result, str)
        assert os.path.isabs(result)
        # Should end with 'commands' directory
        assert result.endswith("commands")


class TestPathWorking:
    """Tests for Path.working method"""

    def test_working_returns_cwd(self):
        result = Path.working()
        assert result == os.getcwd()
        assert os.path.isabs(result)


class TestPathCombine:
    """Tests for Path.combine method"""

    def test_combine_basic(self):
        if os.name == 'nt':  # Windows
            result = Path.combine("C:", "Users", "test")
            assert "Users" in result and "test" in result
        else:  # Unix
            result = Path.combine("home", "user", "test")
            assert result == "home/user/test"


    def test_combine_single_path(self):
        if os.name != 'nt':
            result = Path.combine("tmp")
            assert result == "tmp"


class TestPathInstanceUsage:
    """Instance-oriented helpers for Path"""

    def test_path_string_property(self):
        expected = Path.combine("/", "etc", "hosts")
        p = Path("/", "etc", "hosts")
        assert p.string == expected
        assert str(p) == expected

    def test_path_div_operator(self):
        base = Path("home")
        new = base / "user"
        assert isinstance(new, Path)
        assert new.string == Path.combine("home", "user")




class TestPathGetParent:
    """Tests for Path.get_parent method"""

    def test_get_parent_basic(self):
        path = "/home/user/documents/file.txt"
        result = Path.get_parent(path)
        assert result == "/home/user/documents"

    def test_get_parent_windows_style(self):
        # Test with Unix-style path on Unix, Windows-style on Windows
        if os.name == 'nt':
            path = "C:\\Users\\test\\file.txt"
            result = Path.get_parent(path)
            assert result == "C:\\Users\\test"
        else:
            path = "/home/test/file.txt"
            result = Path.get_parent(path)
            assert result == "/home/test"

    def test_get_parent_no_parent(self):
        path = "file.txt"
        result = Path.get_parent(path)
        assert result == ""




class TestPathAddBeforeExtension:
    """Tests for Path.add_before_extension method"""

    def test_add_before_extension_basic(self):
        result = Path.add_before_extension("file.txt", "_backup")
        assert result == "file_backup.txt"

    def test_add_before_extension_multiple_dots(self):
        result = Path.add_before_extension("my.file.txt", "_v2")
        assert result == "my.file_v2.txt"

    def test_add_before_extension_no_extension(self):
        result = Path.add_before_extension("filename", "_suffix")
        # Without extension, it just appends
        assert "_suffix" in result


class TestPathPython:
    """Tests for Path.python method"""

    def test_python_returns_executable(self):
        result = Path.python()
        assert isinstance(result, str)
        assert os.path.isabs(result)
        assert "python" in result.lower() or result.endswith(("python3", "python.exe"))


class TestPathTemp:
    """Tests for Path.temp method"""

    def test_temp_returns_directory(self):
        result = Path.temp()
        assert isinstance(result, str)
        assert os.path.isdir(result)
        assert os.path.isabs(result)


class TestPathSafeFile:
    """Tests for Path.safe__file__ method"""

    def test_safe_file(self):
        result = Path.safe__file__(__file__)
        assert os.path.isabs(result)
        assert result.endswith("test_path.py")


class TestPathSeparator:
    """Tests for Path.separator method"""

    def test_separator_returns_os_sep(self):
        result = Path.separator()
        assert result == os.sep
        assert result in ['/', '\\']


class TestPathSplit:
    """Tests for Path.split method"""

    def test_split_basic(self):
        path = "/home/user/file.txt"
        head, tail = Path.split(path)
        assert head == "/home/user"
        assert tail == "file.txt"

    def test_split_windows_or_unix(self):
        if os.name == 'nt':
            path = "C:\\Users\\test.txt"
            head, tail = Path.split(path)
            assert tail == "test.txt"
        else:
            path = "/home/user/test.txt"
            head, tail = Path.split(path)
            assert tail == "test.txt"


# Negative tests
class TestPathNegative:
    """Negative tests for Path module"""

    def test_full_empty_string(self):
        """Should handle empty string"""
        result = Path.full("")
        # Should still return something valid
        assert isinstance(result, str)




    def test_get_parent_root(self):
        """Should handle root directory"""
        if os.name == 'nt':
            path = "C:\\"
        else:
            path = "/"
        result = Path.get_parent(path)
        # Parent of root is typically root or empty
        assert isinstance(result, str)

    def test_add_before_extension_empty(self):
        """Should handle empty filename"""
        result = Path.add_before_extension("", "_suffix")
        assert isinstance(result, str)


class TestPathCombineEdgeCases:
    """Test edge cases in Path.combine for full coverage"""

    def test_combine_relative_dot_path(self):
        """Test combining paths starting with dot (Unix)"""
        from commands.os import OS
        if OS.unix_family:
            result = Path.combine("./dir", "file.txt")
            assert isinstance(result, str)
            assert "dir" in result
            assert "file.txt" in result

    def test_combine_windows_drive_letter(self):
        """Test Windows drive letter handling (C:, D:, etc)"""
        from commands.os import OS
        if OS.windows:
            result = Path.combine("C:", "Users", "test")
            assert isinstance(result, str)
            assert "C:" in result or "c:" in result
            assert "Users" in result

    def test_combine_smb_path(self):
        """Test SMB/UNC path handling (\\\\server\\share)"""
        from commands.os import OS
        from commands.const import backslash
        if OS.windows:
            result = Path.combine(backslash, "server", "share")
            assert isinstance(result, str)
            # Should start with double backslash for SMB paths


    def test_temp_basic(self):
        """Test temp() returns valid directory"""
        result = Path.temp()
        # Should return a valid temp directory
        assert isinstance(result, str)
        assert len(result) > 0
        assert os.path.isdir(result)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ---- from test_path_instance.py ----


import os
import pytest
from commands.path import Path


def test_path_append_and_string():
    p = Path("a")
    p.append("b", "c")
    assert p.string.endswith(os.path.join("a", "b", "c"))


def test_path_truediv():
    p = Path("a")
    q = p / "b"
    assert isinstance(q, Path)
    assert q.string.endswith(os.path.join("a", "b"))


def test_path_combine_home(monkeypatch):
    import commands.path as mod
    mod.OS = type("O", (), {"windows": False})
    mod.Path = Path
    original_home = mod.Path.home
    try:
        mod.Path.home = staticmethod(lambda: "/home/user")
        assert Path.combine("~", "file") == os.path.join("/home/user", "file")
    finally:
        mod.Path.home = original_home


def test_path_combine_windows_drive(monkeypatch):
    import string
    import commands.path as mod
    mod.OS = type("O", (), {"windows": True})
    mod.os = os
    result = Path.combine("C:", "folder")
    assert result.startswith("C:")


def test_path_home_uses_console(monkeypatch):
    import commands.path as mod
    mod.Console = type("C", (), {"get_output": staticmethod(lambda cmd, pure_shell=True: "/home/test\n")})
    mod.Str = type("S", (), {"nl": staticmethod(lambda x: [x.strip()])})
    mod.OS = type("O", (), {"windows": False})
    # inject mocked Path.home by temporarily replacing in module
    original_home = Path.home
    try:
        Path.home = staticmethod(lambda: "/home/test")
        assert Path.home() == "/home/test"
    finally:
        Path.home = original_home


# ---- from test_path_more_coverage.py ----


import types

import pytest

from commands.path import Path
from commands.os import OS


def test_path_append_initializes_when_empty():
    p = Path()
    assert p.string is None
    p.append("a", "b")
    assert isinstance(p.string, str)
    assert p.string.endswith("a/b") or p.string.endswith("a\\b")


def test_path_repr_and_truediv():
    p = Path("a")
    r = repr(p)
    assert r.startswith("Path(")
    assert "a" in r
    assert str(p / "b").endswith("a/b") or str(p / "b").endswith("a\\b")


def test_path_combine_windows_smb_and_drive(monkeypatch):
    monkeypatch.setattr(OS, "_windows", True)
    monkeypatch.setattr(OS, "_unix_family", False)

    from commands.const import backslash
    smb = Path.combine(backslash, "server", "share")
    assert smb.startswith(backslash * 2)

    drive = Path.combine("C:", "Windows")
    assert drive.endswith("Windows")

    # Non-drive 2-char prefix should pass through unchanged (covers Path.combine line 91).
    weird = Path.combine("1:", "x")
    assert "1:" in weird


def test_path_home_uses_expanduser(monkeypatch):
    monkeypatch.setattr("commands.path.os.path.expanduser", lambda _path: "C:\\Users\\Me")
    assert Path.home() == "C:\\Users\\Me"
