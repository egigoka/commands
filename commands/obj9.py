#! python3
# -*- coding: utf-8 -*-
"""Internal module for logging
"""
from typing import Any

__version__ = "0.0.1"


class Obj:
    @staticmethod
    def cast_to(obj: Any, cast_to: list):
        for type_to in cast_to:
            try:
                return type_to(obj)
            except Exception:
                pass
        return obj
