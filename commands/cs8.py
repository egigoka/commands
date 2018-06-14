#! python3
# -*- coding: utf-8 -*-
"""Internal module with shit functions
"""
__version__ = "2.1.0"


def dirify(object_, regexp="*", quiet=False):
    """Print and return list of object public attributes
    :param object_: object to input
    :param quiet: suppress output to console
    :return: list of object public attributes
    """
    output = []
    for subobj in List.wildcard_search(dir(object_), regexp):
        if "__" not in subobj:
            if not quiet:
                print(subobj)
            output.append(subobj)
    return output
