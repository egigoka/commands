#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.1"


class Locations:
    from .os8 import OS
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
