#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.2"

class Bash:
    from .const8 import backslash
    escapable_chars = [backslash]

    @classmethod
    def argument_escape(cls, argument):
        from .const8 import backslash
        from .str8 import Str
        for char in cls.escapable_chars:
            argument = argument.replace(char, backslash + char)
        return Str.to_quotes(argument)

