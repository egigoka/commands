#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with files
"""
__version__ = "0.5.0"
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
        from .path8 import Path
        from .dir8 import Dir
        filename = Path.full(filename)
        if os.path.split(filename)[0] != "":
            Dir.create(os.path.split(filename)[0])
        if not quiet:
            print(f"Creating file {filename}")
        if not cls.exists(filename):
            with open(filename, 'a'):  # open file and close after
                os.utime(filename, None)  # change time of file modification
        else:
            raise FileExistsError("file" + str(filename) + "exists")
        if not cls.exists(filename):
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
            if cls.exists(path):
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
        :return: None
        """
        cls.move(input_file, output_file)

    @classmethod
    def hide(cls, filename, quiet=True):
        """Adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
        file, if running on Windows
        :param filename: string with path to file
        :param quiet: suppress print to console
        :return: string with new filename
        """
        import os
        from .path8 import Path
        from .os8 import OS
        filename = Path.full(filename)
        if OS.windows:
            import win32api
            import win32con
            win32api.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN)  # hiding file like windows do
        dotted_file = Path.extend(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
        cls.rename(filename, dotted_file)
        if not quiet:
            print("file", filename, "is hidden now")
        return dotted_file

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
        from .path8 import Path
        from .dir8 import Dir
        from .time8 import Time
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
    def read(path):  # return pipe to file content
        """
        :param path: string with path to file
        :return: pipe to file text content with utf-8 decoding
        """
        try:
            with open(path, "r", encoding='utf-8') as file:
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
    def get_size(filename):  # return size in bytes
        """
        :param filename: string with path to file
        :return: int with filesize in bytes
        """
        import os
        return os.stat(filename).st_size

    @staticmethod
    def exists(filename):
        """
        :param filename: string with path to file
        :return: boolean that means existence of file
        """
        import os
        return os.path.exists(filename)

    @staticmethod
    def get_modification_time(filename):
        """
        :param filename: string, path to file
        :return: float,
        """
        import os
        return os.path.getmtime(filename)
