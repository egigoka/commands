#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with directories."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import os
    import shutil
    import stat
    import time
    from typing import Any, Callable, Iterable, Iterator, List, Optional, Sequence, Tuple
    from .file import File
    from .path import Path

from .module import LazyModule, LazyProperty
__version__ = "1.8.1"
if not TYPE_CHECKING:
    os = LazyModule("os")
    stat = LazyModule("stat")
    time = LazyModule("time")
    shutil = LazyModule("shutil")
    Path = LazyProperty(".path", "Path")
    File = LazyProperty(".file", "File")


class Dir:
    """Class to work with directories."""

    path: Optional[str]

    def __getattribute__(self, name: str) -> Any:
        """Forward selected instance methods to class methods."""
        if name in {"create", "delete", "cleanup", "move"}:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                self._ensure_path()
                method = getattr(self.__class__, name)
                path = self.path
                assert path is not None
                result = method(path, *args, **kwargs)
                if name in {"move"}:
                    self.path = args[0] if args else kwargs.get("dst_", self.path)
                return result
            return _wrapper
        return object.__getattribute__(self, name)

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = Path.full(path) if path else None

    def _ensure_path(self) -> None:
        if not self.path:
            raise ValueError("Directory path is not set")

    @property
    def string(self) -> Optional[str]:
        """Return stored directory path."""
        return self.path

    def rename(self, new_name: str) -> str:
        """Rename directory to a new name within the same parent."""
        self._ensure_path()
        path = self.path
        assert path is not None
        parent = os.path.dirname(path) or "."
        new_path = os.path.join(parent, new_name)
        os.rename(path, new_path)
        self.path = new_path
        return new_path


    @classmethod
    def create(cls, dir_name: str) -> None:
        """Create a directory if it doesn't exist.

        <br>`param dir_name` string with path to new dir
        <br>`return`
        """
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    @classmethod
    def list_of_entries(cls, path: str) -> List[str]:
        """Return list of files and folders in a path.

        <br>`param path` string with path to folder
        <br>`return` list of files and folders in path
        """
        return os.listdir(path)

    @classmethod
    def list_of_files(cls, path: str) -> List[str]:
        """Return list of files in a directory."""
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    @classmethod
    def list_of_dirs(cls, path: str) -> List[str]:
        """Return list of subdirectories in a directory."""
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    @classmethod
    def number_of_files(cls, path: str, verbose: bool = False) -> int:
        """Return the number of files in a directory.

        <br>`param path` string with path
        <br>`param verbose` suppress print to console
        <br>`return` int count of files in directory
        """
        if not cls.exist(path):
            raise FileNotFoundError(f"Directory '{path}' not found")
        cnt = 0
        for root, dirs, files in os.walk(path):
            cnt += len(files)
        if verbose:
            print(os.path.split(path)[1], "contain", cnt, "files")
        return cnt

    @classmethod
    def batch_rename(
        cls,
        directory: str,
        previous_name_substring: str,
        new_name_substring: str,
        verbose: bool = False
    ) -> None:
        """Batch rename files in a directory.

        <br>`param directory` string with path to directory
        <br>`param previous_name_substring` string that must be changed in every file
        <br>`param new_name_substring` string to that will be changed 'input_str'
        <br>`param verbose` suppress print to console
        <br>`return` None
        """
        for filename in cls.list_of_files(directory):
            if previous_name_substring in filename:
                path_from = Path.combine(directory, filename)
                final_name = filename.replace(previous_name_substring, new_name_substring)
                final_path = Path.combine(directory, final_name)
                File.rename(path_from, final_path)
                if verbose:
                    print(path_from, "renamed to", final_path)

    @classmethod
    def delete(
        cls,
        path: str,
        cleanup: bool = False,
        remove_readonly: bool = True,
        no_sleep: bool = False,
        skip_permission_error: bool = False,
        quiet_permission_error: bool = False
    ) -> None:
        """Remove a directory.

        <br>`param path` string
        <br>`param cleanup` boolean, True doesn't delete "path" folder, only content
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        for root, dirs, files in os.walk(path):  # , topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if remove_readonly:
                    try:
                        os.remove(os.path.join(root, name))  # unsafe
                    except PermissionError:
                        # let's just assume that it's read-only and chmod it.
                        if not skip_permission_error:
                            os.chmod(file_path, stat.S_IWRITE)
                            os.remove(file_path)
                        else:
                            try:
                                os.chmod(file_path, stat.S_IWRITE)
                                os.remove(file_path)
                            except PermissionError as err:
                                if not quiet_permission_error:
                                    print(err)
                else:
                    if not skip_permission_error:
                        os.remove(file_path)  # unsafe
                    else:
                        try:
                            os.remove(file_path)  # unsafe
                        except PermissionError as err:
                            if not quiet_permission_error:
                                print(err)
            for name in dirs:
                cls.delete(os.path.join(root, name), cleanup, remove_readonly, no_sleep,
                           skip_permission_error, quiet_permission_error)  # recursion
        if not cleanup:
            try:

                os.rmdir(path)  # unsafe
            except OSError:
                if not no_sleep:
                    time.sleep(0.05)
                os.rmdir(path)  # unsafe

    @classmethod
    def cleanup(
        cls,
        path: str,
        skip_permission_error: bool = False,
        quiet_permission_error: bool = False
    ) -> None:
        """Remove all content in a directory.

        <br>`param path` string
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        cls.delete(path, cleanup=True,
                   skip_permission_error=skip_permission_error, quiet_permission_error=quiet_permission_error)

    @classmethod
    def copy(
        cls,
        src: str,
        dst: str,
        symlinks: bool = False,
        ignore: Optional[Callable[[str, List[str]], Iterable[str]]] = None,
        skip_permission_error: bool = False,
        quiet_permission_error: bool = False,
        skip_file_not_found_error: bool = False,
        quiet_file_not_found_error: bool = False,
        skip_os_error: bool = False,
        quiet_os_error: bool = False,
        verbose: bool = False
    ) -> None:
        """Copy a directory tree into a destination.

        Same behavior as shutil.copytree, but can copy into existing directory
        https`//stackoverflow.com/a/22331852/6519078
        <br>`param src` string, source directory to copy
        <br>`param dst` string, destination
        <br>`param symlinks` boolean, following symlinks
        <br>`param ignore` You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments` a directory name and the files in it, it
        should return an iterable of ignored files.
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        if not os.path.exists(dst):
            if verbose:
                print(f"creating dir {dst}")
            os.makedirs(dst)
            shutil.copystat(src, dst)
        lst = os.listdir(src)
        if ignore:
            excl = ignore(src, lst)
            lst = [x for x in lst if x not in excl]
        for item in lst:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)
                os.symlink(os.readlink(s), d)
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    lchmod = getattr(os, "lchmod", None)
                    if lchmod is not None:
                        lchmod(d, mode)
                except Exception:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                cls.copy(src=s, dst=d, symlinks=symlinks, ignore=ignore,
                         skip_permission_error=skip_permission_error, quiet_permission_error=quiet_permission_error,
                         skip_file_not_found_error=skip_file_not_found_error,
                         quiet_file_not_found_error=quiet_file_not_found_error,
                         skip_os_error=skip_os_error, quiet_os_error=quiet_os_error,
                         verbose=verbose)
            else:
                try:
                    if verbose:
                        print(f"copying {s} to {d}")
                    shutil.copy2(s, d)
                except PermissionError as err:
                    if not quiet_permission_error:
                        print(err)
                    if not skip_permission_error:
                        raise
                except FileNotFoundError as err:
                    if not quiet_file_not_found_error:
                        print(err)
                    if not skip_file_not_found_error:
                        raise
                except OSError as err:
                    if not quiet_os_error:
                        print(err)
                    if not skip_os_error:
                        raise

    @classmethod
    def move(
        cls,
        src_: str,
        dst_: str,
        symlinks_: bool = False,
        ignore_: Optional[Callable[[str, List[str]], Iterable[str]]] = None,
        skip_permission_error: bool = False,
        quiet_permission_error: bool = False,
        verbose: bool = False
    ) -> None:
        """Move a directory by copying then deleting source.

        <br>`param src` string, source directory to copy
        <br>`param dst` string, destination
        <br>`param symlinks` boolean, following symlinks
        <br>`param ignore` You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments` a directory name and the files in it, it
        should return an iterable of ignore files.
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        cls.copy(src=src_, dst=dst_, symlinks=symlinks_, ignore=ignore_,
                 skip_permission_error=skip_permission_error,
                 quiet_permission_error=quiet_permission_error, verbose=verbose)

        cls.delete(src_)

    @classmethod
    def exist(cls, filename: str) -> bool:
        """Return True if a directory exists.

        <br>`param filename` string with path to dir
        <br>`return` boolean that means existence of dir
        """
        return os.path.isdir(filename)

    @classmethod
    def exists(cls, filename: str) -> bool:
        """Alias for exist."""
        return cls.exist(filename=filename)

    @classmethod
    def get_size(cls, path: str) -> int:
        """Return total size of files in a directory."""
        if not cls.exist(path):
            raise FileNotFoundError(f"Directory '{path}' not found")

        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = Path.combine(root, file)
                size = File.get_size(filepath)
                assert isinstance(size, int)
                total_size += size
        return total_size

    @classmethod
    def get_modification_time(cls, path: str) -> float:
        """Return directory modification time."""
        return float(File.get_modification_time(path))

    @classmethod
    def get_free_space(cls, path: str) -> int:
        """Return free disk space for the given path."""
        total, used, free = shutil.disk_usage(path)
        return free
