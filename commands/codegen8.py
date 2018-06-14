#! python3
# -*- coding: utf-8 -*-
"""Internal module to write files
"""
__version__ = "0.2.0"


class Codegen:
    """Class for write files
    """
    debug = False

    @classmethod
    def start(cls, file_path):
        """Define path of file and wipes it
        :param file_path: string with path of file
        :return:
        """
        from .file8 import File
        File.wipe(file_path)
        cls.file_path = file_path

    @classmethod
    def add_line(cls, some_string):
        """Write arg string to file
        :param some_string: string that will be wrote to file
        :return: None
        """
        with open(cls.file_path, "ab") as file:
            file.write(some_string.encode('utf8'))
        if cls.debug:
            print(some_string)

    from .const8 import newline
    shebang = "#! python3" + newline + \
              "# -*- coding: utf-8 -*-" + newline
