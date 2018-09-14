#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for creating some random values.
"""
__version__ = "0.4.0"


class Random:
    """Class with functions for creating some random values.
    """
    @staticmethod
    def integer(minimum, maximum):
        """
        :param minimum: int, minimum value
        :param maximum: int, maximum value
        :return: int, random from 'minimum' to 'maximum'
        """
        import random
        return random.randrange(minimum, maximum + 1)

    @staticmethod
    def float(minimum, maximum):  # return random floating number
        """
        :param minimum: int|float, minimum value
        :param maximum: int|float, maximum value
        :return: float, random from 'minimum' to 'maximum'
        """
        import random
        return random.uniform(minimum, maximum)

    @staticmethod
    def string(length, string_of_symbols=None):
        """
        :param length: int, length of output string
        :param string_of_symbols: string, will be used to create output
        :return: string, with random symbols
        """
        if not string_of_symbols:
            import string
            string_of_symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits
        import random
        return ''.join(random.choices(string_of_symbols, k=length))

    @staticmethod
    def string_unicode(length):
        """
        :param length: int, length of output string
        :return: string, with random unicode symbols
        """
        import random

        try:
            get_char = unichr  # py2
        except NameError:
            get_char = chr

        # Update this to include code point ranges to be sampled
        include_ranges = [
            (0x0021, 0x0021),
            (0x0023, 0x0026),
            (0x0028, 0x007E),
            (0x00A1, 0x00AC),
            (0x00AE, 0x00FF),
            (0x0100, 0x017F),
            (0x0180, 0x024F),
            (0x2C60, 0x2C7F),
            (0x16A0, 0x16F0),
            (0x0370, 0x0377),
            (0x037A, 0x037E),
            (0x0384, 0x038A),
            (0x038C, 0x038C)]

        alphabet = [get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)]
        return ''.join(random.choice(alphabet) for i in range(length))

    @staticmethod
    def boolean():
        """
        :return: Boolean, random
        """
        import random
        return random.random() < 0.5

    @classmethod
    def guid(cls):
        """
        :return: string, guid in lowercase
        """
        import string
        symbols = cls.string(32, string.digits + "abcdef")
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols [12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string
