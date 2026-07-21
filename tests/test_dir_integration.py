# Consolidated tests for commands/dir.py (integration)

# ---- from test_dir_integration.py ----

# Placeholder for future tests.
import pytest
import tempfile
import os
from commands.dir import Dir
import shutil
from unittest.mock import patch, Mock, MagicMock
import pathlib
import stat

def test_dir_create():
    with tempfile.TemporaryDirectory() as tmpdir:
        new_dir = os.path.join(tmpdir, "test_dir")
        Dir.create(new_dir)
        assert os.path.isdir(new_dir)

def test_dir_create_nested():
    with tempfile.TemporaryDirectory() as tmpdir:
        new_dir = os.path.join(tmpdir, "level1", "level2", "level3")
        Dir.create(new_dir)
        assert os.path.isdir(new_dir)

def test_dir_create_existing():
    with tempfile.TemporaryDirectory() as tmpdir:
        Dir.create(tmpdir)
        assert os.path.isdir(tmpdir)

def test_dir_list_of_entries():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir"))
        open(os.path.join(tmpdir, "file.txt"), "w").close()
        entries = Dir.list_of_entries(tmpdir)
        assert "subdir" in entries
        assert "file.txt" in entries

def test_dir_list_of_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir"))
        open(os.path.join(tmpdir, "file1.txt"), "w").close()
        open(os.path.join(tmpdir, "file2.txt"), "w").close()
        files = Dir.list_of_files(tmpdir)
        assert "file1.txt" in files
        assert "file2.txt" in files
        assert "subdir" not in files

def test_dir_list_of_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir1"))
        os.makedirs(os.path.join(tmpdir, "subdir2"))
        open(os.path.join(tmpdir, "file.txt"), "w").close()
        dirs = Dir.list_of_dirs(tmpdir)
        assert "subdir1" in dirs
        assert "subdir2" in dirs
        assert "file.txt" not in dirs

def test_dir_number_of_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, "file1.txt"), "w").close()
        open(os.path.join(tmpdir, "file2.txt"), "w").close()
        os.makedirs(os.path.join(tmpdir, "subdir"))
        open(os.path.join(tmpdir, "subdir", "file3.txt"), "w").close()
        count = Dir.number_of_files(tmpdir, verbose=False)
        assert count == 3

def test_dir_exist():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert Dir.exist(tmpdir)
        assert not Dir.exist(os.path.join(tmpdir, "nonexistent"))

def test_dir_delete():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "to_delete")
        os.makedirs(test_dir)
        open(os.path.join(test_dir, "file.txt"), "w").close()
        Dir.delete(test_dir, no_sleep=True)
        assert not os.path.exists(test_dir)

