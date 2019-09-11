#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with bytes
"""

__version__ = "0.0.1"


class Bytes:
    @staticmethod
    def get_encoding(slice_of_raw_data):
        # check for utf-16-le
        fail_symbols = 0
        for cnt, sym in enumerate(slice_of_raw_data):
            if cnt % 2 != 0:
                if sym != 0:
                    fail_symbols += 1
        utf_16_le = False
        if fail_symbols / (len(slice_of_raw_data) / 2) < 0.2:
            utf_16_le = True
        if utf_16_le:
            encoding = "utf-16-le"
        # end check for utf-16-le
        else:
            import chardet
            encoding = chardet.detect(slice_of_raw_data)["encoding"]
        return encoding

    @classmethod
    def to_string(cls, slice_of_raw_data: bytes):
        if isinstance(slice_of_raw_data, str):
            return slice_of_raw_data
        return slice_of_raw_data.decode(encoding=cls.get_encoding(slice_of_raw_data))