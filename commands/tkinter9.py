#! python3
# -*- coding: utf-8 -*-
"""Internal module to simplify work with tkinter
"""
__version__ = "0.0.2"


class Tkinter:  # pylint: disable=too-few-public-methods
    """Class to simplify work with tkinter
    """
    @staticmethod
    def color(red, green, blue):
        """
        `param red` red intensity (0-255)
        `param green` green intensity (0-255)
        `param blue` green intensity (0-255)
        `return` string of color matching for use in Tkinter
        """
        return str('#%02x%02x%02x' % (red, green, blue))
