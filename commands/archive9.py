#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with zip and tar.lzma archives
"""
# https://code.tutsplus.com/ru/tutorials/compressing-and-extracting-files-in-python--cms-26816
__version__ = "0.5.2"


class UniversalArchive:
    def __init__(self, archive_file, mode, archive_type):
        self.archive_file = archive_file
        self.mode = mode
        self.archive_type = archive_type

        if archive_type == Archive.MODE_ZIPDEFLATED:
            import zipfile
            self._real_archive_object = zipfile.ZipFile(archive_file, mode=mode)
        # https://www.tutorialspoint.com/read-and-write-tar-archive-files-using-python-tarfile
        elif archive_type == Archive.MODE_TARLZMA:
            import tarfile
            self._real_archive_object = tarfile.open(archive_file, mode=f"{mode}:xz")
        elif archive_type == Archive.MODE_TARGZ:
            if mode not in ("r", "w", "x"):
                raise ValueError("mode must be 'r', 'w' or 'x'")
            import tarfile
            self._real_archive_object = tarfile.open(archive_file, mode=f"{mode}:gz")

    def write(self, input_file, arcname=None):
        additional_args = {}
        if self.archive_type == Archive.MODE_ZIPDEFLATED:
            import zipfile
            additional_args["compress_type"] = zipfile.ZIP_DEFLATED
        elif self.archive_type in (Archive.MODE_TARLZMA, Archive.MODE_TARGZ):
            self._real_archive_object.write = self._real_archive_object.add
        return self._real_archive_object.write(input_file, arcname=arcname, **additional_args)

    def extract(self, *args, **kwargs):
        return self._real_archive_object.extract(*args, **kwargs)

    def extractall(self, *args, **kwargs):
        return self._real_archive_object.extractall(*args, **kwargs)

    def close(self):
        return self._real_archive_object.close()


class Archive:
    MODE_ZIPDEFLATED = 1
    MODE_TARLZMA = 2
    MODE_TARGZ = 3

    @staticmethod
    def file(input_file, archive_file, arcname=None, mode="a", archive_type=MODE_ZIPDEFLATED):
        from .file9 import File

        if not File.exist(input_file):
            raise IOError(input_file + " is not file")

        if not File.exist(archive_file) and "w" not in mode:
            temp_file = archive_file + ".tmp"
            File.delete(temp_file, quiet=True)

            archive = UniversalArchive(temp_file, mode=mode, archive_type=archive_type)
            archive.write(input_file, arcname=arcname)
            archive.close()

            File.move(temp_file, archive_file)

        else:
            archive = UniversalArchive(archive_file, mode=mode, archive_type=archive_type)
            archive.write(input_file, arcname=arcname)
            archive.close()

    @staticmethod
    def dir(input_dir, archive_file, quiet=True, archive_type=MODE_ZIPDEFLATED):
        import os
        from .file9 import File
        from .dir9 import Dir

        if not Dir.exist(input_dir):
            raise IOError(input_dir + " is not dir")

        temp_file = archive_file + ".tmp"
        File.delete(temp_file, quiet=True)

        archive = UniversalArchive(temp_file, 'w', archive_type=archive_type)
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                archive.write(file_path, os.path.relpath(os.path.join(root, file), input_dir))
                if not quiet:
                    from .print9 import Print
                    from .cli9 import CLI
                    Print.rewrite(CLI.wait_update(quiet=True), file_path, "archived")

        archive.close()
        File.move(temp_file, archive_file)


class Unarchive:
    @staticmethod
    def all(archive_path, output_dir, archive_type=Archive.MODE_ZIPDEFLATED):
        archive = UniversalArchive(archive_path, mode="r", archive_type=archive_type)
        archive.extractall(output_dir)
        archive.close()

    @staticmethod
    def single(archive_path, path_inside_archive, output_path, archive_type=Archive.MODE_ZIPDEFLATED):
        """
        archive_path : path1 to archive for extracting
        path_inside_archive : Full name of file to be extracted.
        output_path : location where file need to be extracted,
        if not provided it will extract the file in current directory.
        :return: None"""
        from .path9 import Path
        from .file9 import File

        archive = UniversalArchive(archive_path, mode="r", archive_type=archive_type)
        temp_path = archive.extract(path_inside_archive, Path.temp())
        archive.close()

        File.move(temp_path, output_path)


