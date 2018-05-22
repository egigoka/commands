#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Dir:
    @staticmethod
    def create(filename):  # create dir if didn't exist
        import os
        if not os.path.exists(filename):
            os.makedirs(filename)

    @staticmethod
    def commands8():
        from .path8 import Path
        return Path.commands8()  # alias to Path.commands8

    @staticmethod
    def working():
        from .path8 import Path
        return Path.working()  # alias to Path.working

    @staticmethod
    def list_of_files(path):  # return list of files in folder
        import os
        return os.listdir(path)

    @staticmethod
    def number_of_files(path, quiet=False):
        """Return integer of number of files in directory
        """
        import os
        try:
            dir_contents = Dir.contents(path)
            if not quiet:
                print(os.path.split(path)[1], "contain", len(dir_contents), "files")
            return len(dir_contents)
        except FileNotFoundError:
            if not quiet:
                print("Path", path, "isn't found")
            return None

    @classmethod
    def batch_rename(cls, directory, input_str, output_str, quiet=False):
        for filename in cls.contain(directory):
            if input_str in filename:
                from .file8 import File
                final_name = filename.replace(input_str, output_str)
                File.rename(filename, final_name)
                if not quiet:
                    print(filename, "renamed to", final_name)