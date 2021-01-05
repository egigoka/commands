#! python3
# -*- coding: utf-8 -*-
"""Global Interpreter Variables
"""
__version__ = "0.1.0"


class GIV:
    """Global Interpreter Variables implementation
    """

    json = None

    @classmethod
    def init(cls):
        if cls.json is None:
            from .path9 import Path
            from .json9 import JsonDict

            json_path = Path.combine(Path.temp(), "commands_GIV.json")
            cls.json = JsonDict(json_path, debug=False, quiet=True)

    @classmethod
    def __getitem__(cls, item):
        cls.init()
        cls.json.load()
        return cls.json.__getitem__(item)

    @classmethod
    def __setitem__(cls, key, value):
        cls.init()
        result = cls.json.__setitem__(key, value)
        cls.json.save()
        return result

    @classmethod
    def __repr__(cls):
        cls.init()
        return cls.json.__repr__()

    @classmethod
    def clean(cls):
        cls.init()
        cls.json.string = {}
        cls.json.save()

    @classmethod
    def pop(cls, *args):
        cls.init()
        result = cls.json.pop(*args)
        cls.json.save()
        return result


GIV = GIV()
