#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with dicts
"""
__version__ = "0.1.0"


class Dict:
    """Class to work with dicts
    """
    @staticmethod
    def iterable(dict_, copy_dict=False):
        """Return iterable dict
        <br>`param dict_` input dict
        <br>`param copy_dict` bool, if True, return iterable copy of dict
        <br>`return` iterable dict
        """
        if not isinstance(dict_, dict):
            raise TypeError("There must be dict in input")
        if copy_dict:
            return dict_.copy().items()
        return dict_.items()

    @staticmethod
    def sorted_by_key(dict_, case_insensitive=False):
        """Return sorted dict
        <br>`param dict_` input dict
        <br>`param case_insensitive` sort dict insensitive
        <br>`return`
        """
        if case_insensitive:
            output = {}
            for i in sorted(dict_, key=str.lower):
                output[i] = dict_[i]
            return output
        import collections
        return collections.OrderedDict(sorted(dict_.items()))
