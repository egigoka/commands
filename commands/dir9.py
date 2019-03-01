#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with directories
"""
__version__ = "1.0.0"


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
    def number_of_files(cls, path, quiet=True):
        """
        :param path: string with paht
        :param quiet: suppress print to console
        :return: int count of files in directory
        """
        import os
        dir_contents = cls.list_of_files(path)
        if not quiet:
            print(os.path.split(path)[1], "contain", len(dir_contents), "files")
        return len(dir_contents)

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
                from .file9 import File
                final_name = filename.replace(previous_name_substring, new_name_substring)
                File.rename(filename, final_name)
                if not quiet:
                    print(filename, "renamed to", final_name)

    @classmethod
    def delete(cls, path, cleanup=False, remove_readonly=True, no_sleep=False, 
               skip_PermissionError=False, quiet_PermissionError=False):
        """Remove directory
        :param path: string
        :param cleanup: boolean, True doesn't delete "path" folder, only content
        :param skip_PermissionError: boolean, if True, skips files with denied permissions to read|write
        :param quiet_PermissionError: boolean, suppress console output when skip file by PermissionError
        :return: None
        """
        import os
        if quiet_PermissionError:
            skip_PermissionError = True
        for root, dirs, files in os.walk(path):  # , topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if remove_readonly:
                    try:
                        os.remove(os.path.join(root, name))  # unsafe
                    except PermissionError:
                        # let's just assume that it's read-only and chmod it.
                        import stat
                        if not skip_PermissionError:
                            os.chmod(file_path, stat.S_IWRITE)
                            os.remove(file_path)
                        else:
                            try:
                                os.chmod(file_path, stat.S_IWRITE)
                                os.remove(file_path)
                            except PermissionError as err:
                                if not quiet_PermissionError:
                                    print(err)
                else:
                    if not skip_PermissionError:
                        os.remove(file_path)  # unsafe
                    else:
                        try:
                            os.remove(file_path)  # unsafe
                        except PermissionError as err:
                            if not quiet_PermissionError:
                                print(err)
            for name in dirs:
                cls.delete(os.path.join(root, name))  # recursion
        if not cleanup:
            try:
                
                os.rmdir(path)  # unsafe
            except OSError:
                if not no_sleep:
                    import time
                    time.sleep(0.05)
                os.rmdir(path)  # unsafe


    @classmethod
    def cleanup(cls, path, skip_PermissionError=False, quiet_PermissionError=False):
        """Removes all content in directory
        :param path: string
        :param skip_PermissionError: boolean, if True, skips files with denied permissions to read|write
        :param quiet_PermissionError: boolean, suppress console output when skip file by PermissionError
        :return: None
        """
        if quiet_PermissionError:
            skip_PermissionError = True
        cls.delete(path, cleanup=True, 
                   skip_PermissionError=skip_PermissionError, quiet_PermissionError=quiet_PermissionError)

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
        if quiet_PermissionError:
            skip_PermissionError = True
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
             skip_PermissionError=False, quiet_PermissionError=False):
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
        if quiet_PermissionError:
            skip_PermissionError = True
        cls.copy(src=src_, dst=dst_, symlinks=symlinks_, ignore=ignore_,
                 skip_PermissionError=skip_PermissionError,
                 quiet_PermissionError=quiet_PermissionError)
        cls.delete(src_)

    @staticmethod
    def exist(filename):
        """
        :param filename: string with path to dir
        :return: boolean that means existence of dir
        """
        import os
        return os.path.isdir(filename)
