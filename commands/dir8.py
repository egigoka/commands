#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with directories
"""
__version__ = "0.9.2"


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
        :return: None
        """
        for filename in cls.list_of_files(directory):
            if previous_name_substring in filename:
                from .file8 import File
                final_name = filename.replace(previous_name_substring, new_name_substring)
                File.rename(filename, final_name)
                if not quiet:
                    print(filename, "renamed to", final_name)

    @classmethod
    def delete(cls, path, cleanup=False):
        """Remove directorye
        :param path: string
        :param cleanup: boolean, True doesn't delete "path" folder, only content
        :return: None
        """
        import os
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                cls.delete(os.path.join(root, name))
        if not cleanup:
            os.removedirs(path)

    @classmethod
    def cleanup(cls, path):
        """Removes all content in directory
        :param path: string
        :return: None
        """
        cls.delete(path, cleanup=True)

    @classmethod
    def copy(cls, src, dst, symlinks=False, ignore=None,
             skip_PermissionError=False, quiet_PermissionError=False):
        """Same behavior as shutil.copytree, but can copy into existing directory
        https://stackoverflow.com/a/22331852/6519078
        :param src: string, source directory to copy
        :param dst: stirng, destination
        :param symlinks: boolean, following symlinks
        :param ignore: You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments: a directory name and the files in it, it
        should return an iterable of ignore files.
        :param skip_PermissionError: boolean, if True, skips files with denied permissions to read|write
        :param quiet_PermissionError: boolean, suppress console output when skip file by PermissionError
        :return: None
        """
        import os
        import shutil
        import stat
        if not os.path.exists(dst):
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
                    os.lchmod(d, mode)
                except:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                cls.copy(s, d, symlinks, ignore, skip_PermissionError, quiet_PermissionError)
            else:
                if not skip_PermissionError:
                    shutil.copy2(s, d)
                else:
                    try:
                        shutil.copy2(s, d)
                    except PermissionError as err:
                        if not quiet_PermissionError:
                            print(err)

    @classmethod
    def move(cls, src_, dst_, symlinks_=False, ignore_=None,
             skip_PermissionError_=False, quiet_PermissionError_=False):
        """Copies folder, than delete source folder
        :param src: string, source directory to copy
        :param dst: stirng, destination
        :param symlinks: boolean, following symlinks
        :param ignore: You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments: a directory name and the files in it, it
        should return an iterable of ignore files.
        :param skip_PermissionError: boolean, if True, skips files with denied permissions to read|write
        :param quiet_PermissionError: boolean, suppress console output when skip file by PermissionError
        :return: None
        """
        cls.copy(src=src_, dst=dst_, symlinks=symlinks_, ignore=ignore_,
                 skip_PermissionError=skip_PermissionError_,
                 quiet_PermissionError=quiet_PermissionError_)
        cls.delete(src_)

    @staticmethod
    def exists(filename):
        """
        :param filename: string with path to file
        :return: boolean that means existence of file
        """
        import os
        return os.path.isdir(filename)
