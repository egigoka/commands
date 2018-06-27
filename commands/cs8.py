#! python3
# -*- coding: utf-8 -*-
"""Internal module with shit functions
"""
__version__ = "2.3.0"


def dirify(object_, regexp="*", quiet=False):
    """Print and return list of object public attributes
    :param object_: object to input
    :param regexp: string with shell-like wildcards for filtering
    :param quiet: suppress output to console
    :return: list of object public attributes
    """
    from .list8 import List
    output = []
    for subobj in List.wildcard_search(dir(object_), regexp):
        if "__" not in subobj:
            if not quiet:
                print(subobj)
            output.append(subobj)
    return output

def multiple(*types):
    from typing import Union
    return Union[types]
