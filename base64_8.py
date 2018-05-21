#! python3
# -*- coding: utf-8 -*-
# http://python.su/forum/topic/15531/?page=1#post-93316
__version__ = "1.0.1"


class Base64:
    @staticmethod
    def to_png(string, filename):
        import base64
        png_recovered = base64.decodestring(string.encode('ascii'))  # decode string to pure picture
        f = open(str(filename)+".png", "wb")
        f.write(png_recovered)
        f.close()
