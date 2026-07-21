#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with files."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import codecs
    import hashlib
    import os
    import shutil
    import sys
    import time
    from typing import Any, Iterator, Optional, Tuple, Union, cast
    from .bytes import Bytes
    from .console import Console
    from .const import GiB, KiB, MiB, TiB
    from .dir import Dir
    from .os import OS as OSClass
    from .path import Path
    from .time import Time
    OS = OSClass()
else:
    def cast(_type, value):
        """Return value unchanged for runtime typing fallback."""
        return value


from .module import LazyModule, LazyProperty

__version__ = "1.7.0"
if not TYPE_CHECKING:
    os = LazyModule("os")
    sys = LazyModule("sys")
    time = LazyModule("time")
    shutil = LazyModule("shutil")
    codecs = LazyModule("codecs")
    hashlib = LazyModule("hashlib")
    Path = LazyProperty(".path", "Path")
    Dir = LazyProperty(".dir", "Dir")
    OS = LazyProperty(".os", "OS")
    Time = LazyProperty(".time", "Time")
    Bytes = LazyProperty(".bytes", "Bytes")
    Console = LazyProperty(".console", "Console")
# pylint: disable=c-extension-no-member

win32api = LazyModule("win32api", optional=True)
win32con = LazyModule("win32con", optional=True)
winmagic = LazyModule("winmagic", optional=True)
magic = LazyModule("magic", optional=True)
if not TYPE_CHECKING:
    KiB = LazyProperty(".const", "KiB")
    MiB = LazyProperty(".const", "MiB")
    GiB = LazyProperty(".const", "GiB")
    TiB = LazyProperty(".const", "TiB")


