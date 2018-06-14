#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with directories
"""
__version__ = "0.3.0"


class Dir:
    """Class to work with directories
    """
    @staticmethod
    def create(dirname):
        """Creates dir if it doesn't exist
        :param dirname: string with path to new dir
        :return:
        """
        import os
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    @staticmethod
    def commands():
        """Used to store configs(?)
        :return: path to this module
        """
        from .path8 import Path
        return Path.commands8()

    @staticmethod
    def working():
        """
        :return: string with working directory
        """
        from .path8 import Path
        return Path.working()

    @staticmethod
    def list_of_files(path):
        """
        :param path: string with path to folder
        :return: list of files in folder
        """
        import os
        return os.listdir(path)

    @classmethod
    def number_of_files(cls, path, quiet=False):
        """
        :param path: string with paht
        :param quiet: suppress print to console
        :return: int count of files in directory
        """
        import os
        try:
            dir_contents = cls.list_of_files(path)
            if not quiet:
                print(os.path.split(path)[1], "contain", len(dir_contents), "files")
            return len(dir_contents)
        except FileNotFoundError:
            if not quiet:
                print("Path", path, "isn't found")
            return None

    @classmethod
    def batch_rename(cls, directory, previous_name_substring, new_name_substring, quiet=False):
        """Batch renames files in directory.
        :param directory: string with path to directory
        :param previous_name_substring: string that must be changed in every file
        :param new_name_substring: string to that will be changed 'input_str'
        :param quiet: suppress print to console
        :return:
        """
        for filename in cls.list_of_files(directory):
            if previous_name_substring in filename:
                from .file8 import File
                final_name = filename.replace(previous_name_substring, new_name_substring)
                File.rename(filename, final_name)
                if not quiet:
                    print(filename, "renamed to", final_name)

    @staticmethod
    def delete(directory):
        """Removes all content in directory
        :param directory: string with path to directory
        """
        import os
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
