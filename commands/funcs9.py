#! python3
# -*- coding: utf-8 -*-
"""Internal module with shit functions
"""
__version__ = "3.0.2"


def dirify(object_, wildcard="*"):
    """Print and return list of object public attributes
    <br>`param object_` object to input
    <br>`param regexp` string with shell-like wildcards for filtering
    <br>`param quiet` suppress output to console
    <br>`return` None
    """
    from .list9 import List
    from .str9 import Str
    longest_name = 0
    for attr_str in List.wildcard_search(dir(object_), wildcard):
        if "__" not in attr_str:
            if len(attr_str) > longest_name:
                longest_name = len(attr_str)
    for attr_str in List.wildcard_search(dir(object_), wildcard):
        if "__" not in attr_str:
            print(Str.rightpad(attr_str, longest_name, " "), type(object_.__getattribute__(attr_str)))


def multiple(*types):
    from typing import Union
    return Union[types]
