#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with zip archives
"""
# https://code.tutsplus.com/ru/tutorials/compressing-and-extracting-files-in-python--cms-26816
__version__ = "0.3.0"


class Zip:
    @staticmethod
    def file(input_file, output_zip, arcname=None, mode="w"):
        import zipfile
        import os

        if not os.path.isfile(input_file):
            raise IOError(input_file + " is not file")

        with zipfile.ZipFile(output_zip, mode=mode) as zip:
            zip.write(input_file, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)

    @staticmethod
    def dir(input_dir, output_zip, quiet=True):
        import os
        import zipfile

        if not os.path.isdir(input_dir):
            raise IOError(input_dir + " is not dir")

        temp_zip = zipfile.ZipFile(output_zip, 'w')
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                temp_zip.write(file_path, os.path.relpath(os.path.join(root, file), input_dir),
                               compress_type=zipfile.ZIP_DEFLATED)
                if not quiet:
                    from .print9 import Print
                    from .cli9 import CLI
                    Print.rewrite(CLI.wait_update(quiet=True), file_path, "zipped")

        temp_zip.close()


class Unzip:
    @staticmethod
    def all(input_zip, output_dir):
        import zipfile

        temp_zip = zipfile.ZipFile(input_zip)
        temp_zip.extractall(output_dir)

        temp_zip.close()

    @staticmethod
    def single(input_zip, path_inside_zip, output_path):
        '''https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
        input_zip : path to zip for extracting
        path_inside_zip : Full name of file to be extracted. It should one from the list of archived files names returned by ZipFile.namelist()
        output_path : location where zip file need to be extracted, if not provided it will extract the file in current directory.
        :return: None'''
        import zipfile
        from .path9 import Path
        from .file9 import File

        temp_zip = zipfile.ZipFile(input_zip)
        temp_path = temp_zip.extract(path_inside_zip, Path.temp())  # why I only can unzip to folder with original name?
        temp_zip.close()

        File.move(temp_path, output_path)


