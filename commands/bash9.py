#! python3
# -*- coding: utf-8 -*-
"""Internal module to help with bash
"""
__version__ = "0.0.4"


class Bash:  # pylint: disable=too-few-public-methods
    """Class to help with bash
    """
    from .const9 import backslash
    escape_chars = [backslash]

    @classmethod
    def argument_escape(cls, argument):
        """
        `param argument` import argument string that will be used in bash
        `return` string with escaped symbols, defined in Bash.escape_chars
        """
        from .const9 import backslash
        from .str9 import Str
        for char in cls.escape_chars:
            argument = argument.replace(char, backslash + char)
        return Str.to_quotes(argument)
