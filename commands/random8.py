#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for creating some random values.
"""
__version__ = "0.3.2"


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