class File:
    """Class to work with files."""

    path: Optional[str]

    def __getattribute__(self, name: str) -> Any:
        """Forward selected instance methods to class methods."""
        if name in {"move", "rename", "delete", "copy", "backup", "hide"}:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                self._ensure_path()
                method = getattr(self.__class__, name)
                path = self.path
                assert path is not None
                result = method(path, *args, **kwargs)
                if name in {"move", "rename"}:
                    self.path = str(result)
                    return self.path
                return result
            return _wrapper
        return object.__getattribute__(self, name)

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = Path.full(path) if path else None

    def _ensure_path(self) -> None:
        if not self.path:
            raise ValueError("File path is not set")

    @property
    def string(self) -> Optional[str]:
        """Return stored file path."""
        return self.path

    @classmethod
    def create(cls, filename: str, verbose: bool = False) -> None:
        """Create a file and parent directories if needed.

        <br>`param filename` string with path to creating file
        <br>`param verbose` boolean, if True, suppress output to console
        <br>`return` None
        """
        if not isinstance(verbose, bool):
            raise TypeError("argument 'verbose' must be boolean")
        filename = Path.full(filename)
        if os.path.split(filename)[0] != "":
            Dir.create(os.path.split(filename)[0])
        if verbose:
            print(f"Creating file {filename}")
        if not cls.exist(filename):
            with open(filename, 'a'):  # open file and close after
                os.utime(filename, None)  # change time of file modification
        else:
            raise FileExistsError("file " + str(filename) + " exist")
        if not cls.exist(filename):
            raise FileNotFoundError("error while creating file " + filename +
                                    "try to repair script at " + Path.full(sys.argv[0]))
        elif verbose:
            print(f"File {filename} created")

    @classmethod
    def delete(cls, path: str, verbose: bool = False, no_sleep: bool = False) -> None:
        """Delete a file.

        <br>`param path` string with path to deleting file
        <br>`param verbose` boolean, suppress print to console
        <br>`param no_sleep` boolean, if True - function skip sleep in 0.05 seconds after deleting file
        (to ensure than file
        deleted before next code run)
        <br>`return` None
        """
        if os.path.isdir(path):
            raise IsADirectoryError(path + " is directory, use Dir.delete to delete")
        try:
            os.remove(path)
        except FileNotFoundError:
            if verbose:
                print("file", path, "is not exist")
        if verbose:
            print("file", path, "is deleted")
        if not no_sleep:
            time.sleep(0.05)
            if cls.exist(path):
                raise FileExistsError(path + " is not deleted")

    @classmethod
    def move(cls, input_file: str, output_file: str) -> str:
        """Move a file to a new path.

        <br>`param input_file` string with path to previous file place
        <br>`param output_file` string with path to new file place
        <br>`return` None
        """
        if cls.exist(input_file):
            return shutil.move(input_file, output_file)
        raise FileNotFoundError(f"When trying to move/rename file '{input_file}'>'{output_file}': "
                                f"File '{input_file}' not found")

    @classmethod
    def copy(cls, input_file: str, output_file: str) -> None:
        """Copy a file to a new path.

        <br>`param input_file` string with path to existing file
        <br>`param output_file` string with path to new file
        <br>`return` None
        """
        shutil.copy2(input_file, output_file)

    @classmethod
    def rename(cls, input_file: str, output_file: str) -> str:
        """Rename a file to a new path.

        <br>`param input_file` string with path to previous file place
        <br>`param output_file` string with path to new file place
        <br>`return` string with path to new file place
        """
        return cls.move(input_file, output_file)

    @classmethod
    def hide(cls, filename: str, verbose: bool = False) -> str:
        """Hide a file by OS-specific means.

        Adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
        file, if running on Windows
        <br>`param filename` string with path to file
        <br>`param verbose` suppress print to console
        <br>`return` string with new filename
        """
        filename = Path.full(filename)
        if OS.windows:
            win32api.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN)  # hiding file like windows do
        elif OS.unix_family:
            dotted_file = Path.combine(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
            filename = cls.rename(filename, dotted_file)  # adding dot
        else:
            raise NotImplementedError("Your OS doesn't supported")
        if verbose:
            print("file", filename, "is hidden now")
        return filename

    @classmethod
    def backup(
        cls,
        filename: str,
        subdirectory: str = "bak",
        hide: bool = True,
        verbose: bool = False
    ) -> str:
        """Backup a file into a subdirectory.

        Move file to subdirectory, adds sort of timestamp to filename and hide file if 'hide' argument is True
        <br>`param filename` string with path to file
        <br>`param subdirectory` string with name of subdirectory of backed up files
        <br>`param hide` boolean, define hide file or not
        <br>`param verbose` boolean, suppress print to console
        <br>`return`
        """
        filename = Path.full(filename)  # normalize filename
        backup_filename = str(filename) + "." + Time.dotted() + ".bak"  # add dotted time to back up filename
        backup_dir, backup_name = os.path.split(backup_filename)  # splitting filename to folder and file
        try:  # if subdirectory has no len
            if len(subdirectory) < 1:  # if subdirectory has zero len
                raise TypeError("subdirectory must have non-zero len")
        except TypeError:  # if subdirectory has no len
            subdirectory = "bak"  # set subdirectory to default
            print("len(subdirectory) < 1, so subdirectory = 'bak'")  # print error
        subdirectory = Path.combine(backup_dir, subdirectory)  # append subdirectory name
        Dir.create(subdirectory)  # create subdirectory
        backup_filename = str(Path.combine(subdirectory, backup_name))  # backup file name full path
        shutil.copy2(filename, backup_filename)  # finally backup file
        if hide:
            backup_filename = cls.hide(backup_filename)  # hiding file
        backup_filename_str = str(backup_filename)
        if not os.path.isfile(backup_filename_str):  # if file is not created
            raise FileNotFoundError(backup_filename_str + " isn't created while backup")
        if verbose:
            print("backup of file", filename, "created as", backup_filename_str)  # all is ok, print that
        return backup_filename_str

    @classmethod
    def wipe(cls, path: str) -> None:
        """Erase content of a file.

        <br>`param path` string with path to file
        <br>`return` None
        """
        file = open(path, 'w')
        file.close()

    @classmethod
    def get_encoding(cls, path: str, count_of_symbols: Union[bool, int] = True) -> str:
        """Detect file encoding.

        <br>`param path` path to file
        <br>`param count_of_symbols` how much symbols use to auto define decoding, if True, uses 10000
        <br>`return` string, file encoding
        """
        if count_of_symbols is True:  # you can define how much symbols use to define encoding
            count_of_symbols = 10000
        with open(path, "rb") as raw_file:
            slice_of_raw_data = raw_file.read(count_of_symbols)
        encoding = Bytes.get_encoding(slice_of_raw_data)
        return str(encoding)

    @classmethod
    def _read_with_encoding(cls, path: str, encoding: str) -> str:
        with open(path, "r", encoding=encoding) as file:
            return file.read()

    @classmethod
    def read(
        cls,
        path: str,
        encoding: str = "utf-8",
        auto_detect_encoding: Union[bool, int] = True,
        mode: str = "r"
    ) -> Optional[Union[str, bytes]]:
        # return pipe to file content
        """Read file content.

        <br>`param path` path to file
        <br>`param auto_detect_encoding` how much symbols use to auto define decoding, if True, uses 10000
        <br>`return` pipe, to file text content with utf-8 decoding
        """
        if mode == "r":
            try:
                if auto_detect_encoding:
                    encoding = cls.get_encoding(path, count_of_symbols=auto_detect_encoding)
                try:
                    return cls._read_with_encoding(path, encoding)
                except LookupError:
                    if encoding.lower() == "EUC-TW".lower():
                        return cls._read_with_encoding(path, "TIS-620")  # crude fix for EUC-TW
            except UnicodeDecodeError:
                with codecs.open(path, encoding='cp1251', errors='replace') as file:
                    content = file.read()
                    if isinstance(content, (str, bytes)):
                        return content
                    return str(content)
        elif mode in ["b", "rb"]:
            with open(path, "rb") as file:
                content_bytes: bytes = file.read()
                return content_bytes
        return None

    @classmethod
    def write(
        cls,
        filename: str,
        what_to_write: Any,
        mode: str = "a",
        encoding: str = "utf-8",
        verbose: bool = False
    ) -> None:
        """Write to a file.

        Write to end of file if "mode" arg isn't redefined
        <br>`param filename` string with path to file
        <br>`param what_to_write` string to write
        <br>`param mode` string with any mode that supported by python open() func
        <br>`param encoding` string with any encoding
        <br>`param verbose` boolean, if True, suppress output to console
        <br>`return` None
        """
        if verbose:
            print(f"Writing to file {filename}")
        is_binary = "b" in mode
        if is_binary:
            with open(filename, mode=mode) as file:
                if isinstance(what_to_write, str):
                    data = what_to_write.encode(encoding)
                elif isinstance(what_to_write, bytearray):
                    data = bytes(what_to_write)
                elif isinstance(what_to_write, bytes):
                    data = what_to_write
                else:
                    data = str(what_to_write).encode(encoding)
                file.write(data)
        else:
            with open(filename, mode=mode, encoding=encoding) as file:
                if isinstance(what_to_write, bytes):
                    text = what_to_write.decode(encoding, errors="replace")
                elif isinstance(what_to_write, bytearray):
                    text = bytes(what_to_write).decode(encoding, errors="replace")
                else:
                    text = str(what_to_write)
                file.write(text)
        if verbose:
            print(f"Written to file {filename}")

    @classmethod
    def read_by_chunk(
        cls,
        path: str,
        chunk_size: int = 8192,
        mode: str = "rb"
    ) -> Iterator[Union[str, bytes]]:
        """Generate chunks of file content.

        <br>`param path` path to file
        <br>`param chunk_size` int, size of each chunk in bytes (default 8192)
        <br>`param mode` string, read mode - "rb" for binary, "r" for text
        <br>`return` generator yielding chunks
        """
        if mode == "r":
            encoding = cls.get_encoding(path)
            with open(path, mode, encoding=encoding) as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        else:
            with open(path, mode) as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

    @classmethod
    def read_by_line(
        cls,
        path: str,
        encoding: str = "utf-8",
        auto_detect_encoding: Union[bool, int] = True,
        strip_newline: bool = True
    ) -> Iterator[str]:
        r"""Generate lines from a file.

        <br>`param path` path to file
        <br>`param encoding` string, encoding to use (default "utf-8")
        <br>`param auto_detect_encoding` how much symbols use to auto define decoding, if True, uses 10000
        <br>`param strip_newline` boolean, if True removes \\n from end of lines
        <br>`return` generator yielding lines
        """
        if auto_detect_encoding:
            encoding = cls.get_encoding(path, count_of_symbols=auto_detect_encoding)

        try:
            with open(path, "r", encoding=encoding) as file:
                for line in file:
                    if strip_newline:
                        yield line.rstrip('\n\r')
                    else:
                        yield line
        except LookupError:
            if encoding.lower() == "EUC-TW".lower():
                with open(path, "r", encoding="TIS-620") as file:
                    for line in file:
                        if strip_newline:
                            yield line.rstrip('\n\r')
                        else:
                            yield line

    @classmethod
    def exist(cls, filename: str) -> bool:
        """Return True if a file exists.

        <br>`param filename` string with path to file
        <br>`return` boolean that means existence of file
        """
        return os.path.isfile(filename)

    @classmethod
    def format_size_human_readable(cls, size_in_bytes: int) -> str:
        """Return a human-readable string for a byte size."""
        size_string = f" {str(int(size_in_bytes % KiB))}b"

        if size_in_bytes < KiB:
            return size_string.strip()

        size_string = size_string.strip().zfill(4)
        size_string = " " + size_string
        size_string = f" {str(int(size_in_bytes / KiB % 1024))}KiB" + size_string

        if size_in_bytes < MiB:
            return size_string.strip()

        size_string = size_string.strip().zfill(11)
        size_string = " " + size_string
        size_string = f" {str(int(size_in_bytes / MiB % 1024))}MiB" + size_string

        if size_in_bytes < GiB:
            return size_string.strip()

        size_string = size_string.strip().zfill(18)
        size_string = " " + size_string
        size_string = f" {str(int(size_in_bytes / GiB % 1024))}GiB" + size_string

        if size_in_bytes < TiB:
            return size_string.strip()

        size_string = size_string.strip().zfill(25)
        size_string = " " + size_string
        size_string = f" {str(int(size_in_bytes / TiB))}TiB" + size_string

        return size_string.strip()

    @classmethod
    def get_size(cls, filename: str, human_readable: bool = False) -> Union[int, str]:
        """Return file size, optionally formatted.

        <br>`param filename` string with path to file
        <br>`return` int with file size in bytes
        """
        size_in_bytes = os.stat(filename).st_size
        if not human_readable:
            return size_in_bytes

        return cls.format_size_human_readable(size_in_bytes=size_in_bytes)

    @classmethod
    def get_modification_time(cls, filename: str) -> float:
        """Return file modification time.

        <br>`param filename` string, path to file
        <br>`return` float,
        """
        return os.path.getmtime(filename)

    @classmethod
    def get_extension(cls, filepath: str) -> str:
        """Return a file extension for a path."""
        filename, file_extension = os.path.splitext(filepath)
        return file_extension

    @classmethod
    def sha256_checksum(cls, filename: str, block_size: int = 65536) -> str:
        """Return SHA-256 checksum for a file."""
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    @classmethod
    def get_mime(cls, path: str) -> str:
        """Return MIME type of a file."""
        path = str(path)
        magic = winmagic.magic if OS.windows else globals()["magic"]
        try:
            return str(magic.from_file(path, mime=True))
        except OSError:
            return "unknown"

    @classmethod
    def set_modification_time(cls, filepath: str, datetime: Any) -> None:
        """Set file modification time from a datetime."""
        mod_time = time.mktime(datetime.timetuple())

        os.utime(filepath, (mod_time, mod_time))

    all_encodings = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737',
                     'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863',
                     'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006',
                     'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256',
                     'cp1257', 'cp1258', 'cp65001', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk',
                     'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3',
                     'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
                     'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13',
                     'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048',
                     'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154',
                     'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16',
                     'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']
