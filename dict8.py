#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with dicts
"""
__version__ = "0.0.4"


class Dict:
    """Class to work with dicts
    """
    @staticmethod
    def iterable(dict_):
        """Return iterable dict
        :param dict_: input dict
        :return: iterable dict
        """
        if not isinstance(dict_, dict):
            raise TypeError("There must be dict in input")
        return dict_.items()

    @staticmethod
    def sorted_by_key(dict_, case_insensitive=False):
        """Return sorted dict
        :param dict_: input dict
        :param case_insensitive: sort dict insensitive
        :return:
        """
        if case_insensitive:
            output = {}
            for i in sorted(dict_, key=str.lower):
                output[i] = dict_[i]
            return output
        import collections
        return collections.OrderedDict(sorted(dict_.items()))
