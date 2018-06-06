#! python3
# -*- coding: utf-8 -*-
"""Internal module with shit functions
"""
__version__ = "2.0.5"


def dirify(object_, quiet=False):
    """Print and return list of object public attributes
    :param object_: object to input
    :param quiet: suppress output to console
    :return: list of object public attributes
    """
    output = []
    for subobj in dir(object_):
        if "__" not in subobj:
            if not quiet:
                print(subobj)
            output.append(subobj)
    return output
