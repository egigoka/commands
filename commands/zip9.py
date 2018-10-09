#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with zip archives
"""
# https://code.tutsplus.com/ru/tutorials/compressing-and-extracting-files-in-python--cms-26816
__version__ = "0.0.1"


class Zip:
    @staticmethod
    def file(input_file, output_zip):
        import zipfile
        import os

        if not os.path.isfile(input_file):
            raise IOError(input_file + " is not file")

        temp_zip = zipfile.ZipFile(output_zip, 'w')
        temp_zip.write(input_file, compress_type=zipfile.ZIP_DEFLATED)

        temp_zip.close()

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
    def single(input_zip, output_dir, output_file):
        import zipfile

        temp_zip = zipfile.ZipFile(input_zip)
        temp_zip.extract(output_dir, output_file)

        temp_zip.close()

