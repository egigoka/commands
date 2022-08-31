#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with dicts
"""
__version__ = "0.5.0"


class ImDict(dict):
    """Rejected PEP 351"""
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


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
    def str_lower_of_dict_key(dict_item):
        return str.lower(dict_item[0])

    @staticmethod
    def get_dict_key(dict_item):
        return dict_item[0]

    def sorted_by_key(self, dict_, case_insensitive=False, func=None):
        """Return sorted dict
        <br>`param dict_` input dict
        <br>`param case_insensitive` sort dict insensitive
        <br>`return` OrderedDict
        """
        import collections
        if func is None:
            if case_insensitive:
                func = self.str_lower_of_dict_key
            else:
                func = self.get_dict_key

        output = collections.OrderedDict()
        for i in sorted(dict_.items(), key=func):
            output[i[0]] = i[1]
        return output

    @staticmethod
    def from_str(string):
        """`param string` string
        <br>`return` dict"""
        from ast import literal_eval
        dict_ = literal_eval(string)
        assert isinstance(dict_, dict), f"Output must be dict, {type(dict_)} was found"
        return dict_

    @classmethod
    def isinstance_keys(cls, dict_, types):
        for key, value in cls.iterable(dict_):
            if not isinstance(key, types):
                return False
        return True

    @classmethod
    def isinstance_values(cls, dict_, types):
        for key, value in cls.iterable(dict_):
            if not isinstance(value, types):
                return False
        return True

    @classmethod
    def all_keys_lambda(cls, dict_, func, args=(), kwargs=ImDict({})):
        output_dict = {}
        for key, value in cls.iterable(dict_):
            output_dict[func(key, *args, **kwargs)] = value
        return output_dict

    @classmethod
    def all_values_lambda(cls, dict_, func, args=(), kwargs=ImDict({})):
        output_dict = {}
        for key, value in cls.iterable(dict_):
            output_dict[key] = func(value, *args, **kwargs)
        return output_dict
