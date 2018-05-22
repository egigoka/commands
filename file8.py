#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class File:
    @staticmethod
    def create(filename):
        import os
        from .path8 import Path
        from .dir8 import Dir
        filename = Path.full(filename)
        if os.path.split(filename)[0] != "":
            Dir.create(os.path.split(filename)[0])
        if not File.exists(filename):
            with open(filename, 'a'):  # open file and close after
                os.utime(filename, None)  # change time of file modification
        else:
            raise FileExistsError("file" + str(filename) + "exists")
        if not File.exists(filename):
            import sys
            raise FileNotFoundError("error while creating file " + filename +
                                    "try to repair script at " + Path.full(sys.argv[0]))

    @staticmethod
    def delete(path, quiet=False):  # ...
        import time, os
        if os.path.isdir(path):
            raise IsADirectoryError(path + " is directory, use Dir.delete to delete")
        try:
            os.remove(path)
        except FileNotFoundError:
            if not quiet:
                print("file", path, "is not exist")
        if not quiet:
            print("file", path, "is deleted")
        time.sleep(0.05)
        if File.exists(path):
            raise FileExistsError(path + " is not deleted")

    @staticmethod
    def move(input_file, output_file):  # ...
        import shutil
        shutil.move(input_file, output_file)

    @staticmethod
    def copy(input_file, output_file):  # ...
        import shutil
        shutil.copy2(input_file, output_file)

    @staticmethod
    def rename(input_file, output_file):  # ...
        File.move(input_file, output_file)

    @staticmethod
    def hide(filename, quiet=True):
        """adding dot to filename and set attribute FILE_ATTRIBUTE_HIDDEN to
        file, if running on Windows"""
        import os
        from .path8 import Path
        from .os8 import OS
        filename = Path.full(filename)
        if OS.windows:
            import win32api, win32con
            win32api.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN)  # hiding file like windows do
        dotted_file = Path.extend(os.path.split(filename)[0], "." + os.path.split(filename)[1])  # adding dot
        File.rename(filename, dotted_file)
        if not quiet:
            print("file", filename, "is hidden now")
        return dotted_file

    @classmethod
    def backup(cls, filename, subfolder="bak", hide=True, quiet=False):
        """Move file to subfolder, adds sort of timestamp to filename and
        hide file if same named argument is True
        """
        import os
        import shutil
        from .path8 import Path
        from .dir8 import Dir
        filename = Path.full(filename)  # normalize filename
        backupfilename = str(filename) + "." + Time.dotted() + ".bak"  # add dottedtime to backup filename
        backupfilename = os.path.split(backupfilename)  # splitting filename to folder and file
        try:  # if subfolder has no len
            if len(subfolder) < 1:  # if subfolder has zero len
                raise TypeError("subfolder must have non-zero len")
        except TypeError:  # if subfolder has no len
            subfolder = "bak"  # set subfolder to default
            print("len(subfolder) < 1, so subfolder = 'bak'")  # print error
        subfolder = Path.extend(backupfilename[0], subfolder)  # append subfolder name
        Dir.create(subfolder)  # create subfolder
        backupfilename = Path.extend(subfolder, backupfilename[1])  # backup file name full path
        shutil.copy2(filename, backupfilename)  # finally backup file
        if hide:
            backupfilename = cls.hide(backupfilename)  # hiding file
        if not os.path.isfile(backupfilename):  # if file is not created
            raise FileNotFoundError(backupfilename + " isn't created while backup")
        if not quiet:  # if finction is not shutted up
            print("backup of file", filename, "created as", backupfilename)  # all is ok, print that
        return backupfilename

    @staticmethod
    def wipe(path):  # clean content of file
        file = open(path, 'w')
        file.close()

    @staticmethod
    def read(path):  # return pipe to file content
        with open(path, "r", encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write(filename, what_to_write, mode="ab"):
        """write to end of file with default mode, you can change it to any
        that supported by python open() func"""
        with open(filename, mode=mode) as file:  # open file then closes it
            file.write(what_to_write.encode("utf-8"))

    @staticmethod
    def get_size(filename):  # return size in bytes
        import os
        return os.stat(filename).st_size

    @staticmethod
    def exists(filename):
        import os
        return os.path.exists(filename)