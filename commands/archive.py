#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with zip and tar.lzma archives."""
from __future__ import annotations
from .module import LazyModule, LazyProperty

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Literal, Optional, cast
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value
    ZipMode = str

if TYPE_CHECKING:
    ZipMode = Literal["r", "w", "x", "a"]

__version__ = "0.6.0"
zipfile = LazyModule("zipfile")
tarfile = LazyModule("tarfile")
os = LazyModule("os")
sys = LazyModule("sys")
File = LazyProperty(".file", "File")
Dir = LazyProperty(".dir", "Dir")
Print = LazyProperty(".print", "Print")
CLI = LazyProperty(".cli", "CLI")
Path = LazyProperty(".path", "Path")


class Archive:
    """Archive creation and extraction helpers for zip and tar formats."""

    MODE_ZIPDEFLATED = 1
    MODE_TARLZMA = 2
    MODE_TARGZ = 3

    def __init__(self, archive_file: Optional[str], archive_type: int = MODE_ZIPDEFLATED, mode: str = "a") -> None:
        self.archive_file = archive_file
        self.archive_type = archive_type
        self.mode = mode
        self._real_archive_object: Any = None

    def _ensure_archive_file(self) -> str:
        if not self.archive_file:
            raise ValueError("archive_file must be set")
        return self.archive_file

    def _open(
        self,
        mode: Optional[str] = None,
        archive_file: Optional[str] = None
    ) -> Any:
        archive_file = archive_file or self._ensure_archive_file()
        use_mode = mode or self.mode
        use_type = self.archive_type

        if use_type == self.MODE_ZIPDEFLATED:
            zip_mode = cast(ZipMode, use_mode)
            self._real_archive_object = zipfile.ZipFile(archive_file, mode=zip_mode)
        elif use_type == self.MODE_TARLZMA:
            mode_str = f"{use_mode}:xz"
            self._real_archive_object = tarfile.open(archive_file, mode=mode_str)
        elif use_type == self.MODE_TARGZ:
            if use_mode not in ("r", "w", "x"):
                raise ValueError("mode must be 'r', 'w' or 'x'")
            mode_str = f"{use_mode}:gz"
            self._real_archive_object = tarfile.open(archive_file, mode=mode_str)
        else:
            raise ValueError("unknown archive_type")
        return self._real_archive_object

    def _close(self) -> None:
        if self._real_archive_object is not None:
            self._real_archive_object.close()
            self._real_archive_object = None

    @property
    def path(self) -> Optional[str]:
        """Return the archive file path."""
        return self.archive_file

    def add_file(
        self,
        input_file: str,
        arcname: Optional[str] = None
    ) -> "Archive":
        """Add a file to the archive using instance defaults."""
        return self.file(input_file=input_file, arcname=arcname)

    def add_dir(self, input_dir: str, verbose: bool = False) -> "Archive":
        """Add a directory to the archive using instance defaults."""
        return self.dir(input_dir=input_dir, verbose=verbose)

    def file(
        self,
        input_file: str,
        arcname: Optional[str] = None
    ) -> "Archive":
        """Archive a single file into a target archive."""
        archive_file = self._ensure_archive_file()
        use_mode = self.mode
        use_type = self.archive_type

        if not File.exist(input_file):
            raise IOError(input_file + " is not file")

        if not File.exist(archive_file) and "w" not in use_mode:
            temp_file = archive_file + ".tmp"
            File.delete(temp_file, verbose=False)

            archive = self._open(mode=use_mode, archive_file=temp_file)
            self._write(archive, input_file, arcname=arcname, archive_type=use_type)
            self._close()

            File.move(temp_file, archive_file)
        else:
            archive = self._open(mode=use_mode)
            self._write(archive, input_file, arcname=arcname, archive_type=use_type)
            self._close()
        return self

    def dir(self, input_dir: str, verbose: bool = False) -> "Archive":
        """Archive a directory into a target archive."""
        archive_file = self._ensure_archive_file()
        use_type = self.archive_type

        if not Dir.exist(input_dir):
            raise IOError(input_dir + " is not dir")

        temp_file = archive_file + ".tmp"
        File.delete(temp_file, verbose=False)

        archive = self._open(mode="w", archive_file=temp_file)
        for root, _dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self._write(
                    archive,
                    file_path,
                    arcname=os.path.relpath(os.path.join(root, file), input_dir),
                    archive_type=use_type
                )
                if verbose:
                    Print.rewrite(CLI.wait_update(verbose=False), file_path, "archived")

        self._close()
        File.move(temp_file, archive_file)
        return self

    def extract_all(self, output_dir: str) -> "Archive":
        """Extract all files to the output directory."""
        archive = self._open(mode="r")
        self._extract_all(archive, output_dir, archive_type=self.archive_type)
        self._close()
        return self

    def extract(self, path_inside_archive: str, output_path: str) -> "Archive":
        """Extract a single file to the output path."""
        temp_dir = Path.temp()
        archive = self._open(mode="r")
        temp_path = self._extract_single(archive, path_inside_archive, temp_dir, archive_type=self.archive_type)
        self._close()

        File.move(temp_path, output_path)
        return self

    def _write(self, archive: Any, input_file: str, arcname: Optional[str], archive_type: int) -> Any:
        additional_args: dict[str, Any] = {}
        if archive_type == self.MODE_ZIPDEFLATED:
            additional_args["compress_type"] = zipfile.ZIP_DEFLATED
            return archive.write(input_file, arcname=arcname, **additional_args)
        if archive_type in (self.MODE_TARLZMA, self.MODE_TARGZ):
            return archive.add(input_file, arcname=arcname, **additional_args)
        return archive.write(input_file, arcname=arcname, **additional_args)

    def _extract_single(self, archive: Any, path_inside_archive: str, output_dir: str, archive_type: int) -> str:
        kwargs: dict[str, Any] = {}
        if archive_type in (self.MODE_TARLZMA, self.MODE_TARGZ):
            if sys.version_info >= (3, 12):
                kwargs["filter"] = "data"

        temp_path = archive.extract(path_inside_archive, output_dir, **kwargs)
        if temp_path is None:
            temp_path = Path.combine(output_dir, path_inside_archive)
        return cast(str, temp_path)

    def _extract_all(self, archive: Any, output_dir: str, archive_type: int) -> Any:
        kwargs: dict[str, Any] = {}
        if archive_type in (self.MODE_TARLZMA, self.MODE_TARGZ):
            if sys.version_info >= (3, 12):
                kwargs["filter"] = "data"
        return archive.extractall(output_dir, **kwargs)
