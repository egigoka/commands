#! python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"


class Base65536:
    @staticmethod
    def b65kencode(input):
        import base65536
        bytes = input.encode()
        b65k = base65536.encode(bytes)
        return b65k
    @staticmethod
    def b65kdecode(input):
        import base65536
        bytes = base65536.decode(input)
        string = bytes.decode()
        return string

    @classmethod
    def to_file(cls, string, file_path):
        from .file9 import File
        encoded = cls.b65kencode(string)
        File.write(file_path, encoded)

    @classmethod
    def from_file(cls, file_path):
        from .file9 import File
        encoded = File.read(file_path)
        decoded = cls.b65kdecode(encoded)
        return encoded