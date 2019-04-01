#! python3
# -*- coding: utf-8 -*-

__version__ = "0.0.2"


class Base65536:
    def to_file(string, file_path):
        import base65536
        from .file9 import File
        decoded = base65536.decode(string)
        File.write(file_path, decoded)

    def from_file(file_path):
        import base65536
        from .file9 import File
        decoded = File.read(file_path)
        encoded = base65536.encode(decoded)
        return encoded