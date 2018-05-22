#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"


class Codegen:
    debug = False

    @classmethod
    def start(cls, file_path):
        from .file8 import File
        File.wipe(file_path)
        cls.file = open(file_path, "wb")

    @classmethod
    def add_line(cls, code):
        cls.file.write(code.encode('utf8'))
        if cls.debug:
            print(code)

    @classmethod
    def end(cls, quiet=False):
        cls.file.close()

    from .const8 import newline
    shebang = "#! python3" + newline + \
              "# -*- coding: utf-8 -*-" + newline