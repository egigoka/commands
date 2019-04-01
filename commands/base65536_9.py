#! python3
# -*- coding: utf-8 -*-

__version__ = "0.0.1"


class Base65536:
    def to_file(bytes_, file_path):
        import base65536
        from .file9 import File
        string = base65536.decode(bytes_)
        File.write(file_path, string)

    def from_file(file_path):
        import base65536
        from .file9 import File
        bytes_ = File.read(file_path, mode='b')
        string = base65536.encode(bytes_)
        return string