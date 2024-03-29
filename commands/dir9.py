#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with directories
"""
__version__ = "1.8.0"


class Dir:
    """Class to work with directories
    """
    @staticmethod
    def create(dir_name):
        """Creates dir if it doesn't exist
        <br>`param dir_name` string with path to new dir
        <br>`return`
        """
        import os
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def list_of_entries(path):
        """
        <br>`param path` string with path to folder
        <br>`return` list of files and folders in path
        """
        import os
        return os.listdir(path)

    @staticmethod
    def list_of_files(path):
        import os
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    @staticmethod
    def list_of_dirs(path):
        import os
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    @classmethod
    def number_of_files(cls, path, quiet=True):
        """
        <br>`param path` string with path
        <br>`param quiet` suppress print to console
        <br>`return` int count of files in directory
        """
        import os
        if not cls.exist(path):
            raise FileNotFoundError(f"Directory '{path}' not found")
        cnt = 0
        for root, dirs, files in os.walk(path):
            cnt += len(files)
        if not quiet:
            print(os.path.split(path)[1], "contain", cnt, "files")
        return cnt

    @classmethod
    def batch_rename(cls, directory, previous_name_substring, new_name_substring, quiet=False):
        """Batch renames files in directory.
        <br>`param directory` string with path to directory
        <br>`param previous_name_substring` string that must be changed in every file
        <br>`param new_name_substring` string to that will be changed 'input_str'
        <br>`param quiet` suppress print to console
        <br>`return` None
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
               skip_permission_error=False, quiet_permission_error=False):
        """Remove directory
        <br>`param path` string
        <br>`param cleanup` boolean, True doesn't delete "path" folder, only content
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        import os
        if quiet_permission_error:
            skip_permission_error = True
        for root, dirs, files in os.walk(path):  # , topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if remove_readonly:
                    try:
                        os.remove(os.path.join(root, name))  # unsafe
                    except PermissionError:
                        # let's just assume that it's read-only and chmod it.
                        import stat
                        if not skip_permission_error:
                            os.chmod(file_path, stat.S_IWRITE)
                            os.remove(file_path)
                        else:
                            try:
                                os.chmod(file_path, stat.S_IWRITE)
                                os.remove(file_path)
                            except PermissionError as err:
                                if not quiet_permission_error:
                                    print(err)
                else:
                    if not skip_permission_error:
                        os.remove(file_path)  # unsafe
                    else:
                        try:
                            os.remove(file_path)  # unsafe
                        except PermissionError as err:
                            if not quiet_permission_error:
                                print(err)
            for name in dirs:
                cls.delete(os.path.join(root, name), cleanup, remove_readonly, no_sleep,
                           skip_permission_error, quiet_permission_error)  # recursion
        if not cleanup:
            try:
                
                os.rmdir(path)  # unsafe
            except OSError:
                if not no_sleep:
                    import time
                    time.sleep(0.05)
                os.rmdir(path)  # unsafe

    @classmethod
    def cleanup(cls, path, skip_permission_error=False, quiet_permission_error=False):
        """Removes all content in directory
        <br>`param path` string
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        cls.delete(path, cleanup=True,
                   skip_permission_error=skip_permission_error, quiet_permission_error=quiet_permission_error)

    @classmethod
    def copy(cls, src, dst, symlinks=False, ignore=None,
             skip_permission_error=False, quiet_permission_error=False,
             skip_file_not_found_error=False, quiet_file_not_found_error=False,
             skip_os_error=False, quiet_os_error=False,
             verbose=False):
        """Same behavior as shutil.copytree, but can copy into existing directory
        https`//stackoverflow.com/a/22331852/6519078
        <br>`param src` string, source directory to copy
        <br>`param dst` string, destination
        <br>`param symlinks` boolean, following symlinks
        <br>`param ignore` You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments` a directory name and the files in it, it
        should return an iterable of ignored files.
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        import os
        import shutil
        import stat
        if quiet_permission_error:
            skip_permission_error = True
        if not os.path.exists(dst):
            if verbose:
                print(f"creating dir {dst}")
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
                except Exception:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                cls.copy(src=s, dst=d, symlinks=symlinks, ignore=ignore,
                         skip_permission_error=skip_permission_error, quiet_permission_error=quiet_permission_error,
                         skip_file_not_found_error=skip_file_not_found_error,
                         quiet_file_not_found_error=quiet_file_not_found_error,
                         skip_os_error=skip_os_error, quiet_os_error=quiet_os_error,
                         verbose=verbose)
            else:
                try:
                    if verbose:
                        print(f"copying {s} to {d}")
                    shutil.copy2(s, d)
                except PermissionError as err:
                    if not quiet_permission_error:
                        print(err)
                    if not skip_permission_error:
                        raise
                except FileNotFoundError as err:
                    if not quiet_file_not_found_error:
                        print(err)
                    if not skip_file_not_found_error:
                        raise
                except OSError as err:
                    if not quiet_os_error:
                        print(err)
                    if not skip_os_error:
                        raise

    @classmethod
    def move(cls, src_, dst_, symlinks_=False, ignore_=None,
             skip_permission_error=False, quiet_permission_error=False, verbose=False):
        """Copies folder, then delete source folder
        <br>`param src` string, source directory to copy
        <br>`param dst` string, destination
        <br>`param symlinks` boolean, following symlinks
        <br>`param ignore` You can define any function with any name you like before calling copytree function. This
        function (which could also be a lambda expression) takes two arguments` a directory name and the files in it, it
        should return an iterable of ignore files.
        <br>`param skip_PermissionError` boolean, if True, skips files with denied permissions to read|write
        <br>`param quiet_PermissionError` boolean, suppress console output when skip file by PermissionError
        <br>`return` None
        """
        if quiet_permission_error:
            skip_permission_error = True
        cls.copy(src=src_, dst=dst_, symlinks=symlinks_, ignore=ignore_,
                 skip_permission_error=skip_permission_error,
                 quiet_permission_error=quiet_permission_error, verbose=verbose)

        cls.delete(src_)

    @staticmethod
    def exist(filename):
        """
        <br>`param filename` string with path to dir
        <br>`return` boolean that means existence of dir
        """
        import os
        return os.path.isdir(filename)

    @classmethod
    def exists(cls, filename):
        return cls.exist(filename=filename)

    @classmethod
    def get_size(cls, path):
        import os
        from .file9 import File
        from .path9 import Path

        if not cls.exist(path):
            raise FileNotFoundError(f"Directory '{path}' not found")

        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = Path.combine(root, file)
                total_size += File.get_size(filepath)
        return total_size

    @staticmethod
    def get_modification_time(path):
        from .file9 import File
        return File.get_modification_time(path)

    @staticmethod
    def get_free_space(path):
        import shutil
        total, used, free = shutil.disk_usage(path)
        return free
