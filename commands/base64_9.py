#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64
"""
__version__ = "2.0.1"


class Base64:
    """Class to work with base64"""
    
    @staticmethod
    def to_bytes(input_):
        import base64
        if isinstance(input_, str):
            return base64.decodebytes(input_.encode('ascii'))
        else:
            return base64.decodebytes(input_)
    
    @staticmethod
    def from_bytes(bytes_):
        import base64
        return base64.encodebytes(bytes_)
    
    @classmethod
    def to_file(cls, string, filename):
        from .file9 import File
        file_bytes = cls.to_bytes(string)
        File.write(filename, file_bytes, mode="wb")
    
    @classmethod
    def from_file(cls, filename):
        with open(filename, mode="rb") as file:
            file_bytes = file.read()
        return cls.from_bytes(file_bytes)
