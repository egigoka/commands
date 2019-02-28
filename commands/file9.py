#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with files
"""
__version__ = "1.0.1"
# pylint: disable=c-extension-no-member


class File:
    """Class to work with files
    """
    @classmethod
    def create(cls, filename, quiet=True):
        """Creates subdirs, if needed
        :param filename: string with path to creating file
        :param quiet: boolean, if True, suppress output to console
        :return: None
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
    def delete(cls, path, quiet=False, no_sleep=False):
        """
        :param path: string with path to deleting file
        :param quiet: boolean, suppress print to console
        :param no_sleep: boolean, if True - function skip sleep in 0.05 seconds after deleting file (to ensure than file
        deleted before next code run)
        :return: None
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

    @staticmethod
    def move(input_file, output_file):
        """
        :param input_file: string with path to previous file place
        :param output_file: string with path to new file place
        :return: None
        """
        import shutil
        shutil.move(input_file, output_file)
        return output_file

    @staticmethod
    def copy(input_file, output_file):
        """
        :param input_file: string with path to existing file
        :param output_file: string with path to new file
        :return: None
        """
        import shutil
        shutil.copy2(input_file, output_file)

    @classmethod
    def rename(cls, input_file, output_file):
        """
        :param input_file: string with path to previous file place
        :param output_file: string with path to new file place
        :return: string with path to new file place
        """
        return cls.move(input_file, output_file)

    @classmethod
    def hide(cls, filename, quiet=True):
        """Adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
        file, if running on Windows
        :param filename: string with path to file
        :param quiet: suppress print to console
        :return: string with new filename
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
            dotted_file = Path.extend(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
            filename = cls.rename(filename, dotted_file)  # adding dot
        else:
            raise NotImplementedError("Your OS doesn't supported")
        if not quiet:
            print("file", filename, "is hidden now")
        return filename

    @classmethod
    def backup(cls, filename, subfolder="bak", hide=True, quiet=False):
        """Move file to subfolder, adds sort of timestamp to filename and hide file if 'hide' argument is True
        :param filename: string with path to file
        :param subfolder: string with name of subfolder of backed up files
        :param hide: boolean, define hide file or not
        :param quiet: boolean, suppress print to console
        :return:
        """
        import os
        import shutil
        from .path9 import Path
        from .dir9 import Dir
        from .time9 import Time
        filename = Path.full(filename)  # normalize filename
        backup_filename = str(filename) + "." + Time.dotted() + ".bak"  # add dotted time to backup filename
        backup_filename = os.path.split(backup_filename)  # splitting filename to folder and file
        try:  # if subfolder has no len
            if len(subfolder) < 1:  # if subfolder has zero len
                raise TypeError("subfolder must have non-zero len")
        except TypeError:  # if subfolder has no len
            subfolder = "bak"  # set subfolder to default
            print("len(subfolder) < 1, so subfolder = 'bak'")  # print error
        subfolder = Path.extend(backup_filename[0], subfolder)  # append subfolder name
        Dir.create(subfolder)  # create subfolder
        backup_filename = Path.extend(subfolder, backup_filename[1])  # backup file name full path
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
        :param path: string with path to file
        :return: None
        """
        file = open(path, 'w')
        file.close()

    @staticmethod
    def read(path, encoding="utf-8", auto_detect_encoding=False, quiet=True):  # return pipe to file content
        """
        :param path: string, with path to file
        :param auto_detect_encoding: bool or int, how much symbols use to auto define decoding, if True, uses 10000
        :param quiet: bool, if True, suppress output to console
        :return: pipe, to file text content with utf-8 decoding
        """
        try:
            if auto_detect_encoding:
                if not quiet:
                    from .bench9 import Bench
                    define_encoding_bench = Bench()
                count_of_symbols = auto_detect_encoding
                if auto_detect_encoding is True:  # you can define how much symbols use to define encoding
                    count_of_symbols = 10000
                with open(path, "rb") as rawfile:
                    slice_of_raw_data = rawfile.read(count_of_symbols)
                # check for utf-16-le
                fail_symbols = 0
                for cnt, sym in enumerate(slice_of_raw_data):
                    if cnt % 2 != 0:
                        if sym != 0:
                            fail_symbols += 1
                utf_16_le = False
                if fail_symbols/(len(slice_of_raw_data)/2) < 0.99:
                    utf_16_le = True
                if utf_16_le:
                    encoding = "utf-16-le"
                    if not quiet:
                        define_encoding_bench.end(f"encoding defined by egigoka: [{encoding}] by [{count_of_symbols}] first symbols in")
                # end check for utf-16-le
                else:
                    import chardet
                    encoding = chardet.detect(slice_of_raw_data)["encoding"]
                    if not quiet:
                        define_encoding_bench.end(f"encoding defined by chardet: [{encoding}] by [{count_of_symbols}] first symbols in")
            with open(path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            import codecs
            with codecs.open(path, encoding='cp1251', errors='replace') as file:
                content = file.read()
                file.close()
                return content

    @staticmethod
    def write(filename, what_to_write, mode="a", quiet=True):
        """Write to end of file if "mode" arg isn't redefined
        :param filename: string with path to file
        :param what_to_write: string to write
        :param mode: string with any mode that supported by python open() func
        :param quiet: boolean, if True, suppress output to console
        :return: None
        """
        if not quiet:
            print(f"Writing to file {filename}")
        if "b" not in mode and isinstance(what_to_write, str):
            with open(filename, mode=mode+"b") as file:  # open file then closes it
                file.write(what_to_write.encode("utf-8"))
        else:
            with open(filename, mode=mode) as file:  # open file then closes it
                file.write(what_to_write)
        if not quiet:
            print(f"Writed to file {filename}")

    @staticmethod
    def exist(filename):
        """
        :param filename: string with path to file
        :return: boolean that means existence of file
        """
        import os
        return os.path.isfile(filename)

    @staticmethod
    def get_size(filename):  # return size in bytes
        """
        :param filename: string with path to file
        :return: int with filesize in bytes
        """
        import os
        return os.stat(filename).st_size

    @staticmethod
    def get_modification_time(filename):
        """
        :param filename: string, path to file
        :return: float,
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

