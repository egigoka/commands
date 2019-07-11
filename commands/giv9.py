#! python3
# -*- coding: utf-8 -*-
"""Global Interpreter Variables
"""
__version__ = "0.0.3"


class GIV:
    """Global Interpreter Variables implementation
    """

    json = None

    @classmethod
    def init(cls):
        if cls.json is None:
            from .path9 import Path
            from .json9 import Json

            json_path = Path.combine(Path.temp(), "commands_GIV.json")
            cls.json = Json(json_path, debug=False, quiet=True)

    @classmethod
    def __getitem__(cls, item):
        cls.init()
        return cls.json.__getitem__(item)

    @classmethod
    def __setitem__(cls, key, value):
        cls.init()
        return cls.json.__setitem__(key, value)

    @classmethod
    def clean(cls):
        cls.init()
        cls.json.string = {}
        cls.json.save()

GIV = GIV()