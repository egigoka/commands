#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64
"""
__version__ = "1.1.0"


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
        png_recovered = cls.to
        file = open(filename, "wb")
        file.write(png_recovered)
        file.close()
    
    @staticmethod
    def to_bytes(string):
        import base64
        return base64.decodebytes(string.encode('ascii'))
    
    @staticmethod
    def to_string(bytes_):
        import base64
        return base64.encodebytes(bytes_)
    
    @classmethod
    def to_file(cls, string, filename):
        from .file9 import File
        file_bytes = cls.to_bytes(string)
        File.write(filename, string, mode="wb")
    
    @classmethod
    def from_file(cls, filename):
        with open(filename, mode="rb") as file:
            file_bytes = file.read()
        return cls.to_string(file_bytes)