class TestDirCoverage:
    """Tests to improve coverage for dir9.py"""
    def test_number_of_files_verbose(self, capsys):
        """Test Dir.number_of_files with verbose=True (line 54)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "file1.txt"), "w").close()
            open(os.path.join(tmpdir, "file2.txt"), "w").close()

            count = Dir.number_of_files(tmpdir, verbose=True)

            assert count == 2
            captured = capsys.readouterr()
            assert "contain" in captured.out
            assert "2" in captured.out
            assert "files" in captured.out
    def test_batch_rename(self, capsys):
        """Test Dir.batch_rename (lines 58-72)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            open(os.path.join(tmpdir, "old_file1.txt"), "w").close()
            open(os.path.join(tmpdir, "old_file2.txt"), "w").close()
            open(os.path.join(tmpdir, "other.txt"), "w").close()

            # Batch rename with verbose=True
            Dir.batch_rename(tmpdir, "old_", "new_", verbose=True)

            # Check files were renamed
            files = Dir.list_of_files(tmpdir)
            assert "new_file1.txt" in files
            assert "new_file2.txt" in files
            assert "other.txt" in files
            assert "old_file1.txt" not in files

            # Check verbose output
            captured = capsys.readouterr()
            assert "renamed to" in captured.out
    def test_batch_rename_quiet(self):
        """Test Dir.batch_rename with verbose=False"""
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "test_old.txt"), "w").close()

            Dir.batch_rename(tmpdir, "old", "new", verbose=False)

            files = Dir.list_of_files(tmpdir)
            assert "test_new.txt" in files
    def test_cleanup(self):
        """Test Dir.cleanup (lines 129-139)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create content
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            open(os.path.join(tmpdir, "file1.txt"), "w").close()
            open(os.path.join(subdir, "file2.txt"), "w").close()

            # Cleanup (should remove files but keep directory structure)
            Dir.cleanup(tmpdir)

            # Directory should exist with subdirectory but no files
            assert os.path.isdir(tmpdir)
            assert os.path.isdir(subdir)
            assert not os.path.isfile(os.path.join(tmpdir, "file1.txt"))
            assert not os.path.isfile(os.path.join(subdir, "file2.txt"))
    def test_cleanup_with_quiet_permission_error(self):
        """Test Dir.cleanup with quiet_permission_error=True (lines 136-137)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "file.txt"), "w").close()

            # quiet_permission_error should set skip_permission_error
            Dir.cleanup(tmpdir, quiet_permission_error=True)

            assert os.path.isdir(tmpdir)
            assert len(os.listdir(tmpdir)) == 0
    def test_dir_instance_rename_and_delete(self, tmp_path):
        dir_path = tmp_path / "dir1"
        Dir.create(dir_path)
        d = Dir(dir_path)

        new_path = d.rename("dir2")
        assert os.path.basename(new_path) == "dir2"
        assert os.path.isdir(new_path)

        d.delete(no_sleep=True)
        assert not os.path.exists(new_path)
    def test_delete_cleanup_mode(self):
        """Test Dir.delete with cleanup=True (line 118)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            open(os.path.join(tmpdir, "file.txt"), "w").close()

            Dir.delete(tmpdir, cleanup=True, no_sleep=True)

            # Directory should exist with subdirectory but no files
            assert os.path.isdir(tmpdir)
            assert os.path.isdir(subdir)
            assert not os.path.isfile(os.path.join(tmpdir, "file.txt"))
    def test_copy_basic(self):
        """Test Dir.copy basic usage (lines 142-212)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            # Create source structure
            os.makedirs(src)
            open(os.path.join(src, "file1.txt"), "w").write("content1")
            subdir = os.path.join(src, "subdir")
            os.makedirs(subdir)
            open(os.path.join(subdir, "file2.txt"), "w").write("content2")

            # Copy
            Dir.copy(src, dst)

            # Verify
            assert os.path.isdir(dst)
            assert os.path.isfile(os.path.join(dst, "file1.txt"))
            assert os.path.isfile(os.path.join(dst, "subdir", "file2.txt"))
    def test_copy_verbose(self, capsys):
        """Test Dir.copy with verbose=True (lines 165-166, 195-196)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            os.makedirs(src)
            open(os.path.join(src, "file.txt"), "w").close()

            Dir.copy(src, dst, verbose=True)

            captured = capsys.readouterr()
            assert "copying" in captured.out or "creating dir" in captured.out
    def test_copy_with_ignore(self):
        """Test Dir.copy with ignore function (lines 170-172)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            os.makedirs(src)
            open(os.path.join(src, "keep.txt"), "w").close()
            open(os.path.join(src, "ignore.txt"), "w").close()

            # Ignore function
            def ignore_func(dir, files):
                return [f for f in files if "ignore" in f]

            Dir.copy(src, dst, ignore=ignore_func)

            assert os.path.isfile(os.path.join(dst, "keep.txt"))
            assert not os.path.isfile(os.path.join(dst, "ignore.txt"))
    def test_move(self):
        """Test Dir.move (lines 215-234)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            # Create source
            os.makedirs(src)
            open(os.path.join(src, "file.txt"), "w").write("content")

            # Move
            Dir.move(src, dst)

            # Source should be gone, dst should exist
            assert not os.path.exists(src)
            assert os.path.isdir(dst)
            assert os.path.isfile(os.path.join(dst, "file.txt"))
    def test_move_verbose(self, capsys):
        """Test Dir.move with verbose=True (line 232)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            os.makedirs(src)
            open(os.path.join(src, "file.txt"), "w").close()

            Dir.move(src, dst, verbose=True)

            captured = capsys.readouterr()
            assert len(captured.out) > 0  # Should have some output
    def test_move_with_quiet_permission_error(self):
        """Test Dir.move with quiet_permission_error=True (lines 228-229)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            dst = os.path.join(tmpdir, "dst")

            os.makedirs(src)
            open(os.path.join(src, "file.txt"), "w").close()

            Dir.move(src, dst, quiet_permission_error=True)

            assert not os.path.exists(src)
            assert os.path.isdir(dst)
    def test_exists_alias(self):
        """Test Dir.exists alias (lines 246-247)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert Dir.exists(tmpdir)
            assert not Dir.exists(os.path.join(tmpdir, "nonexistent"))
    def test_get_size(self):
        """Test Dir.get_size (lines 250-263)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files with known sizes
            with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
                f.write("a" * 100)  # 100 bytes

            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            with open(os.path.join(subdir, "file2.txt"), "w") as f:
                f.write("b" * 50)  # 50 bytes

            size = Dir.get_size(tmpdir)
            assert size == 150
    def test_get_modification_time(self):
        """Test Dir.get_modification_time (lines 266-268)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = Dir.get_modification_time(tmpdir)
            assert isinstance(result, float)
            assert result > 0
    def test_get_free_space(self):
        """Test Dir.get_free_space (lines 271-274)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            free = Dir.get_free_space(tmpdir)
            assert isinstance(free, int)
            assert free > 0

class TestDirInstanceComprehensive:
    """Comprehensive tests for Dir instance methods"""
    def test_instance_create(self, tmp_path):
        """Test instance create method to cover lines 37-38"""
        test_dir = tmp_path / "test_instance_create"
        d = Dir(str(test_dir))
        d.create()
        assert test_dir.exists()
    def test_instance_move(self, tmp_path):
        """Test instance move method to cover lines 52-55"""
        src_dir = tmp_path / "src_move"
        dst_dir = tmp_path / "dst_move"
        src_dir.mkdir()

        d = Dir(str(src_dir))
        d.move(str(dst_dir))

        # Path should be updated to destination
        assert d.path == str(dst_dir)
        assert dst_dir.exists()
    def test_instance_delete(self, tmp_path):
        """Test instance delete method to cover lines 59-60"""
        test_dir = tmp_path / "test_instance_delete"
        test_dir.mkdir()

        d = Dir(str(test_dir))
        d.delete()

        assert not test_dir.exists()
    def test_instance_delete_with_cleanup(self, tmp_path):
        """Test instance delete with cleanup parameter"""
        test_dir = tmp_path / "test_cleanup_dir"
        test_dir.mkdir()
        test_file = test_dir / "file.txt"
        test_file.write_text("content")

        d = Dir(str(test_dir))
        d.delete(cleanup=True)

        # Directory should exist but be empty
        assert test_dir.exists()
        assert len(list(test_dir.iterdir())) == 0
    def test_instance_delete_with_skip_permission_error(self, tmp_path):
        """Test instance delete with skip_permission_error parameter"""
        test_dir = tmp_path / "test_skip_perm"
        test_dir.mkdir()

        d = Dir(str(test_dir))
        d.delete(skip_permission_error=True)

        assert not test_dir.exists()
    def test_instance_delete_with_quiet_permission_error(self, tmp_path):
        """Test instance delete with quiet_permission_error parameter"""
        test_dir = tmp_path / "test_quiet_perm"
        test_dir.mkdir()

        d = Dir(str(test_dir))
        d.delete(quiet_permission_error=True)

        assert not test_dir.exists()

class TestDirCopySymlinksAndErrors:
    """Tests for symlinks and error handling in copy method"""
    def test_copy_with_symlinks(self, tmp_path):
        """Test copy with symlinks=True to cover lines 233-241"""
        src_dir = tmp_path / "src_symlink"
        dst_dir = tmp_path / "dst_symlink"
        src_dir.mkdir()

        # Create a file and a symlink to it
        real_file = src_dir / "real_file.txt"
        real_file.write_text("content")
        symlink_file = src_dir / "symlink_file.txt"

        try:
            symlink_file.symlink_to(real_file)

            # Copy with symlinks=True
            Dir.copy(str(src_dir), str(dst_dir), symlinks=True)

            # Check that symlink was copied
            copied_symlink = dst_dir / "symlink_file.txt"
            assert copied_symlink.exists()
        except OSError:
            pytest.skip("Symlink creation not supported")

def test_dir_instance_move_updates_path(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    d = Dir(src)
    d.move(dst)
    assert str(d.path) == str(dst)
    assert not src.exists()
    assert dst.exists()

def test_dir_number_of_files_and_get_size(tmp_path):
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_text("world")
    assert Dir.number_of_files(tmp_path) == 2
    size = Dir.get_size(tmp_path)
    assert size == os.path.getsize(tmp_path / "a.txt") + os.path.getsize(tmp_path / "sub" / "b.txt")

def test_dir_batch_rename(tmp_path):
    f1 = tmp_path / "old1.txt"
    f2 = tmp_path / "keep.txt"
    f1.write_text("x")
    f2.write_text("y")
    Dir.batch_rename(tmp_path, "old", "new")
    assert (tmp_path / "new1.txt").exists()
    assert (tmp_path / "keep.txt").exists()

def test_dir_copy_with_ignore_and_errors(tmp_path, monkeypatch):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "keep.txt").write_text("ok")
    (src / "skip.me").write_text("bad")

    def ignore_func(path, names):
        return {"skip.me"}

    # simulate PermissionError on copy
    original_copy2 = os.path
    import shutil
    called = []

    def fake_copy2(s, d):
        called.append((s, d))
        if "keep" in s:
            pathlib.Path(d).write_text(pathlib.Path(s).read_text())
            return None
        raise PermissionError("fail")

    monkeypatch.setattr(shutil, "copy2", fake_copy2)
    Dir.copy(src, dst, ignore=ignore_func, skip_permission_error=True, quiet_permission_error=True)
    assert (dst / "keep.txt").exists()
    assert not (dst / "skip.me").exists()

def test_dir_exist_alias(tmp_path):
    tmp_path.mkdir(exist_ok=True)
    assert Dir.exist(tmp_path)
    assert Dir.exists(tmp_path)
