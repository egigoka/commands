#! python3
# -*- coding: utf-8 -*-
"""Internal module to write files
"""
__version__ = "2.0.0"


class Codegen:
    """Class for write files
    """
    def __init__(self, file_path, debug=False):
        """Define path of file and wipes it
        :param file_path: string with path of file
        :return:
        """
        from .file9 import File
        File.wipe(file_path)
        self.file_path = file_path

        self.debug = debug

        from .const9 import newline
        self.shebang = "#! python3" + newline + \
                       "# -*- coding: utf-8 -*-" + newline

    def add_line(self, some_string):
        """Write arg string to file
        :param some_string: string that will be wrote to file
        :return: None
        """
        with open(self.file_path, "ab") as file:
            file.write(some_string.encode('utf8'))
        if self.debug:
            print(some_string)


