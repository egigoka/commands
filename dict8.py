#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.1"


class Dict:
    @staticmethod
    def iterable(dict_):
        if not isinstance(dict_, dict):
            raise TypeError("There must be dict in input")
        return dict_.items()

    @staticmethod
    def sorted_by_key(dict, case_insensitive=False):
        if case_insensitive == True:
            output = {}
            for i in sorted(dict, key=str.lower):
                output[i] = dict[i]
            return output
        else:
            import collections
            return collections.OrderedDict(sorted(dict.items()))