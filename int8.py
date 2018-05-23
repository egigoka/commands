#! python3
# -*- coding: utf-8 -*-
"""Internal module, import it like "from commands.int8 import Int"
"""
__version__ = "0.0.5"


class Int:  # pylint: disable=too-few-public-methods
    """Methods to interact with integers
    """
    @staticmethod
    def from_to(start, end, to_str=False):
        """return list of integers, if argument
        "to_str" activated, return list of strings with equal length
        if "list" arg activated, list will be returned, otherwise, it will be iterable obj
        """
        from .str8 import Str
        from .os8 import OS
        if OS.is_python3:
            roots = range(start, end + 1)
        else:
            roots = xrange(start, end + 1)  # pylint: disable=undefined-variable
        if to_str:
            output = []
            max_len = max(len(str(start)), len(str(end)))
            for root in roots:
                if root < 0:
                    output.append("-" + Str.leftpad(-root, max_len - 1, 0))
                else:
                    output.append(Str.leftpad(root, max_len, 0))
            return output
        return roots
