#! python3
# -*- coding: utf-8 -*-

__version__ = "0.1.2"


class Base65536:
    @staticmethod
    def encode(input):
        import base65536
        bytes = input.encode()
        b65k = base65536.encode(bytes)
        return b65k

    @staticmethod
    def decode(input):
        import base65536
        bytes = base65536.decode(input)
        string = bytes.decode()
        return string

    @classmethod
    def to_file(cls, string, file_path):
        from .file9 import File
        decoded = cls.decode(string)
        File.write(file_path, decoded)

    @classmethod
    def from_file(cls, file_path, encoding=None, auto_detect_encoding=True):
        from .file9 import File
        decoded = File.read(file_path, encoding=encoding, auto_detect_encoding=auto_detect_encoding)
        encoded = cls.encode(decoded)
        return encoded