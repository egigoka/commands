#! python3
# -*- coding: utf-8 -*-
from typing import Union
"""Internal module to work with files
"""
__version__ = "1.5.1"
# pylint: disable=c-extension-no-member


class File:
    """Class to work with files
    """
    @classmethod
    def create(cls, filename, quiet=True):
        """Creates subdirectories, if needed
        <br>`param filename` string with path to creating file
        <br>`param quiet` boolean, if True, suppress output to console
        <br>`return` None
        """
        import os
        from .path9 import Path
        from .dir9 import Dir
        if not isinstance(quiet, bool):
            raise TypeError("argument 'quiet' must be boolean")
        filename = Path.full(filename)
        if os.path.split(filename)[0] != "":
            Dir.create(os.path.split(filename)[0])
        if not quiet:
            print(f"Creating file {filename}")
        if not cls.exist(filename):
            with open(filename, 'a'):  # open file and close after
                os.utime(filename, None)  # change time of file modification
        else:
            raise FileExistsError("file " + str(filename) + " exist")
        if not cls.exist(filename):
            import sys
            raise FileNotFoundError("error while creating file " + filename +
                                    "try to repair script at " + Path.full(sys.argv[0]))
        elif not quiet:
            print(f"File {filename} created")

    @classmethod
    def delete(cls, path, quiet=True, no_sleep=False):
        """
        <br>`param path` string with path to deleting file
        <br>`param quiet` boolean, suppress print to console
        <br>`param no_sleep` boolean, if True - function skip sleep in 0.05 seconds after deleting file
        (to ensure than file
        deleted before next code run)
        <br>`return` None
        """
        import time
        import os
        if os.path.isdir(path):
            raise IsADirectoryError(path + " is directory, use Dir.delete to delete")
        try:
            os.remove(path)
        except FileNotFoundError:
            if not quiet:
                print("file", path, "is not exist")
        if not quiet:
            print("file", path, "is deleted")
        if not no_sleep:
            time.sleep(0.05)
            if cls.exist(path):
                raise FileExistsError(path + " is not deleted")

    @classmethod
    def move(cls, input_file, output_file):
        """
        <br>`param input_file` string with path to previous file place
        <br>`param output_file` string with path to new file place
        <br>`return` None
        """
        import shutil
        if cls.exist(input_file):
            return shutil.move(input_file, output_file)
        raise FileNotFoundError(f"When trying to move/rename file '{input_file}'>'{output_file}': "
                                f"File '{input_file}' not found")

    @staticmethod
    def copy(input_file, output_file):
        """
        <br>`param input_file` string with path to existing file
        <br>`param output_file` string with path to new file
        <br>`return` None
        """
        import shutil
        shutil.copy2(input_file, output_file)

    @classmethod
    def rename(cls, input_file, output_file):
        """
        <br>`param input_file` string with path to previous file place
        <br>`param output_file` string with path to new file place
        <br>`return` string with path to new file place
        """
        return cls.move(input_file, output_file)

    @classmethod
    def hide(cls, filename, quiet=True):
        """Adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
        file, if running on Windows
        <br>`param filename` string with path to file
        <br>`param quiet` suppress print to console
        <br>`return` string with new filename
        """
        import os
        from .path9 import Path
        from .os9 import OS
        filename = Path.full(filename)
        if OS.windows:
            import win32api
            import win32con
            win32api.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN)  # hiding file like windows do
        elif OS.unix_family:
            dotted_file = Path.combine(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
            filename = cls.rename(filename, dotted_file)  # adding dot
        else:
            raise NotImplementedError("Your OS doesn't supported")
        if not quiet:
            print("file", filename, "is hidden now")
        return filename

    @classmethod
    def backup(cls, filename, subdirectory="bak", hide=True, quiet=False):
        """Move file to subdirectory, adds sort of timestamp to filename and hide file if 'hide' argument is True
        <br>`param filename` string with path to file
        <br>`param subdirectory` string with name of subdirectory of backed up files
        <br>`param hide` boolean, define hide file or not
        <br>`param quiet` boolean, suppress print to console
        <br>`return`
        """
        import os
        import shutil
        from .path9 import Path
        from .dir9 import Dir
        from .time9 import Time
        filename = Path.full(filename)  # normalize filename
        backup_filename = str(filename) + "." + Time.dotted() + ".bak"  # add dotted time to back up filename
        backup_filename = os.path.split(backup_filename)  # splitting filename to folder and file
        try:  # if subdirectory has no len
            if len(subdirectory) < 1:  # if subdirectory has zero len
                raise TypeError("subdirectory must have non-zero len")
        except TypeError:  # if subdirectory has no len
            subdirectory = "bak"  # set subdirectory to default
            print("len(subdirectory) < 1, so subdirectory = 'bak'")  # print error
        subdirectory = Path.combine(backup_filename[0], subdirectory)  # append subdirectory name
        Dir.create(subdirectory)  # create subdirectory
        backup_filename = Path.combine(subdirectory, backup_filename[1])  # backup file name full path
        shutil.copy2(filename, backup_filename)  # finally backup file
        if hide:
            backup_filename = cls.hide(backup_filename)  # hiding file
        if not os.path.isfile(backup_filename):  # if file is not created
            raise FileNotFoundError(backup_filename + " isn't created while backup")
        if not quiet:
            print("backup of file", filename, "created as", backup_filename)  # all is ok, print that
        return backup_filename

    @staticmethod
    def wipe(path):
        """Erase content of file
        <br>`param path` string with path to file
        <br>`return` None
        """
        file = open(path, 'w')
        file.close()

    @staticmethod
    def get_encoding(path, count_of_symbols: Union[bool, int] = True):
        """
        <br>`param path` path to file
        <br>`param count_of_symbols` how much symbols use to auto define decoding, if True, uses 10000
        <br>`return` string, file encoding
        """
        from .bytes9 import Bytes
        count_of_symbols = count_of_symbols
        if count_of_symbols is True:  # you can define how much symbols use to define encoding
            count_of_symbols = 10000
        with open(path, "rb") as raw_file:
            slice_of_raw_data = raw_file.read(count_of_symbols)
        encoding = Bytes.get_encoding(slice_of_raw_data)
        return encoding

    @classmethod
    def read(cls, path, encoding: str = "utf-8", auto_detect_encoding: Union[bool, int] = True, mode: str = "r"):
        # return pipe to file content
        """
        <br>`param path` path to file
        <br>`param auto_detect_encoding` how much symbols use to auto define decoding, if True, uses 10000
        <br>`return` pipe, to file text content with utf-8 decoding
        """
        if mode == "r":
            try:
                if auto_detect_encoding:
                    encoding = cls.get_encoding(path, count_of_symbols=auto_detect_encoding)
                with open(path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                import codecs
                with codecs.open(path, encoding='cp1251', errors='replace') as file:
                    content = file.read()
                    return content
        elif mode in ["b", "rb"]:
            with open(path, "rb") as file:
                content = file.read()
                return content

    @staticmethod
    def write(filename, what_to_write, mode="a", encoding="utf-8", quiet=True):
        """Write to end of file if "mode" arg isn't redefined
        <br>`param filename` string with path to file
        <br>`param what_to_write` string to write
        <br>`param mode` string with any mode that supported by python open() func
        <br>`param encoding` string with any encoding
        <br>`param quiet` boolean, if True, suppress output to console
        <br>`return` None
        """
        if not quiet:
            print(f"Writing to file {filename}")
        if "b" not in mode and isinstance(what_to_write, str):
            with open(filename, mode=mode+"b") as file:  # open file then closes it
                file.write(what_to_write.encode(encoding))
        else:
            with open(filename, mode=mode) as file:  # open file then closes it
                if isinstance(what_to_write, int):
                    what_to_write = str(what_to_write)
                file.write(what_to_write)
        if not quiet:
            print(f"Written to file {filename}")

    @staticmethod
    def exist(filename):
        """
        <br>`param filename` string with path to file
        <br>`return` boolean that means existence of file
        """
        import os
        return os.path.isfile(filename)

    @staticmethod
    def get_size(filename, human_readable=False):  # return size in bytes
        """
        <br>`param filename` string with path to file
        <br>`return` int with file size in bytes
        """
        import os
        from .const9 import KiB, MiB, GiB, TiB
        size_in_bytes = os.stat(filename).st_size
        if not human_readable:
            return size_in_bytes

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

    @staticmethod
    def get_modification_time(filename):
        """
        <br>`param filename` string, path to file
        <br>`return` float,
        """
        import os
        return os.path.getmtime(filename)

    @staticmethod
    def get_extension(filepath):
        import os
        filename, file_extension = os.path.splitext(filepath)
        return file_extension

    @staticmethod
    def sha256_checksum(filename, block_size=65536):
        import hashlib
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def get_mime(path):
        from .os9 import OS
        if OS.windows:
            from winmagic import magic
        else:
            import magic
        try:
            return magic.from_file(path, mime=True)
        except OSError:
            from .console9 import Console
            from .path9 import Path
            out = Console.get_output(Path.combine(Path.commands(), "res", "file.exe"), "-i", path)
            try:
                return out.split("; ")[1]
            except IndexError:
                return "unknown"

    @staticmethod
    def set_modification_time(filepath, datetime):
        import time
        import os

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
