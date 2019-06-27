#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for creating some random values.
"""
__version__ = "0.6.2"


class Random:
    """Class with functions for creating some random values.
    """
    @staticmethod
    def integer(minimum, maximum, to_str=False):
        """
        <br>`param minimum` int, minimum value
        <br>`param maximum` int, maximum value
        <br>`param to_str` bool, if True - return string with len of str(maximum) param
        <br>`return` int|str, random from 'minimum' to 'maximum'
        """
        import random

        if maximum < minimum:
            temp = maximum
            maximum = minimum
            minimum = temp

        result = random.randrange(minimum, maximum + 1)
        if to_str:
            from .str9 import Str
            result = Str.leftpad(result, len(str(maximum)))
        return result

    @staticmethod
    def float(minimum, maximum):  # return random floating number
        """
        <br>`param minimum` int|float, minimum value
        <br>`param maximum` int|float, maximum value
        <br>`return` float, random from 'minimum' to 'maximum'
        """
        import random
        return random.uniform(minimum, maximum)

    @staticmethod
    def string(length, string_of_symbols=None):
        """
        <br>`param length` int, length of output string
        <br>`param string_of_symbols` string, will be used to create output
        <br>`return` string, with random symbols
        """
        if not string_of_symbols:
            import string
            string_of_symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits
        import random
        return ''.join(random.choices(string_of_symbols, k=length))

    @staticmethod
    def item(*objects, **kwargs):
        import random
        if len(objects) == 1:
            objects = objects[0]
        if kwargs:
            objects = kwargs

        if isinstance(objects, dict):
            key, value = random.choice(list(objects.items()))
            return key, value
        else:
            return random.choice(objects)

    @staticmethod
    def string_unicode(length):
        """
        <br>`param length` int, length of output string
        <br>`return` string, with random unicode symbols
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
        <br>`return` Boolean, random
        """
        import random
        return random.random() < 0.5

    @classmethod
    def guid(cls):
        """
        <br>`return` string, guid in lowercase
        """
        import string
        symbols = cls.string(32, string.digits + "abcdef")
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols [12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string
