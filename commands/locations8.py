#! python3
# -*- coding: utf-8 -*-
"""Internal module with some predefined paths
"""
from .os8 import OS
__version__ = "0.0.3"


class Locations:  # pylint: disable=too-few-public-methods
    """Class with some predefined paths
    """
    if OS.windows:
        texteditor = "notepad"  # d notepad is in every version of Windows, yea?
        py = "py"
        pyw = "pyw"
    elif OS.macos:
        texteditor = "open"  # d just open default program for file
        py = "python3"
        pyw = "python3"
    elif OS.linux:
        texteditor = "nano"  # d nano is everywhere, I suppose? ]-:
        py = "python3"
        pyw = "python3"
