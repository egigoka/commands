#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with base64
"""
__version__ = "1.0.4"


class Base64:  # pylint: disable=too-few-public-methods
    """Class to work with base64
    """
    @staticmethod
    def to_png(string, filename):
        """
        :param string: string base64
        :param filename: filename to save png
        :return: None
        """
        import base64
        png_recovered = base64.decodebytes(string.encode('ascii'))  # decode string to pure picture
        filename = str(filename)
        if not filename.endswith(".png"):
            filename = filename + ".png"
        file = open(filename, "wb")
        file.write(png_recovered)
        file.close()
