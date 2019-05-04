#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with dicts
"""
__version__ = "0.4.0"



class imdict(dict):
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
    def sorted_by_key(dict_, case_insensitive=False):
        """Return sorted dict
        <br>`param dict_` input dict
        <br>`param case_insensitive` sort dict insensitive
        <br>`return` OrderedDict
        """
        if case_insensitive:
            output = {}
            for i in sorted(dict_, key=str.lower):
                output[i] = dict_[i]
            return output
        import collections
        return collections.OrderedDict(sorted(dict_.items()))

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
    def all_keys_lambda(cls, dict_, func, args=(), kwargs=imdict({})):
        output_dict = {}
        for key, value in cls.iterable(dict_):
            output_dict[func(key, *args, **kwargs)] = value
        return output_dict

    @classmethod
    def all_values_lambda(cls, dict_, func, args=(), kwargs=imdict({})):
        output_dict = {}
        for key, value in cls.iterable(dict_):
            output_dict[key] = func(value, *args, **kwargs)
        return output_dict