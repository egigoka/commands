#! python3
# -*- coding: utf-8 -*-
"""Internal module with constants
"""
__version__ = "1.2.0"

# pylint: disable=invalid-name, anomalous-backslash-in-string
newline = '\n'  # string with LF newline
ruble = u"\u20bd"  # string with ₽ symbol
backslash = "\ "[:1]  # string with backslash
newline2 = "\r\n"  # string with CRLF newline
rtl = "\u202e"  # string with Right-To-Left character https://resources.infosecinstitute.com/spoof-using-right-to-left-override-rtlo-technique-2/
KiB = 1024
MiB = KiB*1024
GiB = MiB*1024