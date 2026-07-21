#! python3
# -*- coding: utf-8 -*-
"""Helpers to make class-only APIs usable from instances without boilerplate."""
from __future__ import annotations

from typing import Any, Callable, Type, cast


def add_instance_shortcuts(*classes: Type[Any]) -> None:
    """Attach a generic __getattr__ that forwards to class attributes if callable.

    This keeps existing explicit __getattr__ implementations intact.
    """
    def _delegate(self: Any, name: str) -> Callable[..., Any]:
        attr = getattr(self.__class__, name)
        if callable(attr):
            return cast(Callable[..., Any], attr)
        raise AttributeError(name)

    for cls in classes:
        if not hasattr(cls, "__getattr__"):
            try:
                cls.__getattr__ = _delegate
            except (TypeError, AttributeError):
                # Skip immutable/built-in types like _thread.lock.
                continue
