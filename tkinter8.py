#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.1"


class Tkinter():
    @staticmethod
    def color(red, green, blue):
        """
        :param red: red intensity (0-255)
        :param green: green intensity (0-255)
        :param blue: green intensity (0-255)
        :return: string of color matching for use in Tkinter
        """
        return str('#%02x%02x%02x' % (red, green, blue))
