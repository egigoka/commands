#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for creating some random values.
"""
__version__ = "0.1.1"


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
    def string(length):
        """
        :param length: int, length of output string
        :return: string, with random latin symbols
        """
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
