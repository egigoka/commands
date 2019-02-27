#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64
"""
__version__ = "1.1.3"


class Base64:  # pylint: disable=too-few-public-methods
    """Class to work with base64
    """
    @classmethod
    def to_png(cls, string, filename):
        """
        :param string: string base64
        :param filename: filename to save png
        :return: None
        """
        
        
        filename = str(filename)
        if not filename.endswith(".png"):
            filename = filename + ".png"
        png_recovered = cls.to_bytes(string)
        file = open(filename, "wb")
        file.write(png_recovered)
        file.close()
    
    @staticmethod
    def to_bytes(input):
        import base64
        if isinstance(input, str):
            return base64.decodebytes(input.encode('ascii'))
        else:
            return base64.decodebytes(input)
    
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
